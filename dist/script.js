const menu=document.querySelector('.menu');
const nav=document.querySelector('#nav');
function closeMenu(){nav.classList.remove('open');menu.setAttribute('aria-expanded','false');}
menu.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));nav.classList.toggle('open',open);});
nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',closeMenu));
document.addEventListener('keydown',e=>{if(e.key==='Escape' && nav.classList.contains('open')){closeMenu();menu.focus();}});
window.matchMedia('(min-width:901px)').addEventListener('change',closeMenu);
document.querySelector('#year').textContent=new Date().getFullYear();

// Reveal the selected service before navigating to its details.
document.querySelectorAll('.care-strip a[href^="#"]').forEach(link=>link.addEventListener('click',()=>{const panel=document.querySelector(link.getAttribute('href'));if(panel?.tagName==='DETAILS')panel.open=true;}));
document.querySelectorAll('.service-list details').forEach(panel=>panel.addEventListener('toggle',()=>{panel.querySelector('.view-label').textContent=panel.open?'Close details':'View details';}));
