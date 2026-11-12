import fs from 'fs';
import { getDocument } from 'pdfjs-dist/legacy/build/pdf.mjs';
const data = new Uint8Array(fs.readFileSync('.tmp/body.pdf'));
const doc = await getDocument({ data }).promise;
const out = await doc.getOutline();
async function walk(ns) {
  for (const n of ns || []) {
    if (n.title.includes('附录') || n.title.includes('后记') || n.title.includes('A.8')) {
      console.log(JSON.stringify(n.title), 'dest=', JSON.stringify(n.dest));
      try {
        const d = typeof n.dest === 'string' ? await doc.getDestination(n.dest) : n.dest;
        console.log('  page', await doc.getPageIndex(d[0]));
      } catch (e) { console.log('  ERR', e.message); }
    }
    if (n.items) await walk(n.items);
  }
}
await walk(out);
