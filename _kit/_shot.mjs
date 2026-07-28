import { chromium } from 'playwright'
import { createServer } from 'node:http'
import { readFileSync, existsSync } from 'node:fs'
import { join, extname } from 'node:path'
const [dir, out, ...pages] = process.argv.slice(2)
const T = { '.html':'text/html','.css':'text/css','.js':'text/javascript','.jpg':'image/jpeg','.png':'image/png','.svg':'image/svg+xml' }
const srv = createServer((q,r)=>{const f=join(dir,decodeURIComponent(q.url.split('?')[0]));if(!existsSync(f)){r.writeHead(404);return r.end()}r.writeHead(200,{'content-type':T[extname(f)]??'application/octet-stream'});r.end(readFileSync(f))}).listen(0)
const port = srv.address().port
const b = await chromium.launch(); const errs = []
for (const page of pages) for (const [w,h,tag,full] of [[1440,1000,'desk',true],[390,844,'mob',false]]) {
  const p = await b.newPage({ viewport: { width: w, height: h } })
  p.on('pageerror', e => errs.push(`${page} ${tag}: ${e.message}`))
  await p.goto(`http://127.0.0.1:${port}/${page}`, { waitUntil: 'networkidle' })
  await p.waitForTimeout(400)
  await p.screenshot({ path: `${out}/${page.replace('.html','')}-${tag}.png`, fullPage: full })
  await p.close()
}
await b.close(); srv.close()
console.log(errs.length ? errs.join('\n') : 'shots ok')
