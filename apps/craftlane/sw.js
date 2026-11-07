// Optional offline mode for static assets only. Never caches imported media or exports.
const CACHE_NAME='craftlane-company-static-v3';
const ASSETS=['./','./index.html','./assets/styles.css','./assets/app.js','./assets/favicon.svg','./assets/icon-192.png','./assets/icon-512.png','./manifest.webmanifest','./privacy.html','./tools/index.html','./tools/thumbnail.html','./tools/motion.html','./tools/resize.html','./tools/captions.html','./tools/hooks.html'];
self.addEventListener('install',event=>{
  event.waitUntil(caches.open(CACHE_NAME).then(cache=>cache.addAll(ASSETS)).then(()=>self.skipWaiting()));
});
self.addEventListener('activate',event=>{
  event.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(key=>key.startsWith('craftlane-company-static-')&&key!==CACHE_NAME).map(key=>caches.delete(key)))).then(()=>self.clients.claim()));
});
self.addEventListener('fetch',event=>{
  if(event.request.method!=='GET')return;
  const url=new URL(event.request.url);if(url.origin!==self.location.origin)return;
  if(event.request.mode==='navigate'){
    event.respondWith(fetch(event.request).then(response=>response.ok?response:caches.match(event.request).then(hit=>hit||caches.match('./index.html'))).catch(()=>caches.match(event.request).then(hit=>hit||caches.match('./index.html'))));return;
  }
  if(!ASSETS.some(path=>url.pathname===new URL(path,self.registration.scope).pathname))return;
  event.respondWith(caches.match(event.request,{ignoreSearch:true}).then(hit=>hit||fetch(event.request)));
});