<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>tweet_forge — README</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500&display=swap" rel="stylesheet">
<style>
  html,body{margin:0;padding:40px 16px;background:#070a09;}
</style>
</head>
<body>
<style>
  :root{
    --bg:#0d1210;
    --panel:#141a17;
    --line:#26312c;
    --text:#dce8e0;
    --dim:#7f9488;
    --accent:#5ee6a8;
    --accent-dim:#2f6b52;
    --code-bg:#0a0e0c;
  }
  .tf-wrap{
    background:var(--bg);
    color:var(--text);
    font-family:'IBM Plex Sans',system-ui,sans-serif;
    padding:0;
    border-radius:10px;
    border:1px solid var(--line);
    overflow:hidden;
    max-width:760px;
    margin:0 auto;
  }
  .tf-header{
    padding:28px 32px 22px;
    border-bottom:1px solid var(--line);
    background:linear-gradient(180deg, rgba(94,230,168,0.06), transparent);
  }
  .tf-title{
    font-family:'IBM Plex Mono',monospace;
    font-size:26px;
    font-weight:600;
    letter-spacing:-0.01em;
    margin:0 0 6px;
    color:var(--text);
  }
  .tf-title span{color:var(--accent);}
  .tf-sub{
    color:var(--dim);
    font-size:14px;
    margin:0;
    line-height:1.5;
  }
  .tf-section{
    border-bottom:1px solid var(--line);
  }
  .tf-section:last-child{border-bottom:none;}
  .tf-toggle{
    width:100%;
    display:flex;
    align-items:center;
    justify-content:space-between;
    background:transparent;
    border:none;
    color:var(--text);
    padding:16px 32px;
    font-family:'IBM Plex Mono',monospace;
    font-size:14px;
    letter-spacing:0.02em;
    text-transform:uppercase;
    cursor:pointer;
    text-align:left;
  }
  .tf-toggle:hover{background:rgba(94,230,168,0.04);}
  .tf-toggle .num{color:var(--accent-dim); margin-right:10px;}
  .tf-chevron{
    color:var(--dim);
    transition:transform 0.25s ease;
    font-size:12px;
  }
  .tf-toggle[aria-expanded="true"] .tf-chevron{ transform:rotate(90deg); color:var(--accent);}
  .tf-body{
    max-height:0;
    overflow:hidden;
    transition:max-height 0.3s ease;
    padding:0 32px;
  }
  .tf-body.open{
    max-height:1200px;
    padding:0 32px 24px;
  }
  .tf-body p{
    font-size:14.5px;
    line-height:1.65;
    color:var(--text);
    margin:0 0 12px;
  }
  .tf-body p:last-child{margin-bottom:0;}
  .tf-body code, .tf-body p code{
    background:var(--code-bg);
    border:1px solid var(--line);
    padding:1px 6px;
    border-radius:4px;
    font-family:'IBM Plex Mono',monospace;
    font-size:13px;
    color:var(--accent);
  }
  .tf-codeblock{
    position:relative;
    background:var(--code-bg);
    border:1px solid var(--line);
    border-radius:8px;
    margin:10px 0 14px;
  }
  .tf-codeblock pre{
    margin:0;
    padding:14px 16px;
    font-family:'IBM Plex Mono',monospace;
    font-size:13px;
    line-height:1.6;
    color:#b9f5d5;
    overflow-x:auto;
  }
  .tf-copy{
    position:absolute;
    top:8px;
    right:8px;
    background:var(--panel);
    border:1px solid var(--line);
    color:var(--dim);
    font-family:'IBM Plex Mono',monospace;
    font-size:11px;
    padding:3px 8px;
    border-radius:5px;
    cursor:pointer;
  }
  .tf-copy:hover{color:var(--accent); border-color:var(--accent-dim);}
  .tf-diagram{
    background:var(--code-bg);
    border:1px solid var(--line);
    border-radius:8px;
    padding:20px 10px;
    margin:10px 0 14px;
  }
  .tf-node{
    font-family:'IBM Plex Mono',monospace;
    font-size:12px;
    fill:var(--text);
  }
  .tf-nodebox{
    fill:var(--panel);
    stroke:var(--line);
    stroke-width:1;
  }
  .tf-nodebox.active-node{
    stroke:var(--accent);
  }
  .tf-edge{
    stroke:var(--dim);
    stroke-width:1.4;
    fill:none;
  }
  .tf-edge-label{
    font-family:'IBM Plex Mono',monospace;
    font-size:10px;
    fill:var(--dim);
  }
  .tf-pulse{
    fill:var(--accent);
  }
  .tf-footer{
    padding:16px 32px 22px;
    font-family:'IBM Plex Mono',monospace;
    font-size:11.5px;
    color:var(--dim);
    display:flex;
    justify-content:space-between;
  }
</style>

<div class="tf-wrap">
  <div class="tf-header">
    <p class="tf-title">tweet<span>_</span>forge</p>
    <p class="tf-sub">A LangGraph loop that writes a tweet, evaluates it like a ruthless editor, and rewrites it until it earns approval — or runs out of tries.</p>
  </div>

  <div id="tf-sections"></div>

  <div class="tf-footer">
    <span>langgraph · groq · gpt-oss-120b</span>
    <span id="tf-clock">iteration cap: 5</span>
  </div>
</div>

<script>
(function(){
  const sections = [
    {
      title: "What it does",
      body: [
        "The whole thing is a loop between three LLM personas. A generator drafts a tweet from whatever topic you give it, writing like a top-tier X creator: witty, concise, one strong idea, no clichés, no AI-sounding filler.",
        "That draft goes to an evaluator, which acts like a ruthless editor. It assumes every tweet starts at zero and has to earn its approval, checking things like originality, hook strength, clarity, and whether the ending actually lands. It auto-rejects anything too long, generic, AI-sounding, or leaning on hashtags and clickbait.",
        "If it's not approved, the feedback goes to an optimizer, which rewrites the tweet accordingly, and the new draft goes straight back to the evaluator. This keeps cycling until the tweet is approved or <code>max_iteration</code> is hit, whichever comes first."
      ]
    },
    {
      title: "The graph",
      body: [
        "It's a simple loop: <code>generate → evaluate</code>, then either straight to <code>END</code> if approved, or over to <code>optimize → evaluate</code> again if not. Just a conditional edge deciding whether to exit or keep looping."
      ],
      diagram: true
    },
    {
      title: "State",
      body: [
        "State is tracked as a single dict carrying the topic, current tweet, current evaluation and feedback, iteration count, and the iteration cap.",
        "Two fields, <code>tweet_history</code> and <code>feedback_history</code>, use LangGraph's <code>operator.add</code> reducer, so every draft and every round of feedback accumulates across iterations instead of getting overwritten. Handy for tracing how a tweet evolved rather than just seeing the final result."
      ]
    },
    {
      title: "Models",
      body: [
        "All three roles currently run on <code>openai/gpt-oss-120b</code> through Groq. Nothing stops you from putting a different model on each node though, say a cheaper one for generation and a sharper one for evaluation, since that's the node doing the actual gatekeeping."
      ]
    },
    {
      title: "Setup",
      body: ["Install the dependencies, then drop your Groq key into a <code>.env</code> file."],
      code: [
        {lang:"bash", text:"pip install langgraph langchain-groq python-dotenv pydantic"},
        {lang:"env", text:"GROQ_API_KEY=your_key_here"}
      ]
    },
    {
      title: "Usage",
      body: ["Run the script, give it a topic, and it iterates (5 rounds max by default) until it lands on something worth posting, printing the final tweet along with the evaluator's verdict and feedback."],
      code: [
        {lang:"bash", text:"python tweet_forge.py"}
      ]
    },
    {
      title: "Rough edges",
      body: [
        "There's no retry or error handling around the Groq calls, so a rate limit or dropped connection just crashes the run.",
        "The evaluator depends on structured output support, so swapping in a different model means checking it still works with <code>.with_structured_output()</code>.",
        "The 280-character limit is only enforced through the prompt — nothing in code actually stops a model from ignoring it."
      ]
    }
  ];

  const container = document.getElementById('tf-sections');

  const diagramSVG = `
    <div class="tf-diagram">
      <svg viewBox="0 0 680 190" width="100%" height="190">
        <defs>
          <marker id="tf-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
            <path d="M0,0 L10,5 L0,10 z" fill="#7f9488"/>
          </marker>
        </defs>

        <rect class="tf-nodebox" x="10" y="80" width="70" height="32" rx="6"/>
        <text class="tf-node" x="45" y="100" text-anchor="middle">START</text>

        <rect id="node-generate" class="tf-nodebox" x="130" y="80" width="100" height="32" rx="6"/>
        <text class="tf-node" x="180" y="100" text-anchor="middle">generate</text>

        <rect id="node-evaluate" class="tf-nodebox" x="290" y="80" width="100" height="32" rx="6"/>
        <text class="tf-node" x="340" y="100" text-anchor="middle">evaluate</text>

        <rect class="tf-nodebox" x="590" y="80" width="70" height="32" rx="6"/>
        <text class="tf-node" x="625" y="100" text-anchor="middle">END</text>

        <rect id="node-optimize" class="tf-nodebox" x="290" y="150" width="100" height="32" rx="6"/>
        <text class="tf-node" x="340" y="170" text-anchor="middle">optimize</text>

        <path class="tf-edge" d="M80,96 L130,96" marker-end="url(#tf-arrow)"/>
        <path class="tf-edge" d="M230,96 L290,96" marker-end="url(#tf-arrow)"/>
        <path class="tf-edge" d="M390,96 L590,96" marker-end="url(#tf-arrow)"/>
        <text class="tf-edge-label" x="480" y="88" text-anchor="middle">approved</text>

        <path class="tf-edge" d="M340,112 L340,150" marker-end="url(#tf-arrow)"/>
        <text class="tf-edge-label" x="345" y="132">needs_improvement</text>

        <path class="tf-edge" d="M290,166 C 250,166 250,96 290,96" marker-end="url(#tf-arrow)"/>

        <circle id="tf-dot" class="tf-pulse" r="4" cx="80" cy="96"/>
      </svg>
    </div>
  `;

  sections.forEach((s, i) => {
    const wrap = document.createElement('div');
    wrap.className = 'tf-section';

    let bodyHTML = s.body.map(p => `<p>${p}</p>`).join('');

    if (s.code) {
      s.code.forEach((c, ci) => {
        bodyHTML += `
          <div class="tf-codeblock">
            <button class="tf-copy" data-code="sec${i}-${ci}">copy</button>
            <pre id="sec${i}-${ci}">${c.text}</pre>
          </div>`;
      });
    }

    if (s.diagram) {
      bodyHTML += diagramSVG;
    }

    wrap.innerHTML = `
      <button class="tf-toggle" aria-expanded="${i===0?'true':'false'}">
        <span><span class="num">0${i+1}</span>${s.title}</span>
        <span class="tf-chevron">›</span>
      </button>
      <div class="tf-body ${i===0?'open':''}">${bodyHTML}</div>
    `;
    container.appendChild(wrap);
  });

  container.addEventListener('click', (e) => {
    if (e.target.classList.contains('tf-toggle') || e.target.closest('.tf-toggle')) {
      const btn = e.target.closest('.tf-toggle');
      const body = btn.nextElementSibling;
      const isOpen = body.classList.contains('open');
      body.classList.toggle('open', !isOpen);
      btn.setAttribute('aria-expanded', String(!isOpen));
    }
    if (e.target.classList.contains('tf-copy')) {
      const id = e.target.getAttribute('data-code');
      const text = document.getElementById(id).innerText;
      navigator.clipboard.writeText(text).then(() => {
        const orig = e.target.innerText;
        e.target.innerText = 'copied';
        setTimeout(()=> e.target.innerText = orig, 1200);
      });
    }
  });

  // animate the loop dot along the graph path once the "The graph" section is open
  const path1 = "M80,96 L130,96 L230,96 L290,96 L340,96";
  const dot = document.getElementById('tf-dot');
  if (dot) {
    let t = 0;
    const pts = [[80,96],[130,96],[230,96],[290,96],[340,96],[340,150],[290,150],[290,96],[340,96],[390,96],[590,96]];
    function animate(){
      t += 0.006;
      if (t > 1) t = 0;
      const seg = t * (pts.length - 1);
      const idx = Math.floor(seg);
      const frac = seg - idx;
      const a = pts[idx], b = pts[Math.min(idx+1, pts.length-1)];
      if(a && b){
        dot.setAttribute('cx', a[0] + (b[0]-a[0])*frac);
        dot.setAttribute('cy', a[1] + (b[1]-a[1])*frac);
      }
      requestAnimationFrame(animate);
    }
    requestAnimationFrame(animate);
  }
})();
</script>
</body></html>
