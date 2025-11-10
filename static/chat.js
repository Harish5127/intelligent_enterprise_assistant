const chat = document.getElementById('chat');
const entry = document.getElementById('entry');
const send = document.getElementById('send');
const fileEl = document.getElementById('file');
const upload = document.getElementById('upload');
function append(text, cls='bot'){ const d=document.createElement('div'); d.className=cls; d.textContent=text; chat.appendChild(d); chat.scrollTop=chat.scrollHeight; }
send.addEventListener('click', async ()=>{
  const msg = entry.value.trim(); if(!msg) return;
  append('You: '+msg,'user'); entry.value='';
  const res = await fetch('/chat',{method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({message: msg})});
  const j = await res.json();
  if(j.ok){ append('Assistant: '+j.reply,'bot'); } else { append('Error: '+ (j.error||'unknown'),'bot'); }
});
entry.addEventListener('keypress', (e)=>{ if(e.key==='Enter') send.click(); });
upload.addEventListener('click', async ()=>{
  const f = fileEl.files[0]; if(!f){ alert('Select a file'); return; }
  const fd = new FormData(); fd.append('file', f);
  const res = await fetch('/upload', {method:'POST', body: fd});
  const j = await res.json();
  if(j.ok){ document.getElementById('docresult').innerText = 'Summary:\n'+j.summary + '\n\nKeywords:\n' + j.keywords.join(', '); } else { alert('Upload error'); }
});
