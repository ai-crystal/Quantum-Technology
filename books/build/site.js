/**
 * 生成系列首页、根侧栏与各册首页。
 * 由 build.js 在构建结束后调用，也可单独运行：node site.js
 */
const fs = require('fs');
const path = require('path');
const { PDFDocument } = require('pdf-lib');

const BUILD = __dirname;
const ROOT = path.resolve(BUILD, '..', '..');
const BOOKS = path.join(ROOT, 'books');
const OUT = path.join(ROOT, 'output');
const ORDER = ['intro', 'foundations', 'computing', 'devices', 'qec', 'network'];

function readFirstHeading(file) {
  if (!fs.existsSync(file)) return null;
  const line = fs.readFileSync(file, 'utf8').split('\n')[0].trim();
  const m = line.match(/^#\s+(.+)$/);
  return m ? m[1].trim() : null;
}

async function pageCount(pdf) {
  if (!fs.existsSync(pdf)) return null;
  try {
    const doc = await PDFDocument.load(fs.readFileSync(pdf), { updateMetadata: false });
    return doc.getPageCount();
  } catch (e) {
    return null;
  }
}

async function main() {
  const books = [];
  for (const name of ORDER) {
    const dir = path.join(BOOKS, name);
    if (!fs.existsSync(path.join(dir, 'book.json'))) continue;
    const meta = JSON.parse(fs.readFileSync(path.join(dir, 'book.json'), 'utf8'));
    const st = JSON.parse(fs.readFileSync(path.join(dir, 'structure.json'), 'utf8'));
    const chapters = [];
    for (const part of st.parts) {
      for (const ch of part.chapters) {
        const title = readFirstHeading(path.join(dir, 'chapters', ch + '.md')) || ch;
        if (fs.existsSync(path.join(dir, 'chapters', ch + '.md'))) chapters.push({ ch, title });
      }
    }
    const pages = await pageCount(path.join(OUT, meta.pdf));
    books.push({ name, meta, chapters, pages });
  }

  // 根侧栏
  const lines = ['- [系列首页](/README.md)', ''];
  for (const b of books) {
    lines.push(`- **${b.meta.volume} ${b.meta.title}**`);
    lines.push(`  - [本册首页](/books/${b.name}/README.md)`);
    for (const c of b.chapters) lines.push(`  - [${c.title}](/books/${b.name}/chapters/${c.ch}.md)`);
    lines.push(`  - [下载 PDF](/output/${b.meta.pdf})`);
  }
  fs.writeFileSync(path.join(ROOT, '_sidebar.md'), lines.join('\n') + '\n', 'utf8');

  // 首页
  const rows = books.map((b) => `| ${b.meta.volume} | ${b.meta.title} | ${b.meta.subtitle} | ${b.pages ? b.pages + ' 页' : '待生成'} | [阅读](books/${b.name}/README.md) | [PDF](output/${b.meta.pdf}) |`);
  const readme = `# 量子学技术

> 一套讲量子技术的书　·　作者 Dr. Dezeming

量子技术不只是量子计算。它还包括量子通信、量子精密测量、量子器件与量子纠错。这套书按这个范围展开，一册入门铺全貌，其余各册钻进具体方向。

## 分册

| 册 | 书名 | 副标题 | 篇幅 | 在线阅读 | 下载 |
|---|---|---|---|---|---|
${rows.join('\n')}

## 在线阅读

站点部署在 GitHub Pages 上，打开 [https://ai-crystal.github.io/Quantum-Technology/](https://ai-crystal.github.io/Quantum-Technology/) 可以从封面进入，按册浏览并下载 PDF。

## 怎么读

第一册是入门，从黑体辐射讲到量子芯片，把整个领域的脉络走一遍，不深究细节。后面几册各自独立，可以按兴趣挑着读，不必按顺序。

每一册的正文都在 \`books/<册名>/chapters/\`，插图在 \`books/<册名>/images/\`，绘图代码在 \`books/code/<册名>/\`。站点直接引用这些文件，没有第二份副本。

## 构建

双击根目录的 \`build.bat\` 构建全部，或 \`build-<册名>.bat\` 只构建某一册。
`;
  fs.writeFileSync(path.join(ROOT, 'README.md'), readme, 'utf8');

  // 各册首页
  for (const b of books) {
    const first = b.chapters.length ? b.chapters[0].ch : 'ch01';
    const items = b.chapters.map((c) => `- [${c.title}](chapters/${c.ch}.md)`).join('\n');
    const text = `# ${b.meta.title}

> ${b.meta.volume}　·　${b.meta.subtitle}

${b.meta.blurb || ''}

## 在线阅读

- [从第 1 章开始](chapters/${first}.md)
- [下载本册 PDF](../../output/${b.meta.pdf})

## 目录

${items}
`;
    fs.writeFileSync(path.join(BOOKS, b.name, 'README.md'), text, 'utf8');
  }

  console.log(`  站点文件已更新，共 ${books.length} 册`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
