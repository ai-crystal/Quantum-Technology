import puppeteer from 'puppeteer-core';
const b = await puppeteer.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe', headless:true, args:['--no-sandbox']});
const p = await b.newPage();
await p.goto('http://localhost:8099/', {waitUntil:'networkidle2'});
await new Promise(r=>setTimeout(r,1500));
const info = await p.evaluate(() => {
  const c = document.querySelector('section.cover');
  const cs = getComputedStyle(c);
  const before = getComputedStyle(c, '::before');
  const after = getComputedStyle(c, '::after');
  return {
    cls: c.className,
    bg: cs.backgroundImage.slice(0,120),
    bgc: cs.backgroundColor,
    filter: cs.filter,
    opacity: cs.opacity,
    beforeBg: before.backgroundColor, beforeContent: before.content, beforeOpacity: before.opacity,
    afterBg: after.backgroundColor, afterContent: after.content, afterOpacity: after.opacity
  };
});
console.log(JSON.stringify(info, null, 1));
await b.close();
