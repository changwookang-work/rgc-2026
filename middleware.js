// Vercel Routing Middleware — runs before every request (pages and PDFs).
// 1) Old domain rgc-2026.vercel.app -> new site.
// 2) From 2026-11-18 19:00 KST the site closes: every path shows the thank-you page (no downloads).
export const config = { matcher: '/:path*' };

const NEW_HOST = 'renadog-global-connect-2026.vercel.app';
const CUTOFF = Date.parse('2026-11-18T19:00:00+09:00');

const THANK_YOU = `<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<title>RENADOG GLOBAL CONNECT 2026</title>
<style>@font-face{font-family:Poppins;font-weight:600;src:url(/assets/fonts/poppins-latin-600-normal.woff2) format('woff2')}
@font-face{font-family:'Instrument Serif';font-style:italic;src:url(/assets/fonts/instrument-serif-latin-400-italic.woff2) format('woff2')}
html,body{margin:0;background:#141414;color:#fff;font-family:Poppins,sans-serif;-webkit-font-smoothing:antialiased}
.w{max-width:560px;margin:0 auto;padding:28px 22px;min-height:100vh;box-sizing:border-box;display:flex;flex-direction:column}
.mono{width:40px;height:40px;border:1.4px solid #fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font:italic 400 0 serif}
.mono:before{content:'R';font:400 25px/1 'Instrument Serif',serif;font-style:normal}
.c{flex:1;display:flex;flex-direction:column;justify-content:center}
.e{font:500 11px Poppins,sans-serif;letter-spacing:.22em;color:#A8A8A8;text-transform:uppercase}
h1{font:600 28px/1.25 Poppins,sans-serif;margin:12px 0 0}
em{font:italic 400 36px/1.1 'Instrument Serif',serif;color:#EC7969}
.r{width:44px;height:2px;background:#EC7969;margin:22px 0}
p{color:#A8A8A8;font-size:13px;margin:0}</style></head>
<body><div class="w"><div class="mono"></div><div class="c"><div class="e">Renadog Global Connect 2026</div>
<h1>Thank you for visiting<br><em>Renadog Global Connect</em><br>today.</h1><div class="r"></div>
<p>This page is no longer available.</p></div></div></body></html>`;

export default function middleware(request) {
  const url = new URL(request.url);
  const isAsset = url.pathname.startsWith('/assets/');
  if (url.hostname.startsWith('rgc-2026') && url.hostname.endsWith('.vercel.app')) {
    return Response.redirect('https://' + NEW_HOST + url.pathname + url.search, 307);
  }
  if (Date.now() >= CUTOFF && !isAsset) {
    return new Response(THANK_YOU, {
      status: 200,
      headers: { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store' },
    });
  }
}
