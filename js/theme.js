(()=>{const r=document.documentElement,m=matchMedia('(prefers-color-scheme:dark)');
window.setTheme=p=>{let t='auto';try{if(p)localStorage.t=p;t=localStorage.t||'auto'}catch(e){}
const d=t=='dark'||(t=='auto'&&m.matches);r.dataset.t=d?'dark':'light';
const c=document.querySelector('meta[name=theme-color]');if(c)c.content=d?'#08111a':'#12252f';dispatchEvent(new Event('themechange'))};
m.onchange=()=>setTheme();setTheme()})();
