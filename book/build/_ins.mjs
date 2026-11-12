import puppeteer from 'puppeteer-core';
const b = await puppeteer.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe', headless:true, args:['--no-sandbox']});
const p = await b.newPage();
await p.goto('http://localhost:8099/', {waitUntil:'networkidle2'});
await new Promise(r=>setTimeout(r,2000));
const info = await p.evaluate(() => {
  const h = document.querySelector('section.cover h1');
  const cs = h ? getComputedStyle(h) : null;
  return { html: document.querySelector('section.cover .cover-main')?.outerHTML.slice(0,300), color: cs?.color, fs: cs?.fontSize };
});
console.log(JSON.stringify(info, null, 1));
await b.close();
