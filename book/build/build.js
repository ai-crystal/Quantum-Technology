/**
 * 量子学技术 —— 书籍构建脚本
 * Markdown -> HTML -> PDF（Chrome headless），两遍编译以填充目录页码。
 * 只依赖 Node 与本机 Chrome / Edge，无需 LaTeX。
 */
const fs = require('fs');
const path = require('path');
const MarkdownIt = require('markdown-it');
const katex = require('katex');
const hljs = require('highlight.js');
const puppeteer = require('puppeteer-core');
const { PDFDocument } = require('pdf-lib');

const BUILD = __dirname;
const BOOK = path.resolve(BUILD, '..');
const ROOT = path.resolve(BOOK, '..');
const TMP = path.join(BUILD, '.tmp');
const CACHE = path.join(TMP, 'pages.json');
const OUTPUT = path.join(ROOT, 'output');

const structure = JSON.parse(fs.readFileSync(path.join(BUILD, 'structure.json'), 'utf8'));
const meta = JSON.parse(fs.readFileSync(path.join(BOOK, 'front', 'meta.json'), 'utf8'));

function fileUrl(p) {
  let s = p.replace(/\\/g, '/');
  s = encodeURI(s).replace(/#/g, '%23').replace(/\?/g, '%3F');
  return 'file:///' + s.replace(/^\//, '');
}

function findBrowser() {
  const cands = [
    process.env.CHROME_PATH,
    'C:/Program Files/Google/Chrome/Application/chrome.exe',
    'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
    'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
    'C:/Program Files/Microsoft/Edge/Application/msedge.exe',
  ].filter(Boolean);
  for (const c of cands) if (fs.existsSync(c)) return c;
  throw new Error('未找到 Chrome 或 Edge，请安装后重试，或设置环境变量 CHROME_PATH。');
}

/* ---------------- Markdown 渲染 ---------------- */

const md = new MarkdownIt({ html: true, linkify: false, typographer: false, breaks: false });

// 行内公式 $...$
md.inline.ruler.after('escape', 'math_inline', function (state, silent) {
  const src = state.src;
  if (src[state.pos] !== '$') return false;
  if (src[state.pos + 1] === '$') return false;
  if (state.pos > 0 && src[state.pos - 1] === '\\') return false;
  let pos = state.pos + 1;
  let found = false;
  while (pos < state.posMax) {
    const ch = src[pos];
    if (ch === '\\') { pos += 2; continue; }
    if (ch === '\n') return false;
    if (ch === '$') { found = true; break; }
    pos++;
  }
  if (!found) return false;
  const content = src.slice(state.pos + 1, pos);
  if (!content.trim() || /^\s|\s$/.test(content)) return false;
  if (silent) { state.pos = pos + 1; return true; }
  let out;
  try {
    out = katex.renderToString(content, { displayMode: false, throwOnError: false, strict: 'ignore', output: 'html' });
  } catch (e) { return false; }
  const token = state.push('html_inline', '', 0);
  token.content = out;
  state.pos = pos + 1;
  return true;
});

// 行间公式 $$ ... $$
md.block.ruler.after('blockquote', 'math_block', function (state, startLine, endLine, silent) {
  let pos = state.bMarks[startLine] + state.tShift[startLine];
  let max = state.eMarks[startLine];
  if (pos + 2 > max) return false;
  if (state.src.slice(pos, pos + 2) !== '$$') return false;
  const tail = state.src.slice(pos + 2, max);
  if (tail.trim().endsWith('$$') && tail.trim().length >= 2) {
    if (silent) return true;
    const content = tail.trim().slice(0, -2).trim();
    state.line = startLine + 1;
    const token = state.push('math_block', '', 0);
    token.content = content;
    token.map = [startLine, state.line];
    return true;
  }
  let nextLine = startLine;
  let found = false;
  let buf = tail.trim() ? tail.trim() + '\n' : '';
  for (nextLine = startLine + 1; nextLine < endLine; nextLine++) {
    const lp = state.bMarks[nextLine] + state.tShift[nextLine];
    const lm = state.eMarks[nextLine];
    const lineText = state.src.slice(lp, lm);
    if (lineText.trim() === '$$' || /^\s*\$\$\s*$/.test(lineText)) { found = true; break; }
    buf += lineText + '\n';
  }
  if (!found) return false;
  if (silent) return true;
  state.line = nextLine + 1;
  const token = state.push('math_block', '', 0);
  token.content = buf.trim();
  token.map = [startLine, state.line];
  return true;
});

md.renderer.rules.math_block = function (tokens, idx) {
  const out = katex.renderToString(tokens[idx].content, { displayMode: true, throwOnError: false, strict: 'ignore', output: 'html' });
  return '<div class="math-display">' + out + '</div>\n';
};

md.options.highlight = function (str, lang) {
  if (lang && hljs.getLanguage(lang)) {
    try {
      return '<pre class="hljs"><code>' + hljs.highlight(str, { language: lang, ignoreIllegals: true }).value + '</code></pre>';
    } catch (e) { /* 忽略 */ }
  }
  return '<pre class="hljs"><code>' + md.utils.escapeHtml(str) + '</code></pre>';
};

/* ---------------- 读取文稿 ---------------- */

function listFiles() {
  const items = [];
  for (const f of structure.front) items.push({ file: f.file, kind: f.kind });
  for (const part of structure.parts) {
    items.push({ file: part.file, kind: 'part' });
    for (const ch of part.chapters) items.push({ file: `chapters/${ch}.md`, kind: 'chapter', ch });
  }
  for (const a of structure.appendix) items.push({ file: a, kind: 'appendix' });
  for (const f of structure.back) items.push({ file: f.file, kind: f.kind });
  return items;
}

function stripTags(s) {
  return s.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
}

function loadDocs() {
  const items = listFiles();
  const docs = [];
  let headingSeq = 0;
  for (const it of items) {
    const abs = path.join(BOOK, it.file);
    if (!fs.existsSync(abs)) {
      console.warn('  [跳过缺失文件] ' + it.file);
      continue;
    }
    const raw = fs.readFileSync(abs, 'utf8').replace(/\r\n/g, '\n');
    const tokens = md.parse(raw, {});
    const heads = [];
    for (let i = 0; i < tokens.length; i++) {
      const t = tokens[i];
      if (t.type === 'heading_open' && (t.tag === 'h1' || t.tag === 'h2')) {
        const level = t.tag === 'h1' ? 1 : 2;
        const inline = tokens[i + 1];
        const text = stripTags(inline ? inline.content : '');
        if (text.startsWith('{{TOC}}')) continue;
        const id = 's' + (++headingSeq);
        t.attrSet('id', id);
        heads.push({ level, text, id });
      }
    }
    let html = md.renderer.render(tokens, md.options, {});
    // 篇首页用原始 HTML 写 h1，补一条目录条目，保证目录与书签一致
    if (it.kind === 'part' && heads.length === 0) {
      const m = html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/);
      if (m) heads.push({ level: 1, text: stripTags(m[1]), id: 'p' + (++headingSeq) });
    }
    // 图题：紧跟在图片之后的、以“图 x-y”开头的段落
    html = html.replace(/<p>(\s*)(图\s*\d+[-–—]\d+)/g, '<p class="fig-cap">$1$2');
    // 图片路径改写为可被 Chrome 读取的绝对路径
    const dir = path.dirname(abs);
    html = html.replace(/(<img[^>]*\ssrc=")([^"]+)(")/g, (m, a, src, c) => {
      if (/^(https?:|data:|file:)/.test(src)) return m;
      const p = path.resolve(dir, decodeURI(src));
      if (!fs.existsSync(p)) console.warn('  [缺少图片] ' + path.relative(ROOT, p) + '  (' + it.file + ')');
      return a + fileUrl(p) + c;
    });
    docs.push({ ...it, html, heads });
  }
  return docs;
}

/* ---------------- 目录 ---------------- */

function buildToc(docs, pages) {
  const rows = [];
  let hIndex = -1;
  for (const d of docs) {
    for (const h of d.heads) {
      hIndex++;
      if (h.level === 1 && d.kind === 'cover') continue;
      const pn = pages && pages[hIndex] ? String(pages[hIndex]) : '';
      const cls = h.level === 1 ? 'toc-l1' : 'toc-l2';
      const partCls = h.level === 1 && (d.kind === 'part' || d.kind === 'appendix' || d.kind === 'front' || d.kind === 'back');
      rows.push(
        `<div class="${cls}${partCls ? ' toc-part' : ''}"><span class="toc-t">${h.text}</span>` +
        `<span class="toc-dots"></span><span class="toc-num">${pn}</span></div>`
      );
    }
  }
  return `<div class="toc-page"><h1 id="toc">目录</h1>\n${rows.join('\n')}\n</div>`;
}

/* ---------------- 组装 HTML ---------------- */

const HLJS_CSS = '.hljs{display:block;overflow-x:auto;color:#24292e}.hljs-comment,.hljs-quote{color:#6a737d;font-style:italic}.hljs-keyword,.hljs-selector-tag,.hljs-literal{color:#d73a49}.hljs-string,.hljs-doctag{color:#032f62}.hljs-title,.hljs-section,.hljs-name{color:#6f42c1}.hljs-number,.hljs-built_in,.hljs-builtin-name{color:#005cc5}.hljs-attr,.hljs-attribute{color:#b31d28}.hljs-meta{color:#735c0f}';

function pageHead(katexCss, bodyClass) {
  const css = fs.readFileSync(path.join(BUILD, 'style.css'), 'utf8');
  return `<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<title>${meta.title}</title>
<style>${katexCss}</style>
<style>${css}</style>
<style>${HLJS_CSS}</style>
</head><body class="${bodyClass}">`;
}

function composeBodyHtml(docs, pages, katexCss) {
  let body = '';
  const tocHtml = buildToc(docs, pages);
  let tocInserted = false;
  for (const d of docs) {
    if (d.kind === 'cover' || d.kind === 'backcover') continue;
    if (!tocInserted && (d.kind === 'part' || d.kind === 'chapter')) {
      body += tocHtml;
      tocInserted = true;
    }
    body += `\n<!-- ===== ${d.file} ===== -->\n` + d.html;
  }
  if (!tocInserted) body += tocHtml;
  return pageHead(katexCss, 'bodydoc') + body + '</body></html>';
}

function composeCoverHtml(docs, katexCss) {
  let body = '';
  for (const d of docs) {
    if (d.kind === 'cover' || d.kind === 'backcover') body += `\n<!-- ===== ${d.file} ===== -->\n` + d.html;
  }
  return pageHead(katexCss, 'coverdoc') + body + '</body></html>';
}

/* ---------------- PDF ---------------- */

async function printPdf(browser, html, outFile, opts) {
  const htmlFile = path.join(TMP, path.basename(outFile, '.pdf') + '.html');
  fs.writeFileSync(htmlFile, html, 'utf8');
  const page = await browser.newPage();
  try {
    await page.goto(fileUrl(htmlFile), { waitUntil: 'load', timeout: 180000 });
    await page.evaluate(() => document.fonts.ready);
    await new Promise((r) => setTimeout(r, 500));
    await page.pdf({
      path: outFile,
      format: 'A4',
      printBackground: true,
      preferCSSPageSize: false,
      outline: opts.outline !== false,
      tagged: true,
      displayHeaderFooter: !!opts.footer,
      headerTemplate: '<div></div>',
      footerTemplate: '<div style="width:100%;font-family:\'Microsoft YaHei\',sans-serif;font-size:8pt;color:#8a97a6;text-align:center;margin:0 0 6mm 0;"><span class="pageNumber"></span></div>',
      margin: opts.footer
        ? { top: '20mm', bottom: '18mm', left: '19mm', right: '19mm' }
        : { top: '0mm', bottom: '0mm', left: '0mm', right: '0mm' },
    });
  } finally {
    await page.close();
  }
}

async function readOutlinePages(pdfFile) {
  const { getDocument } = await import('pdfjs-dist/legacy/build/pdf.mjs');
  const data = new Uint8Array(fs.readFileSync(pdfFile));
  const doc = await getDocument({ data, useSystemFonts: true, isEvalSupported: false }).promise;
  const outline = (await doc.getOutline()) || [];
  const flat = [];
  async function walk(nodes, level) {
    for (const n of nodes || []) {
      let pageIdx = null;
      try {
        const dest = typeof n.dest === 'string' ? await doc.getDestination(n.dest) : n.dest;
        if (dest && dest[0]) pageIdx = await doc.getPageIndex(dest[0]);
      } catch (e) { /* 忽略 */ }
      flat.push({ level, title: n.title.trim(), page: pageIdx === null ? null : pageIdx + 1 });
      if (n.items && n.items.length) await walk(n.items, level + 1);
    }
  }
  await walk(outline, 1);
  const pages = await doc.numPages;
  await doc.destroy();
  return { flat, pages };
}

async function mergePdfs(coverPdf, bodyPdf, outPdf) {
  const body = await PDFDocument.load(fs.readFileSync(bodyPdf), { updateMetadata: false });
  const cover = await PDFDocument.load(fs.readFileSync(coverPdf));
  const total = cover.getPageCount();
  const front = await body.copyPages(cover, [0]);
  body.insertPage(0, front[0]);
  if (total > 1) {
    const back = await body.copyPages(cover, [total - 1]);
    body.addPage(back[0]);
  }
  body.setTitle(meta.title + '：' + meta.subtitle);
  body.setAuthor(meta.author);
  body.setSubject('量子力学、光学与量子计算');
  body.setKeywords(['量子力学', '量子计算', '量子光学', '量子信息']);
  body.setCreator('Markdown + Chrome PDF pipeline');
  body.setProducer('Proma book build');
  fs.writeFileSync(outPdf, await body.save({ useObjectStreams: false }));
}

function norm(s) { return String(s).normalize('NFKC').replace(/[\p{Z}\s]+/gu, "").trim(); }

function mapPages(docs, flat) {
  const heads = [];
  for (const d of docs) for (const h of d.heads) heads.push(h);
  const out = new Array(heads.length).fill(null);
  let cursor = 0;
  for (const entry of flat) {
    for (let i = cursor; i < heads.length; i++) {
      if (norm(heads[i].text) === norm(entry.title)) {
        out[i] = entry.page;
        cursor = i + 1;
        break;
      }
    }
  }
  return out;
}

/* ---------------- 侧栏 ---------------- */

function writeSidebar(docs) {
  const skip = new Set(['front/titlepage.md', 'front/copyright.md', 'front/backcover.md']);
  const lines = ['- [首页](/README.md)', ''];
  for (const d of docs) {
    if (d.kind === 'cover' || d.kind === 'backcover' || skip.has(d.file)) continue;
    const h1 = d.heads.find((h) => h.level === 1);
    if (d.kind === 'part') {
      lines.push(`- **${h1 ? h1.text : d.file}**`);
      continue;
    }
    const title = h1 ? h1.text : path.basename(d.file, '.md');
    if (d.kind === 'chapter' || d.kind === 'appendix') {
      lines.push(`  - [${title}](book/${d.file})`);
      continue;
    }
    lines.push(`- [${title}](book/${d.file})`);
  }
  lines.push('');
  lines.push('- [下载 PDF](output/' + meta.pdfName + ')');
  const text = lines.join('\n') + '\n';
  const target = path.join(ROOT, '_sidebar.md');
  const old = fs.existsSync(target) ? fs.readFileSync(target, 'utf8') : '';
  if (old !== text) fs.writeFileSync(target, text, 'utf8');
}

/* ---------------- 主流程 ---------------- */

(async function main() {
  const t0 = Date.now();
  console.log('构建《' + meta.title + '》...');
  const docs = loadDocs();
  let pages = [];
  if (fs.existsSync(CACHE)) {
    try { pages = JSON.parse(fs.readFileSync(CACHE, 'utf8')); } catch (e) { pages = []; }
  }

  const katexCssPath = path.join(BUILD, 'node_modules', 'katex', 'dist', 'katex.min.css');
  const fontDir = fileUrl(path.join(BUILD, 'node_modules', 'katex', 'dist', 'fonts/'));
  const katexCss = fs.readFileSync(katexCssPath, 'utf8').replace(/url\((['"]?)fonts\//g, 'url($1' + fontDir);

  fs.mkdirSync(OUTPUT, { recursive: true });
  fs.mkdirSync(TMP, { recursive: true });
  const outPdf = path.join(OUTPUT, meta.pdfName);
  const browserPath = findBrowser();
  console.log('使用浏览器：' + browserPath);

  const browser = await puppeteer.launch({
    executablePath: browserPath,
    headless: true,
    args: ['--allow-file-access-from-files', '--no-sandbox', '--disable-gpu', '--font-render-hinting=none'],
  });

  const bodyPdf = path.join(TMP, 'body.pdf');
  const coverPdf = path.join(TMP, 'cover.pdf');
  let flatPages = null;
  try {
    const coverHtml = composeCoverHtml(docs, katexCss);
    await printPdf(browser, coverHtml, coverPdf, { footer: false });
    console.log('  封面与封底已排版');

    for (let pass = 1; pass <= 4; pass++) {
      const html = composeBodyHtml(docs, pages, katexCss);
      await printPdf(browser, html, bodyPdf, { footer: true });
      const { flat, pages: total } = await readOutlinePages(bodyPdf);
      flatPages = flat;
      const newPages = mapPages(docs, flat);
      const same = newPages.length === pages.length && newPages.every((v, i) => v === pages[i]);
      console.log(`  第 ${pass} 遍：正文 ${total} 页，书签 ${flat.length} 条`);
      pages = newPages;
      fs.writeFileSync(CACHE, JSON.stringify(pages, null, 0));
      if (same) break;
    }
  } finally {
    await browser.close();
  }

  await mergePdfs(coverPdf, bodyPdf, outPdf);
  writeSidebar(docs);

  const size = fs.statSync(outPdf).size;
  console.log(`完成：${path.relative(ROOT, outPdf)}  ${(size / 1048576).toFixed(2)} MB  用时 ${((Date.now() - t0) / 1000).toFixed(1)} s`);
  if (size > 20 * 1048576) console.warn('  [注意] PDF 超过 20 MB，请压缩插图。');
  if (flatPages) {
    const missing = flatPages.filter((p) => !p.page).length;
    if (missing) console.warn('  [注意] 有 ' + missing + ' 条书签没有页码。');
  }
})().catch((err) => {
  console.error(err);
  process.exit(1);
});
