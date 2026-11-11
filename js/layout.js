(()=>{const p=document.body.dataset.page,L=[['home','./','Beranda'],['tabel','tabel.html','Daftar Tabel'],['strategis','strategis.html','Indikator'],['panduan','panduan.html','Panduan'],['backup','backup.html','Backup Publikasi']];
document.body.insertAdjacentHTML('afterbegin',`<header><div class="bar"><img src="assets/icon-192.png" alt=""><b>ATHENA</b><button class="th" id="th"></button></div><nav>${L.map(l=>`<a href="${l[1]}"${l[0]==p?' class="on"':''}>${l[2]}</a>`).join('')}</nav></header>`);
const T=['auto','light','dark'],N={auto:'◐ Otomatis',light:'☀ Terang',dark:'☾ Gelap'},th=document.getElementById('th'),cur=()=>localStorage.t||'auto',lab=()=>th.textContent=N[cur()];lab();
th.onclick=()=>{setTheme(T[(T.indexOf(cur())+1)%3]);lab()};
if('serviceWorker' in navigator)addEventListener('load',()=>navigator.serviceWorker.register('sw.js'))})();
