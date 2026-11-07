/* Craftlane — 100% client-side creator toolkit. No network requests or paid APIs. */
'use strict';
const $ = (id) => document.getElementById(id);
const $$ = (selector, scope = document) => Array.from(scope.querySelectorAll(selector));
const clamp = (v, min, max) => Math.min(max, Math.max(min, v));
const state = {
  tool: 'thumbnail', thumbRatio:'16:9',thumbStyle:'sunshine',thumbPreset:'bold',
  motionStyle:'pop',motionBg:'electric',motionRatio:'9:16',
  resizeRatio:'9:16',resizeFit:'cover',captionStyle:'clean',hooksTone:'curious'
};
let toastTimer;
function toast(message) {
  const el = $('toast'); el.textContent = message; el.classList.add('show');
  clearTimeout(toastTimer);toastTimer = setTimeout(() => el.classList.remove('show'), 3500);
}
function saveBlob(blob, fileName) {
  if (!blob || !blob.size) { toast('Nothing to download yet.'); return; }
  const url = URL.createObjectURL(blob), a = document.createElement('a');
  a.href = url; a.download = fileName; document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 30000);
}
function downloadCanvas(canvas, fileName) {
  canvas.toBlob((blob) => blob ? saveBlob(blob,fileName) : toast('Could not generate PNG in this browser.'),'image/png');
}
function setCanvasSize(canvas, ratio, base = 720) {
  const dimensions = ratio === '16:9' ? [1280,720] : ratio === '9:16' ? [720,1280] : [1080,1080];
  if (base === 540) { dimensions[0] = ratio === '16:9' ? 960 : ratio === '9:16' ? 540 : 720;
    dimensions[1] = ratio === '16:9' ? 540 : ratio === '9:16' ? 960 : 720; }
  if (base === 1440) { dimensions[0]*=2; dimensions[1]*=2; }
  if (canvas.width !== dimensions[0] || canvas.height !== dimensions[1]) {canvas.width=dimensions[0];canvas.height=dimensions[1];}
  return dimensions;
}
function chooseMime(withAudio=false) {
  if (!window.MediaRecorder) return '';
  const choices = withAudio ? ['video/webm;codecs=vp9,opus','video/webm;codecs=vp8,opus','video/webm'] : ['video/webm;codecs=vp9','video/webm;codecs=vp8','video/webm'];
  return choices.find((mime) => MediaRecorder.isTypeSupported(mime)) || '';
}
function readableError(err) {return err?.message || 'This browser could not complete the export.';}
async function copyText(value) {
  try {
    if (navigator.clipboard && window.isSecureContext) {await navigator.clipboard.writeText(value);} else {
      const hidden=document.createElement('textarea'); hidden.value=value; hidden.style.position='fixed';hidden.style.opacity='0';
      document.body.appendChild(hidden);hidden.select();if(!document.execCommand('copy'))throw Error('Copy not supported');hidden.remove();
    }
    toast('Copied to clipboard.');
  } catch {toast('Copy isn’t available here. You can select and copy the text.');}
}
function openTool(tool, scroll=true) {
  if (!['thumbnail','motion','resize','captions','hooks'].includes(tool)) return;
  state.tool=tool;
  $$('.studio-tab').forEach((b)=>{const active=b.dataset.tool===tool;b.classList.toggle('is-active',active);b.setAttribute('aria-pressed',String(active));});
  $$('.tool-panel').forEach((panel)=>{const active=panel.id==='panel-'+tool;panel.hidden=!active;panel.classList.toggle('is-active',active);});
  $('active-breadcrumb').textContent=({thumbnail:'THUMBNAIL LAB',motion:'TEXT MOTION',resize:'VIDEO RESIZER',captions:'CAPTION STUDIO',hooks:'HOOK LAB'})[tool];
  try {
    const url = new URL(window.location.href); url.searchParams.set('tool', tool);
    history.replaceState(null,'',url.pathname+url.search+url.hash);
  } catch { /* Sandbox previews and local file contexts can disallow URL rewriting. */ }
  if (tool==='thumbnail') drawThumbnail();
  if (tool==='resize') drawVideoPreview();
  if (scroll) $('studio').scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'start'});
}
function wireUI() {
  $('year').textContent=String(new Date().getFullYear());
  $('menu-toggle').addEventListener('click',()=>{const menu=$('.nav-links'); const show=!menu.classList.contains('show');menu.classList.toggle('show',show);$('menu-toggle').setAttribute('aria-expanded',String(show));});
  $$('.nav-links a').forEach((a)=>a.addEventListener('click',()=>{$('.nav-links').classList.remove('show');$('menu-toggle').setAttribute('aria-expanded','false');}));
  $$('.tool-card').forEach((b)=>b.addEventListener('click',()=>openTool(b.dataset.openTool)));
  $$('.studio-tab').forEach((b)=>b.addEventListener('click',()=>openTool(b.dataset.tool,false)));
  $$('[data-choice-group]').forEach((group)=>{
    group.querySelectorAll('button').forEach((b)=>b.addEventListener('click',()=>{
      group.querySelectorAll('button').forEach((btn)=>{btn.classList.remove('active');btn.setAttribute('aria-pressed','false');});
      b.classList.add('active');b.setAttribute('aria-pressed','true');state[group.dataset.choiceGroup.replace(/-([a-z])/g,(_,a)=>a.toUpperCase())]=b.dataset.value;
      if(group.dataset.choiceGroup.startsWith('thumb-'))drawThumbnail();
      if(group.dataset.choiceGroup.startsWith('motion-')){setCanvasSize($('motion-canvas'),state.motionRatio,540);drawMotionFrame(performance.now()/1000%Number($('motion-duration').value));}
      if(group.dataset.choiceGroup.startsWith('resize-')){setCanvasSize($('resize-canvas'),state.resizeRatio,540);drawVideoPreview();}
      if(group.dataset.choiceGroup.startsWith('caption-'))renderCaptions();
      if(group.dataset.choiceGroup.startsWith('hooks-'))generateHooks();
    }));
  });
  $$('[data-choice-group] button').forEach(b=>b.setAttribute('aria-pressed',String(b.classList.contains('active'))));
  $$('.preset').forEach(b=>b.setAttribute('aria-pressed',String(b.classList.contains('active'))));
  // Store a friendly query parameter so tools may be shared as links.
  const selected=new URLSearchParams(window.location.search).get('tool');
  if(selected)openTool(selected,false);
  window.addEventListener('popstate',()=>{const t=new URLSearchParams(location.search).get('tool');if(t)openTool(t,false);});
  $('share-tool').addEventListener('click',()=>{const u=new URL(location.href);u.searchParams.set('tool',state.tool);u.hash='studio';copyText(u.toString());});
  document.addEventListener('keydown',(e)=>{if(e.key==='Escape'&&$('menu-toggle').getAttribute('aria-expanded')==='true'){$('menu-toggle').click();}});
}

// ---------- Thumbnail Lab ----------
const thumb=$('thumb-canvas'),tctx=thumb.getContext('2d');
let thumbImage=null;
function roundRect(ctx,x,y,w,h,r,fill) {ctx.beginPath();ctx.roundRect(x,y,w,h,r);if(fill)ctx.fill();}
function multiline(ctx,raw,maxWidth,size,maxLines=4) {
  const words=(raw || '').trim().split(/\s+/).filter(Boolean), lines=[];let line='';
  for (const word of words) {const next=line ? line+' '+word : word;
    if(line && ctx.measureText(next).width>maxWidth){lines.push(line);line=word;} else {line=next;}}
  if(line)lines.push(line);
  while(lines.length>maxLines) {const last=lines.pop();lines[lines.length-1] += ' '+last;}
  return lines.length ? lines : ['YOUR NEXT BIG THING'];
}
function drawThumbnail(target=thumb,scale=1) {
  const [w,h]=setCanvasSize(target,state.thumbRatio,scale===2?1440:720),ctx=target.getContext('2d');
  ctx.clearRect(0,0,w,h);const min=Math.min(w,h);
  const palettes={sunshine:['#c7aeef','#eadbfd','#d5ff83','#1c1b21'],midnight:['#24252f','#42425b','#e8f68a','#ffffff'],lilac:['#e4cfdf','#e8eef7','#ff9da6','#332637']};
  const [bg,light,accent,ink]=palettes[state.thumbStyle];
  let gradient=ctx.createLinearGradient(0,0,w,h);gradient.addColorStop(0,bg);gradient.addColorStop(1,light);ctx.fillStyle=gradient;ctx.fillRect(0,0,w,h);
  if (thumbImage) {
    const zoom=Number($('thumb-zoom').value)/100;
    const s=Math.max(w/thumbImage.naturalWidth,h/thumbImage.naturalHeight)*zoom;
    const dw=thumbImage.naturalWidth*s,dh=thumbImage.naturalHeight*s;
    const maxX=Math.max(0,(dw-w)/2),maxY=Math.max(0,(dh-h)/2);
    const offsetX=(Number($('thumb-pan-x').value)/100)*maxX;
    const offsetY=(Number($('thumb-pan-y').value)/100)*maxY;
    ctx.drawImage(thumbImage,(w-dw)/2+offsetX,(h-dh)/2+offsetY,dw,dh);
    if ($('thumb-shadow').checked) {const overlay=ctx.createLinearGradient(0,0,w,0);overlay.addColorStop(0,'rgba(13,14,17,.86)');overlay.addColorStop(.72,'rgba(13,14,17,.36)');overlay.addColorStop(1,'rgba(13,14,17,.03)');ctx.fillStyle=overlay;ctx.fillRect(0,0,w,h);}
  } else {
    ctx.fillStyle=accent;ctx.beginPath();ctx.arc(w*.81,h*.33,min*.39,0,Math.PI*2);ctx.fill();
    ctx.lineWidth=min*.052;ctx.strokeStyle=state.thumbStyle==='midnight'?'#ae8aff':'#291f37';ctx.beginPath();ctx.arc(w*.83,h*.34,min*.28,0,Math.PI*2);ctx.stroke();
    ctx.save();ctx.translate(w*.78,h*.83);ctx.rotate(-.38);ctx.fillStyle=state.thumbStyle==='lilac'?'#bda9f0':'#ffb2b7';roundRect(ctx,-min*.18,-min*.15,min*.42,min*.32,min*.04,true);ctx.restore();
    ctx.fillStyle='rgba(255,255,255,.35)';for(let i=0;i<18;i++){const x=((i*101+83)%w),y=((i*179+29)%h);ctx.beginPath();ctx.arc(x,y,3,0,Math.PI*2);ctx.fill();}
  }
  const dark=!!thumbImage && $('thumb-shadow').checked;
  // Starter layouts genuinely alter how text is composed, not just the example copy.
  const preset=state.thumbPreset;
  if(!thumbImage && preset==='news') { ctx.fillStyle='#f34261';ctx.fillRect(0,h*.77,w,h*.23); }
  if(!thumbImage && preset==='minimal') {ctx.fillStyle='#fbf9e8';ctx.fillRect(w*.055,h*.19,w*.89,h*.64);}

  const textColor=dark?'#fff':ink;
  const pad=w*.07,desired=Math.min(w*.118,h*.185)*Number($('thumb-text-size').value)/100;
  let fontSize=desired,lines;
  do {ctx.font=`950 ${fontSize}px system-ui, sans-serif`;lines=multiline(ctx,$('thumb-title').value,w*(thumbImage?.78:.58),fontSize);fontSize*=.95;}
  while (lines.length>4 && fontSize>35);
  const lineHeight=fontSize*1.12;
  const titleY=(preset==='minimal'?h*.5:preset==='news'?h*.39:preset==='tutorial'?h*.43:h*.45)-(lines.length-1)*lineHeight*.24;
  ctx.textBaseline='alphabetic'; ctx.font=`900 ${fontSize}px system-ui, sans-serif`;
  ctx.shadowColor=dark?'rgba(0,0,0,.7)':'transparent';ctx.shadowBlur=dark?10:0;
  lines.forEach((line,i)=>{ctx.fillStyle=textColor;ctx.fillText(line.toUpperCase(),pad,titleY+i*lineHeight,w*(thumbImage?.84:.69));}); ctx.shadowBlur=0;
  const label=$('thumb-subtitle').value.trim();
  ctx.font=`850 ${Math.max(16,min*.026)}px system-ui,sans-serif`;ctx.fillStyle=dark?'#ccff9b':ink;ctx.fillText(label.toUpperCase(),pad,h*.15,w*.85);
  ctx.fillStyle=dark?'#c8ff8a':preset==='news'?'#fdfdfd':'#29272d';ctx.fillRect(pad,h*.86,w*.17,Math.max(7,h*.015));
  if(target===thumb)$('thumb-dimensions').textContent=`${w} × ${h}`;
}
function loadThumbPhoto(file){
  if(!file)return;
  if(!file.type.startsWith('image/')){toast('Please choose an image.');return;}
  if(file.size>40*1024*1024){toast('Please use an image smaller than 40 MB.');return;}
  const url=URL.createObjectURL(file);const img=new Image();
  img.onload=()=>{thumbImage=img;['thumb-pan-x','thumb-pan-y'].forEach(id=>{$(id).value=0;$(id+'-val').textContent='0%';});drawThumbnail();URL.revokeObjectURL(url);toast('Photo ready — processed only on your device.');};
  img.onerror=()=>{URL.revokeObjectURL(url);toast('Could not open this image.');};img.src=url;
}
$('thumb-file').addEventListener('change',(event)=>loadThumbPhoto(event.target.files?.[0]));
function enableDropzone(label,fileId,load){
  const file=$(fileId);
  label.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();file.click();}});
  for(const ev of ['dragenter','dragover'])label.addEventListener(ev,e=>{e.preventDefault();label.classList.add('drag-over');});
  for(const ev of ['dragleave','drop'])label.addEventListener(ev,e=>{e.preventDefault();label.classList.remove('drag-over');});
  label.addEventListener('drop',e=>load(e.dataTransfer?.files?.[0]));
}
enableDropzone(document.querySelector('label[for="thumb-file"]'),'thumb-file',loadThumbPhoto);
$('thumb-reset-photo').addEventListener('click',()=>{thumbImage=null;$('thumb-file').value='';$('thumb-zoom').value=100;$('thumb-zoom-val').textContent='100%';['thumb-pan-x','thumb-pan-y'].forEach(id=>{$(id).value=0;$(id+'-val').textContent='0%';});drawThumbnail();toast('Photo removed.');});
const presets={bold:['sunshine','MAKE IT POP!','YOUR NEXT BIG VIDEO'],tutorial:['lilac','HOW TO MAKE IT','A SIMPLE TUTORIAL'],news:['midnight','BIG NEWS TODAY','THE CREATOR UPDATE'],minimal:['sunshine','LESS IS MORE','NEW IDEAS. CLEAR FOCUS.']};
$$('[data-preset]').forEach(button=>button.addEventListener('click',()=>{
  state.thumbPreset=button.dataset.preset;
  $$('.preset').forEach(b=>{b.classList.toggle('active',b===button);b.setAttribute('aria-pressed',String(b===button));});
  const [palette,title,subtitle]=presets[state.thumbPreset];
  state.thumbStyle=palette;$('thumb-title').value=title;$('thumb-subtitle').value=subtitle;
  $$('[data-choice-group="thumb-style"] button').forEach(b=>{const active=b.dataset.value===palette;b.classList.toggle('active',active);b.setAttribute('aria-pressed',String(active));});
  drawThumbnail();
}));
['thumb-pan-x','thumb-pan-y'].forEach(id=>$(id).addEventListener('input',()=>{$(id+'-val').textContent=$(id).value+'%';drawThumbnail();}));
['thumb-title','thumb-subtitle','thumb-shadow'].forEach((id)=>$(id).addEventListener('input',drawThumbnail));
[['thumb-zoom','thumb-zoom-val'],['thumb-text-size','thumb-size-val']].forEach(([id,out])=>{$(id).addEventListener('input',()=>{$(out).textContent=$(id).value+'%';drawThumbnail();});});
$('thumb-download').addEventListener('click',()=>{
  const scale=Number($('thumb-resolution').value),output=document.createElement('canvas');
  drawThumbnail(output,scale);
  downloadCanvas(output,`craftlane-thumbnail-${output.width}x${output.height}.png`);
});

// ---------- Text Motion ----------
const motion=$('motion-canvas'),mctx=motion.getContext('2d');let exportingMotion=false;
const motionPalettes={electric:['#c8ff8a','#a0d977','#1d2921'],purple:['#c8b3ff','#9d7deb','#242038'],black:['#23262c','#383d43','#fcffdc'],coral:['#ff9d84','#f57585','#382325']};
const easeOut=(t)=>1-Math.pow(1-t,3);
const easeBack=(t)=>1+2.7*Math.pow(t-1,3)+1.7*Math.pow(t-1,2);
function drawMotionFrame(time=0) {
  const w=motion.width,h=motion.height,ctx=mctx,duration=Number($('motion-duration').value),p=clamp(time/duration,0,1);
  const [start,end,ink]=motionPalettes[state.motionBg], min=Math.min(w,h);
  const bg=ctx.createLinearGradient(0,0,w,h);bg.addColorStop(0,start);bg.addColorStop(1,end);ctx.fillStyle=bg;ctx.fillRect(0,0,w,h);
  ctx.save();ctx.translate(w*.79,h*.23);ctx.rotate(time*.11);ctx.lineWidth=min*.075;ctx.strokeStyle=state.motionBg==='black'?'#68617c':'rgba(25,28,27,.18)';ctx.beginPath();ctx.arc(0,0,min*.3,0,Math.PI*2);ctx.stroke();ctx.restore();
  ctx.fillStyle='rgba(255,255,255,.2)';ctx.beginPath();ctx.arc(w*.18,h*.74,min*.28,0,Math.PI*2);ctx.fill();
  for(let j=0;j<8;j++){ctx.fillStyle='rgba(0,0,0,.08)';ctx.fillRect(w*.07+j*w*.042,h*.91,w*.018,min*.048*(1+(j%3)));}
  const raw=$('motion-text').value.trim()||'MAKE IT HAPPEN';
  let text=raw.toUpperCase();const phase=easeOut(clamp(p/.29,0,1));let alpha=1, offsetY=0, scale=1;
  if(state.motionStyle==='type') text=text.slice(0,Math.max(0,Math.round(text.length*clamp(p/.55,0,1))));
  if(state.motionStyle==='slide'){offsetY=(1-phase)*h*.32;alpha=phase;}
  if(state.motionStyle==='pop'){scale=.3+easeBack(clamp(p/.26,0,1))*.7;alpha=phase;}
  if(state.motionStyle==='pulse'){scale=1+Math.sin(time*5)*.045;alpha=phase;}
  if(p>.88){alpha*=clamp((1-p)/.12,0,1);}
  const fontSize=Math.min(w*.122,h*.115);ctx.font=`1000 ${fontSize}px system-ui,sans-serif`;
  const lines=text?multiline(ctx,text,w*.83,fontSize,5):[],lineH=fontSize*1.12;
  ctx.save();ctx.globalAlpha=clamp(alpha,0,1);ctx.translate(w/2,h*.52+offsetY);ctx.scale(scale,scale);ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillStyle=ink;
  lines.forEach((line,i)=>ctx.fillText(line,0,(i-(lines.length-1)/2)*lineH,w*.88));ctx.restore();
  const sub=$('motion-subtext').value.trim();ctx.fillStyle=ink;ctx.globalAlpha=.65*alpha;ctx.textAlign='center';ctx.font=`750 ${Math.max(14,min*.024)}px system-ui,sans-serif`;ctx.fillText(sub.toUpperCase(),w/2,h*.86,w*.85);ctx.globalAlpha=1;
  // No branding or watermarks on exported content.

}
function motionLoop(now){if(state.tool==='motion'&&!exportingMotion){drawMotionFrame((now/1000)%Number($('motion-duration').value));}requestAnimationFrame(motionLoop);}
['motion-text','motion-subtext'].forEach((id)=>$(id).addEventListener('input',()=>drawMotionFrame(.85)));
$('motion-duration').addEventListener('input',()=>{$('motion-duration-val').textContent=$('motion-duration').value+'s';});
$('motion-png').addEventListener('click',()=>{drawMotionFrame(1.3);downloadCanvas(motion,'craftlane-text-motion.png');});
$('motion-export').addEventListener('click',async()=>{
  if(exportingMotion)return;
  if(!motion.captureStream||!window.MediaRecorder){toast('Your browser does not support canvas video recording. Try the PNG button.');return;}
  const mime=chooseMime();if(!mime){toast('WebM export is unavailable in this browser. Try Chrome on desktop or Android.');return;}
  exportingMotion=true;const btn=$('motion-export');btn.disabled=true;$('motion-status').textContent='Rendering your video in real time…';
  try {
    const chunks=[],stream=motion.captureStream(30);
    const rec=new MediaRecorder(stream,{mimeType:mime,videoBitsPerSecond:2500000});
    const completed=new Promise((resolve,reject)=>{
      rec.ondataavailable=(event)=>{if(event.data.size)chunks.push(event.data);};
      rec.onerror=()=>reject(new Error('Video recording failed.'));
      rec.onstop=()=>{stream.getTracks().forEach((track)=>track.stop());resolve(new Blob(chunks,{type:'video/webm'}));};
    });
    rec.start(250);const duration=Number($('motion-duration').value)*1000,start=performance.now();
    await new Promise((resolve)=>{const step=(now)=>{const elapsed=now-start;drawMotionFrame(Math.min(elapsed,duration)/1000);
      if(elapsed<duration){requestAnimationFrame(step);}else{rec.stop();resolve();}};requestAnimationFrame(step);});
    const blob=await completed;saveBlob(blob,'craftlane-text-motion.webm');$('motion-status').textContent='Your WebM animation is ready.';toast('Animation exported!');
  }catch(err){$('motion-status').textContent=readableError(err);toast('Video export was unsuccessful. Try saving a still.');}
  finally{exportingMotion=false;btn.disabled=false;}
});

// ---------- Video Resizer ----------
const video=$('resize-video'),resize=$('resize-canvas'),rctx=resize.getContext('2d');
let videoUrl=null,videoReady=false,exportingVideo=false,audioCtx=null,audioSource=null,audioDestination=null,speakerGain=null;
function drawVideoPreview(){
  const w=resize.width,h=resize.height,ctx=rctx;
  ctx.clearRect(0,0,w,h);ctx.fillStyle=$('resize-bg').value;ctx.fillRect(0,0,w,h);
  if(videoReady&&video.videoWidth&&video.videoHeight&&video.readyState>=2){
    const fit=state.resizeFit==='cover'?'max':'min';const scale=(fit==='max'?Math.max(w/video.videoWidth,h/video.videoHeight):Math.min(w/video.videoWidth,h/video.videoHeight))*(Number($('resize-zoom').value)/100);
    const dw=video.videoWidth*scale,dh=video.videoHeight*scale;ctx.drawImage(video,(w-dw)/2,(h-dh)/2,dw,dh);
  } else {
    const g=ctx.createLinearGradient(0,0,w,h);g.addColorStop(0,'#ddd5f4');g.addColorStop(1,'#a4c6c0');ctx.fillStyle=g;ctx.fillRect(0,0,w,h);
    ctx.fillStyle='#ccff96';ctx.beginPath();ctx.arc(w*.74,h*.28,w*.29,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#212421';ctx.textAlign='center';ctx.font=`900 ${w*.075}px system-ui,sans-serif`;ctx.fillText('YOUR VIDEO',w/2,h*.49,w*.87);ctx.font=`800 ${w*.049}px system-ui,sans-serif`;ctx.fillText('GOES HERE ↗',w/2,h*.56,w*.8);
    ctx.font=`650 ${Math.max(11,w*.022)}px system-ui,sans-serif`;ctx.fillText('CHOOSE A CLIP TO BEGIN',w/2,h*.88,w*.9);
  }
  $('resize-dimensions').textContent=`${w} × ${h}`;
}
function videoLoop(){if(!video.paused&&!video.ended){drawVideoPreview();requestAnimationFrame(videoLoop);} }
video.addEventListener('play',videoLoop);
video.addEventListener('seeked',drawVideoPreview);video.addEventListener('loadeddata',drawVideoPreview);
video.addEventListener('timeupdate',()=>{if(videoReady&&!exportingVideo){
  const {end}=getTrim();if(!video.paused&&video.currentTime>=end-.04)video.pause();
  $('resize-time').textContent=`${video.currentTime.toFixed(1)}s / ${video.duration.toFixed(1)}s · Live preview`;
}});
function loadVideoFile(file){
  if(!file)return;
  if(!file.type.startsWith('video/')&&!/\.(mp4|mov|webm|m4v|ogg)$/i.test(file.name)){toast('Please choose a video file.');return;}
  if(file.size>1024*1024*1024){toast('Please use a clip smaller than 1 GB on your device.');return;}
  video.pause();videoReady=false; $('resize-export').disabled=true;
  if(videoUrl)URL.revokeObjectURL(videoUrl);videoUrl=URL.createObjectURL(file);video.src=videoUrl;video.hidden=false;video.load();
  $('video-file-info').textContent=file.name+' · '+(file.size/1024/1024).toFixed(1)+' MB';
  video.onloadedmetadata=()=>{videoReady=true;$('resize-export').disabled=false;
    $('trim-start').value=0;$('trim-end').value=video.duration.toFixed(1);
    $('trim-start').max=Math.max(0,video.duration-.1).toFixed(1);$('trim-end').max=video.duration.toFixed(1);
    $('trim-box').hidden=false;updateTrim();drawVideoPreview();toast('Video loaded. Processing stays on your device.');};
  video.onerror=()=>{videoReady=false;$('resize-export').disabled=true;$('trim-box').hidden=true;toast('This browser cannot play that video codec. Try MP4 or WebM.');};
}
$('video-file').addEventListener('change',e=>loadVideoFile(e.target.files?.[0]));
enableDropzone(document.querySelector('label[for="video-file"]'),'video-file',loadVideoFile);
function getTrim(){const duration=videoReady&&Number.isFinite(video.duration)?video.duration:0;
  const start=clamp(Number($('trim-start').value)||0,0,Math.max(0,duration-.1));
  const end=clamp(Number($('trim-end').value)||duration,start+.1,duration);
  return {start,end,duration:Math.max(.1,end-start)};
}
function updateTrim(){if(!videoReady)return;
  const {start,end,duration}=getTrim();$('trim-length').textContent=`${duration.toFixed(1)}s selected`;
  $('trim-start').setAttribute('aria-valuemax',String(end));
  if(!Number.isFinite(start)||!Number.isFinite(end)||end<=start)$('resize-export').disabled=true;
  else if(!exportingVideo)$('resize-export').disabled=false;
}
['trim-start','trim-end'].forEach(id=>$(id).addEventListener('change',()=>{if(!videoReady)return;
  let {start,end}=getTrim();$('trim-start').value=start.toFixed(1);$('trim-end').value=end.toFixed(1);updateTrim();video.currentTime=start;
}));
$('trim-preview').addEventListener('click',async()=>{if(!videoReady||exportingVideo)return;const {start}=getTrim();video.pause();video.currentTime=start;
  try{await video.play();}catch{toast('Press play on the clip to preview.');}
});
$('resize-zoom').addEventListener('input',()=>{$('resize-zoom-val').textContent=$('resize-zoom').value+'%';drawVideoPreview();});
$('resize-bg').addEventListener('change',drawVideoPreview);
async function ensureAudio() {
  const ctor=window.AudioContext||window.webkitAudioContext;if(!ctor)return null;
  if(!audioCtx){audioCtx=new ctor();audioSource=audioCtx.createMediaElementSource(video);audioDestination=audioCtx.createMediaStreamDestination();speakerGain=audioCtx.createGain();audioSource.connect(audioDestination);audioSource.connect(speakerGain);speakerGain.connect(audioCtx.destination);}
  await audioCtx.resume();return audioDestination.stream.getAudioTracks()[0]||null;
}
let videoExportCancel=null;
$('resize-cancel').addEventListener('click',()=>{if(videoExportCancel)videoExportCancel();});
$('resize-export').addEventListener('click',async()=>{
  if(!videoReady||exportingVideo)return;
  if(!window.MediaRecorder||!resize.captureStream){toast('Video export requires Chrome or another compatible browser.');return;}
  const mime=chooseMime(true)||chooseMime();if(!mime){toast('WebM recording is unavailable in this browser.');return;}
  const {start,end,duration}=getTrim();
  if(end-start<.1){toast('Select a clip longer than 0.1 seconds.');return;}
  const button=$('resize-export'),cancel=$('resize-cancel'),bar=$('resize-progress');
  exportingVideo=true;button.disabled=true;cancel.hidden=false;bar.hidden=false;bar.value=0;video.controls=false;
  let rec=null,canvasStream=null,tick=null,backup=null,onComplete=null,cancelled=false,recorderFinished=null;
  try {
    video.pause();video.currentTime=start;
    // Seek must finish before recording to prevent black initial frames.
    if(video.seeking)await new Promise((resolve,reject)=>{const timeout=setTimeout(()=>reject(new Error('Video seeking timed out.')),10000);
      video.addEventListener('seeked',()=>{clearTimeout(timeout);resolve();},{once:true});});
    let audioTrack=null;
    try{audioTrack=await ensureAudio();if(speakerGain)speakerGain.gain.value=0;}
    catch(err){console.warn('Audio capture unavailable:',err);$('resize-status').textContent='Audio unavailable. Exporting the video picture.';}
    canvasStream=resize.captureStream(30);if(audioTrack)canvasStream.addTrack(audioTrack);
    const chunks=[];rec=new MediaRecorder(canvasStream,{mimeType:mime,videoBitsPerSecond:2800000});
    recorderFinished=new Promise((resolve,reject)=>{
      rec.ondataavailable=e=>{if(e.data.size)chunks.push(e.data);};
      rec.onerror=()=>reject(new Error('Browser video recording failed.'));
      rec.onstop=()=>resolve(new Blob(chunks,{type:'video/webm'}));
    });
    const stop=()=>{if(rec&&rec.state!=='inactive')rec.stop();};
    videoExportCancel=()=>{cancelled=true;stop();video.pause();$('resize-status').textContent='Export cancelled.';};
    onComplete=()=>stop();video.addEventListener('ended',onComplete);
    rec.start(250);await video.play();
    tick=setInterval(()=>{
      const progress=clamp((video.currentTime-start)/duration*100,0,100);
      bar.value=progress;$('resize-status').textContent=`Processing ${Math.round(progress)}% — keep this tab open.`;
      if(video.currentTime>=end-.055)stop();
    },60);
    backup=setTimeout(stop,(duration+8)*1000);
    const result=await recorderFinished;
    if(!cancelled&&result.size){bar.value=100;saveBlob(result,'craftlane-trimmed-video.webm');$('resize-status').textContent=`Done! Exported ${duration.toFixed(1)} seconds.`;toast('Video exported successfully.');}
    else if(!cancelled){$('resize-status').textContent='No frames were recorded. Try a different clip.';}
  }catch(err){$('resize-status').textContent=readableError(err);toast('Could not export this clip. Try a short MP4 in Chrome.');if(rec?.state==='recording')rec.stop();
    if(recorderFinished)await recorderFinished.catch(()=>{});
  }finally{
    if(tick)clearInterval(tick);if(backup)clearTimeout(backup);
    if(onComplete)video.removeEventListener('ended',onComplete);
    video.pause();video.controls=true;if(speakerGain)speakerGain.gain.value=1;
    if(canvasStream)canvasStream.getTracks().filter(t=>t.kind==='video').forEach(t=>t.stop());
    videoExportCancel=null;exportingVideo=false;button.disabled=false;cancel.hidden=true;
    if(cancelled)bar.hidden=true;drawVideoPreview();
  }
});

// ---------- Caption Studio ----------
function captionLines(){
  let text=$('caption-input').value.replace(/\s+/g,' ').trim();
  if($('caption-fillers').checked)text=text.replace(/\b(?:um+|uh+|erm+|ah+)\b[,.]?\s*/gi,'').replace(/\s+/g,' ').trim();
  if(!text)return [];
  const words=text.split(' '),per=Number($('caption-words').value),lines=[];
  for(let i=0;i<words.length;i+=per){let line=words.slice(i,i+per).join(' ');
    if(state.captionStyle==='punchy')line=line.toUpperCase();
    else if(state.captionStyle==='sentence')line=line.replace(/^\w/,c=>c.toUpperCase());
    lines.push(line);
  }return lines;
}
function renderCaptions(){const lines=captionLines(),out=$('caption-output');out.textContent='';
  if(!lines.length){out.textContent='Your captions will appear here…';$('caption-stats').textContent='0 words';return;}
  lines.forEach((line,i)=>{const span=document.createElement('span');if(i===0)span.className='caption-accent';span.textContent=line;out.appendChild(span);if(i<lines.length-1)out.appendChild(document.createElement('br'));});
  $('caption-stats').textContent=$('caption-input').value.trim().split(/\s+/).filter(Boolean).length+' words';
}
function srtTimestamp(sec){const ms=Math.max(0,Math.round(sec*1000)),hours=Math.floor(ms/3600000),mins=Math.floor(ms%3600000/60000),seconds=Math.floor(ms%60000/1000),fraction=ms%1000;return [hours,mins,seconds].map(n=>String(n).padStart(2,'0')).join(':')+','+String(fraction).padStart(3,'0');}
function buildSrt(){const lines=captionLines(),length=Math.max(1,Number($('caption-duration').value)||30),groups=[];
  for(let i=0;i<lines.length;i+=2)groups.push(lines.slice(i,i+2));
  const weights=groups.map(g=>g.join(' ').split(/\s+/).length),total=weights.reduce((a,b)=>a+b,0)||1;let elapsed=0;
  return groups.map((g,i)=>{const start=elapsed;elapsed+=(weights[i]/total)*length;const end=i===groups.length-1?length:elapsed;return `${i+1}\n${srtTimestamp(start)} --> ${srtTimestamp(end)}\n${g.join('\n')}\n`;}).join('\n');
}
['caption-input','caption-duration','caption-fillers'].forEach(id=>$(id).addEventListener('input',renderCaptions));
$('caption-words').addEventListener('input',()=>{$('caption-words-val').textContent=$('caption-words').value;renderCaptions();});
$('caption-copy').addEventListener('click',()=>copyText(captionLines().join('\n')));
$('caption-srt').addEventListener('click',()=>{const content=buildSrt();if(!content.trim()){toast('Add a transcript first.');return;}saveBlob(new Blob([content],{type:'text/plain;charset=utf-8'}),'craftlane-captions.srt');});
$('caption-vtt').addEventListener('click',()=>{const srt=buildSrt();if(!srt.trim()){toast('Add a transcript first.');return;}
  const vtt='WEBVTT\n\n'+srt.replace(/(^|\n)(\d+)\n(?=\d\d:\d\d:)/g,'$1').replace(/(\d\d:\d\d:\d\d),(\d{3})/g,'$1.$2');
  saveBlob(new Blob([vtt],{type:'text/vtt;charset=utf-8'}),'craftlane-captions.vtt');
});

// ---------- Hook Lab ----------
let hookIteration=0;
function generateHooks(){
  const topic=$('hooks-topic').value.trim().replace(/[.!?]+$/,'')||'your next idea';
  const audience=$('hooks-audience').value.trim()||'beginners';
  const options={
    curious:[`What nobody tells you about ${topic}`,`I tried ${topic} so you don't have to guess`,`The surprising truth about ${topic}`,`Can you actually get better at ${topic}?`,`Here's what changed when I focused on ${topic}`,`Why ${audience} are getting ${topic} wrong`,`Is ${topic} actually worth your time?`,`I tested three approaches to ${topic}`,`The one thing I misunderstood about ${topic}`,`What happens when you try ${topic} for a week?`,`A small change that improved my approach to ${topic}`,`I asked myself this question about ${topic}`],
    bold:[`Stop overthinking ${topic}`,`The biggest mistake people make with ${topic}`,`This changes everything about ${topic}`,`You're doing ${topic} the hard way`,`I wish I knew this before ${topic}`,`The no-nonsense guide to ${topic}`,`Don't start ${topic} until you see this`,`Forget everything you assumed about ${topic}`,`Your ${topic} routine might be holding you back`,`It's time to rethink ${topic}`,`The truth: ${topic} doesn't need to be complicated`,`Here's the shortcut I use for ${topic}`],
    helpful:[`3 simple ways to get started with ${topic}`,`A beginner-friendly guide to ${topic}`,`How to improve at ${topic} in small steps`,`Save this checklist for ${topic}`,`The easiest way for ${audience} to try ${topic}`,`Everything you need to know about ${topic}`,`5 questions to ask before ${topic}`,`A practical step-by-step plan for ${topic}`,`Start with these basics of ${topic}`,`The simple ${topic} checklist I keep using`,`What ${audience} should know about ${topic}`,`How to make ${topic} easier this week`]
  };
  const items=options[state.hooksTone];const rotated=Array.from({length:6},(_,i)=>items[(i+hookIteration*3)%items.length]);const wrap=$('hooks-results');wrap.textContent='';
  rotated.forEach((line,i)=>{const b=document.createElement('button');b.className='hook-result';b.title='Copy this hook';
    const num=document.createElement('span');num.className='hook-index';num.textContent=String(i+1).padStart(2,'0');
    const copy=document.createElement('span');copy.className='hook-text';copy.textContent=line;
    const arrow=document.createElement('span');arrow.className='hook-copy';arrow.textContent='⧉';
    b.append(num,copy,arrow);b.addEventListener('click',()=>copyText(line));wrap.appendChild(b);
  });
}
['hooks-topic','hooks-audience'].forEach(id=>$(id).addEventListener('input',()=>{hookIteration=0;generateHooks();}));
$('hooks-generate').addEventListener('click',()=>{hookIteration=(hookIteration+1)%6;generateHooks();toast('Ideas refreshed.');});
function allHooks(){return $$('.hook-text',$('hooks-results')).map((e,i)=>`${i+1}. ${e.textContent}`).join('\n');}
$('hooks-copy-all').addEventListener('click',()=>copyText(allHooks()));
$('hooks-txt').addEventListener('click',()=>saveBlob(new Blob([allHooks()],{type:'text/plain;charset=utf-8'}),'craftlane-hook-ideas.txt'));

wireUI();drawThumbnail();drawVideoPreview();renderCaptions();generateHooks();setCanvasSize(motion,state.motionRatio,540);drawMotionFrame(.8);requestAnimationFrame(motionLoop);
if ('serviceWorker' in navigator && (location.protocol==='https:' || location.hostname==='localhost' || location.hostname==='127.0.0.1')) {
  window.addEventListener('load',()=>navigator.serviceWorker.register('./sw.js').catch(()=>{}));
}