(()=>{const p=document.body.dataset.page,L=[['home','./','Beranda'],['tabel','tabel.html','Daftar Tabel'],['backup','backup.html','Backup Publikasi']];
document.body.insertAdjacentHTML('afterbegin',`<header><div class="bar"><img src="assets/icon-192.png" alt=""><b>ATHENA</b></div><nav>${L.map(l=>`<a href="${l[1]}"${l[0]==p?' class="on"':''}>${l[2]}</a>`).join('')}</nav></header>`);
if('serviceWorker' in navigator)addEventListener('load',()=>navigator.serviceWorker.register('sw.js'))})();
