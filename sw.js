const V='athena-v1',A=['./','index.html','tabel.html','backup.html','css/style.css','js/layout.js','manifest.webmanifest','assets/icon-192.png','assets/hero.webp','data/tabel.json','data/sumber.json','data/update.json'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(V).then(c=>c.addAll(A)));self.skipWaiting()});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!=V).map(x=>caches.delete(x)))));self.clients.claim()});
self.addEventListener('fetch',e=>{if(e.request.method!='GET'||new URL(e.request.url).origin!=location.origin)return;
e.respondWith(caches.open(V).then(async c=>{const m=await c.match(e.request,{ignoreSearch:true});const f=fetch(e.request).then(r=>{if(r.ok)c.put(e.request,r.clone());return r}).catch(()=>m);return m||f}))});
