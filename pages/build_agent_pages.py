#!/usr/bin/env python3
"""Builds the four agent pages from one shared shell. Run: python3 build.py"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))  # writes the pages next to this script
HQ_URL = "https://claude.ai/artifact/TVDxQLvtJLazHwpoArFq1r"
URLS = json.load(open(os.path.join(HERE, "urls.json"))) if os.path.exists(os.path.join(HERE, "urls.json")) else {}

BUSINESS = """About Sonny's business:
- Sonny Bowen, a one-person freelance web designer based in Shrewsbury, England. Takes on small businesses anywhere in England.
- Price: £595 to build a one-page website, then £50 a month.
- The £50 a month covers hosting, domain renewal, small updates when asked (prices, hours, photos, menu) and security updates with backups. Nothing else.
- Payment by bank transfer. The build fee is due within 7 days of the site going live.
- UK mobile for calls and texts: 07944 539622. WhatsApp is a Thai number (+66 93 121 6854), used only for WhatsApp.
- Example site (beauty businesses only: beauty, hair, nails, lashes, brows and similar): https://sonnybowen-afk.github.io/Revly/annie/"""

VOICE = """How every message must sound:
- Like a real person texting from their phone, not a template and not an AI. Plain everyday words, contractions, British spelling.
- Never mention reviews, ratings or stars in any way.
- Never invent facts (being a customer, walking past, "saw you're busy", owner names you weren't given).
- Never promise results ("more customers", "top of Google", "double your bookings", guarantees) and never use fake urgency.
- Banned words and patterns: "I hope this message finds you well", "I came across", "I noticed that", "elevate", "leverage", "boost your online presence", "take your business to the next level", "in today's digital age", "seamless", "unlock", "game-changer", "tailored", "I'd love to", "reach out", "don't hesitate", "just circling back", "gentle reminder", em-dashes, semicolons, bullet points or bold inside a message, more than one exclamation mark, more than one emoji.
- Sign off with just "Sonny"."""

LOCAL = "Only call Sonny local when the business is in Shrewsbury or a nearby Shropshire town (Telford, Wellington, Newport, Ludlow, Oswestry, Bridgnorth, Market Drayton, Whitchurch, Church Stretton). Elsewhere just say he builds websites for small businesses."

AGENTS = {
  "idea-creator": {
    "key": "idea", "c": "#3ddc97", "eye": "#d4ffe9", "role": "Finds leads and writes the pitch",
    "intro": "Tell it about a business and it writes a first message and a follow-up in your voice, checked against your rules. Finding new businesses on the web happens in Claude Code (see below).",
    "rules": [
      ("Always", ["Says exactly £595 to build and £50 a month", "Signs off \"Sonny\"", "Keeps texts under 60 words and emails under 120", "Uses one specific detail about the business and ends with one easy question", "Only calls you local around Shrewsbury, and offers the Annie example site to beauty businesses only"]),
      ("Never", ["Mentions reviews, ratings or stars", "Invents businesses, numbers or owner names", "Promises more customers or top of Google, or uses fake urgency", "Uses AI phrases like \"I hope this finds you well\" or \"elevate\", or em-dashes"]),
      ("Customer research", ["Walks the customer journey: can people find them, check prices and hours, book or contact, and find the address?", "Uses the biggest problem customers have as the pitch hook, framed as the customer's problem, not a criticism", "Passes what it found into the client brief, so web-builder puts it front and centre"]),
      ("In Claude Code it also", ["Searches Google, Facebook, Instagram, Yell, Checkatrade, Fresha, Booksy, Treatwell, Just Eat and local groups", "Labels each business: no website found, social media only, dead or parked site, or unconfirmed", "Skips chains, closed businesses and anyone already in your pipeline", "Ranks 5–10 leads and saves them to leads/<town>-<trade>-<date>.md"]),
    ],
    "claude_code": [
      ("Save email pitches as Gmail drafts", "Save the email pitches from my latest leads file as Gmail drafts. Don't send anything."),
    ],
  },
  "web-builder": {
    "key": "web", "c": "#4fb3ff", "eye": "#dcefff", "role": "Builds the client's site",
    "intro": "Fill in what you know about a new client. It spots what's missing and writes the message asking them for it, then gives you the complete brief to paste into Claude Code, where it builds the site.",
    "rules": [
      ("Builds", ["Starts from your house template, so every client gets the same polished layout", "Header, hero, services or menu with prices, about, photos, opening hours for all 7 days, contact with a map, and a \"Site by Sonny Bowen\" footer", "Call and WhatsApp buttons on phones, link previews and business details Google can read", "Screenshots the site on a phone and a desktop and fixes anything that looks off"]),
      ("Never", ["Invents prices, hours, numbers or testimonials. Missing info stays as a highlighted placeholder", "Changes the template layout. Only colours and content change between clients", "Uses filler like \"Welcome to our website\""]),
      ("Frontend standards", ["Mobile-first: checked at 360px, 768px and 1280px, with 44px tap targets and no sideways scrolling", "Accessible to WCAG 2.2 AA: proper headings, alt text, 4.5:1 contrast, visible focus, keyboard friendly", "Fast: LCP under 2.5s, compressed images under about 300KB, lazy-loading, and no frameworks on a one-page site", "Polished: consistent spacing, subtle hover effects, works in Safari, Chrome, Firefox and Edge"]),
      ("Design reference", ["Sites should feel like silviamalavasi.com: its layout, spacing, type and polish, adapted to each client. Never copied"]),
      ("Gives you", ["The site file, the colours it picked, the layout check result, and questions to send the client. For bigger jobs (booking, shop), a note so you can quote for them"]),
    ],
    "claude_code": [
      ("Build from a brief", "Use the web-builder agent to build a site from the brief in clients/briefs/<client>.md, then have critique review it and web-builder apply the fixes (2 rounds max)."),
      ("Apply fixes", "Use the web-builder agent to apply every fix from critique's last review of sites/<client>/index.html."),
    ],
  },
  "critique": {
    "key": "crit", "c": "#ff6070", "eye": "#ffdfe2", "role": "Checks everything, messages, sites and code, before it goes out",
    "intro": "Paste any message before you send it: a pitch, a follow-up or a chaser. It gives a verdict, points to exactly what's wrong, and hands back a fixed version ready to copy. Site reviews happen in Claude Code.",
    "rules": [
      ("Fails a message for", ["A wrong or missing price in a first pitch (must be £595 to build and £50 a month)", "Any mention of reviews, ratings or stars", "Made-up facts, over-promising or fake urgency"]),
      ("Flags", ["Anything that sounds like AI or like a sales template", "Salesy tone, more than one question, or too long for the channel", "Messages so generic they could go to anyone"]),
      ("Code review and security", ["Code is simple and readable, with no duplication", "No passwords, API keys or private details left in the code", "Forms check input, block spam and never post to unknown addresses", "Feedback in three levels: Must fix, Should fix and Could improve, each with the exact fix"]),
      ("For sites, in Claude Code", ["Looks at phone and desktop screenshots", "Checks spelling, that every fact matches the brief, all 7 days of hours, links and contrast", "Gives Must fix and Should fix lists with line numbers, plus questions to send the client"]),
    ],
    "claude_code": [
      ("Review a site", "Use the critique agent to review sites/<client>/index.html."),
      ("Review a leads file", "Use the critique agent to check every message in my latest leads file."),
    ],
  },
  "boss": {
    "key": "pm", "c": "#b98bff", "eye": "#f0e6ff", "role": "The master: runs every job and the pipeline", "master": True,
    "intro": "Your pipeline, live. Ask what to do today and it gives you who to chase with messages ready to send. Log anything that happens here and your Claude Code team records it.",
    "rules": [
      ("Runs things", ["Handles every request automatically: works out what you need and which agent does each part", "Runs independent jobs at the same time, e.g. leads in two towns at once", "Plans every job: which agents work on it, in what order, and with what", "Sends every change to a site's code to critique for review, even one-line fixes", "Knows every agent's rules, your prices and your playbook, so it can answer most questions itself", "Keeps clients/pipeline.md: Pitched → Replied → In progress → Delivered → Maintenance → Closed", "Logs pitches that got replies into the playbook, so idea-creator learns what works for you"]),
      ("When to chase", ["No reply to a pitch: after 4 days, then 7 days later. After 2 follow-ups it suggests closing them", "Replied but the next step is unclear: after 2 days. Waiting on client info: after 3 days", "£595 build fee: due 7 days after delivery. £50 maintenance: flagged 3 days before it's due"]),
      ("Never", ["Deletes a client, invents details, or sends anything itself"]),
    ],
    "claude_code": [
      ("Plan anything", "What should I do today? Ask boss to plan it and run the agents it picks."),
      ("Apply what I logged here", "Check my agent pages."),
    ],
  },
}

AVATAR_JS = r"""
function avatar(a, still) {
  const c = a.c, eye = a.eye, dark = "#0a0f1f";
  let top = "", face = "", chest = "";
  if (a.key === "pm") {
    top = `<path d="M34 26 L40 6 L50 18 L60 1 L70 18 L80 6 L86 26 Z" fill="#ffd166"/><circle cx="60" cy="4" r="3.5" fill="#fff4cf"/>
      <path d="M12 58 a48 48 0 0 1 96 0" fill="none" stroke="${dark}" stroke-width="4" opacity=".55"/>
      <rect x="6" y="52" width="10" height="20" rx="5" fill="${dark}"/><rect x="104" y="52" width="10" height="20" rx="5" fill="${dark}"/>
      <path d="M11 70 q2 18 22 18" fill="none" stroke="${dark}" stroke-width="3"/><circle cx="35" cy="88" r="4" fill="${dark}"/>`;
    chest = `<path d="M60 94 l3 6 6.5 .8 -4.8 4.4 1.3 6.4 -6 -3.2 -6 3.2 1.3 -6.4 -4.8 -4.4 6.5 -.8z" fill="#ffd166"/>`;
  } else if (a.key === "idea") {
    top = `<line x1="60" y1="26" x2="60" y2="13" stroke="${c}" stroke-width="4" stroke-linecap="round"/><circle class="${still ? "" : "bulb"}" cx="60" cy="8" r="8" fill="#fff6b8"/>
      <g stroke="#fff6b8" stroke-width="2.5" stroke-linecap="round" opacity=".8"><line x1="46" y1="4" x2="42" y2="1"/><line x1="74" y1="4" x2="78" y2="1"/><line x1="60" y1="-4" x2="60" y2="-8"/></g>`;
    chest = `<circle cx="57" cy="100" r="6" fill="none" stroke="${dark}" stroke-width="3"/><line x1="61.5" y1="104.5" x2="67" y2="110" stroke="${dark}" stroke-width="3.5" stroke-linecap="round"/>`;
  } else if (a.key === "web") {
    top = `<path d="M26 32 a34 24 0 0 1 68 0 z" fill="#ffd166"/><rect x="56" y="10" width="8" height="22" rx="3" fill="#f4b942"/><rect x="16" y="28" width="88" height="7" rx="3.5" fill="#f4b942"/>`;
    chest = `<text x="60" y="106" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="13" font-weight="700" fill="${dark}">&lt;/&gt;</text>`;
  } else {
    top = `<line x1="60" y1="26" x2="60" y2="15" stroke="${c}" stroke-width="4" stroke-linecap="round"/><circle cx="60" cy="11" r="5" fill="${c}"/>`;
    face = `<circle cx="74" cy="57" r="13" fill="none" stroke="#fff" stroke-width="3"/><path d="M87 60 q8 14 2 30" fill="none" stroke="#fff" stroke-width="2" opacity=".7"/>
      <rect class="${still ? "" : "scan"}" x="26" y="40" width="68" height="3" rx="1.5" fill="${c}" opacity=".7"/>`;
    chest = `<path d="M51 101 l6 6 12 -13" fill="none" stroke="${dark}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>`;
  }
  return `<svg viewBox="0 -10 120 142" aria-hidden="true">
    <ellipse cx="60" cy="128" rx="28" ry="5" fill="${c}" opacity=".28"/>
    <rect x="36" y="88" width="48" height="30" rx="14" fill="${c}" opacity=".9"/>
    <rect x="14" y="26" width="92" height="66" rx="24" fill="${c}"/>
    <rect x="24" y="36" width="72" height="46" rx="16" fill="${dark}"/>
    <g class="${still ? "" : "eyes"}"><rect x="39" y="48" width="12" height="17" rx="6" fill="${eye}"/><rect x="68" y="48" width="12" height="17" rx="6" fill="${eye}"/></g>
    <path d="M51 73 q9 6 18 0" fill="none" stroke="${eye}" stroke-width="3" stroke-linecap="round"/>
    ${face}${top}${chest}</svg>`;
}
"""

CSS = r"""
:root {
  color-scheme: dark;
  --ground: #0a0f1f; --panel: #111832; --panel-2: #0d1328; --field: #070b18; --line: #243056;
  --text: #e9edf9; --muted: #9ba6c6; --gold: #ffd166; --bad: #ff6070; --ok: #3ddc97; --warn: #ffd166;
  --display: "Chakra Petch", "Trebuchet MS", sans-serif;
  --body: "IBM Plex Sans", system-ui, -apple-system, "Segoe UI", sans-serif;
  --mono: "JetBrains Mono", ui-monospace, "Courier New", monospace;
}
html, body { background: var(--ground); }
body { color: var(--text); font-family: var(--body); font-size: 16px; line-height: 1.5; padding-inline: 16px; padding-block: 18px 48px; }
.wrap { max-width: 960px; margin-inline: auto; display: grid; gap: 22px; }
h1, h2, h3 { font-family: var(--display); line-height: 1.15; margin: 0; text-wrap: balance; }
h2 { font-size: 21px; }
p { margin: 0; }
a { color: var(--c); }
code { font-family: var(--mono); font-size: .86em; }
button, input, select, textarea { font: inherit; color: inherit; }
:focus-visible { outline: 3px solid var(--gold); outline-offset: 2px; border-radius: 6px; }

.back { font-size: 14px; color: var(--muted); text-decoration: none; }
.back:hover { color: var(--text); }
.hero { display: grid; grid-template-columns: 112px minmax(0, 1fr); gap: 20px; align-items: center;
  background: radial-gradient(ellipse at 10% 50%, color-mix(in srgb, var(--c) 18%, transparent), transparent 60%), var(--panel);
  border: 1px solid var(--line); border-radius: 18px; padding: 18px 22px; }
.hero .art { width: 112px; animation: bob 3.4s ease-in-out infinite; }
.hero .art svg { width: 100%; height: auto; overflow: visible; display: block; }
.hero h1 { font-size: clamp(28px, 5vw, 40px); color: var(--c); }
.hero .role { color: var(--text); font-weight: 600; margin-top: 2px; }
.hero .intro { color: var(--muted); margin-top: 8px; max-width: 64ch; }
.badge { display: inline-block; margin-left: 8px; vertical-align: middle; font-family: var(--display); font-size: 13px; letter-spacing: .1em; color: #1b1300; background: var(--gold); border-radius: 6px; padding: 1px 8px; }
@media (max-width: 520px) { .hero { grid-template-columns: 76px minmax(0, 1fr); gap: 14px; padding: 16px; } .hero .art { width: 76px; } }
@keyframes bob { 50% { transform: translateY(-6px); } }
.eyes { animation: blink 5.2s infinite; transform-box: fill-box; transform-origin: center; }
@keyframes blink { 0%, 93%, 100% { transform: scaleY(1); } 96% { transform: scaleY(.1); } }
.bulb { animation: glow 2.4s ease-in-out infinite; }
@keyframes glow { 50% { opacity: .45; } }
.scan { animation: scan 2.2s ease-in-out infinite; }
@keyframes scan { 50% { transform: translateY(34px); } }

.panel { background: var(--panel); border: 1px solid var(--line); border-radius: 16px; padding: 18px 20px; display: grid; gap: 14px; align-content: start; }
.panel.main { border-color: color-mix(in srgb, var(--c) 55%, var(--line)); }
.sub { color: var(--muted); font-size: 15px; max-width: 70ch; }
.grid { display: grid; gap: 12px; grid-template-columns: repeat(auto-fit, minmax(min(100%, 220px), 1fr)); }
.full { grid-column: 1 / -1; }
.field { display: grid; gap: 4px; }
.field label { font-size: 14px; font-weight: 600; }
.field label small { font-weight: 400; color: var(--muted); }
input, select, textarea { width: 100%; min-height: 44px; background: var(--field); border: 1px solid var(--line); border-radius: 10px; padding: 9px 12px; }
textarea { min-height: 88px; resize: vertical; line-height: 1.45; }
input:focus, select:focus, textarea:focus { border-color: var(--c); outline: none; box-shadow: 0 0 0 2px color-mix(in srgb, var(--c) 35%, transparent); }
.actions { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; }
.btn { min-height: 44px; padding: 8px 18px; border-radius: 10px; cursor: pointer; background: var(--panel-2); border: 1px solid var(--line); font-weight: 600; }
.btn:hover { border-color: var(--muted); }
.btn.primary { background: var(--c); border-color: var(--c); color: #0b1020; font-family: var(--display); font-size: 16px; }
.btn.primary:hover { filter: brightness(1.08); }
.btn.small { min-height: 34px; padding: 3px 12px; font-size: 14px; }
.btn[disabled] { opacity: .55; cursor: default; }
.note { font-size: 14px; color: var(--muted); }
.note.err { color: var(--bad); }

.out { display: grid; gap: 12px; }
.msg { background: var(--panel-2); border: 1px solid var(--line); border-radius: 12px; padding: 12px 14px; display: grid; gap: 8px; }
.msg-head { display: flex; justify-content: space-between; align-items: center; gap: 10px; flex-wrap: wrap; }
.msg-head b { font-family: var(--display); font-size: 15px; color: var(--c); }
.msg-head span { font-size: 13px; color: var(--muted); }
.msg-body { white-space: pre-wrap; overflow-wrap: anywhere; }
.thinking { color: var(--muted); font-style: italic; }

.verdict { display: inline-block; font-family: var(--display); font-weight: 700; letter-spacing: .06em; padding: 4px 12px; border-radius: 8px; font-size: 16px; }
.verdict.PASS { background: color-mix(in srgb, var(--ok) 18%, transparent); color: var(--ok); }
.verdict.NEEDS { background: color-mix(in srgb, var(--warn) 18%, transparent); color: var(--warn); }
.verdict.FAIL { background: color-mix(in srgb, var(--bad) 18%, transparent); color: var(--bad); }
.issues { margin: 0; padding-left: 20px; display: grid; gap: 8px; }
.issues q { color: var(--text); font-style: italic; }
.issues .fix { color: var(--ok); }

pre.cmd { margin: 0; background: var(--field); border: 1px solid var(--line); border-radius: 10px; padding: 10px 12px; font-family: var(--mono); font-size: 13px; line-height: 1.55; white-space: pre-wrap; overflow-wrap: anywhere; color: #d7def5; max-height: 360px; overflow-y: auto; }
.cc { display: grid; gap: 12px; }
.cc-item { display: grid; gap: 6px; }
.cc-head { display: flex; justify-content: space-between; align-items: center; gap: 10px; font-weight: 600; font-size: 15px; }

.lessons { display: grid; gap: 6px; margin: 0; padding: 0; list-style: none; }
.lessons li { display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 4px 12px; align-items: center; background: var(--panel-2); border: 1px solid var(--line); border-radius: 10px; padding: 8px 12px; font-size: 15px; }
.lessons li small { grid-column: 1; color: var(--muted); font-size: 13px; }
.lessons .x { grid-row: 1 / span 2; grid-column: 2; }
.chip { font-size: 12px; font-weight: 600; padding: 1px 8px; border-radius: 999px; }
.chip.new { color: var(--warn); background: color-mix(in srgb, var(--warn) 15%, transparent); }
.chip.applied { color: var(--ok); background: color-mix(in srgb, var(--ok) 15%, transparent); }

details.rules summary { cursor: pointer; font-family: var(--display); font-weight: 600; font-size: 17px; min-height: 36px; display: flex; align-items: center; }
details.rules[open] summary { margin-bottom: 8px; }
.rulegrid { display: grid; gap: 14px; grid-template-columns: repeat(auto-fit, minmax(min(100%, 260px), 1fr)); }
.rulegrid h3 { font-size: 13px; letter-spacing: .1em; text-transform: uppercase; color: var(--muted); margin-bottom: 6px; }
.rulegrid ul { margin: 0; padding-left: 18px; display: grid; gap: 4px; font-size: 15px; }

/* pipeline (boss) */
.money { display: grid; gap: 10px; grid-template-columns: repeat(3, minmax(0, 1fr)); }
.tile { background: var(--panel-2); border: 1px solid var(--line); border-radius: 12px; padding: 10px 14px; }
.tile span { display: block; font-size: 13px; color: var(--muted); }
.tile b { font-family: var(--display); font-size: 26px; font-variant-numeric: tabular-nums; }
.tile.alert b { color: var(--bad); } .tile.good b { color: var(--ok); }
@media (max-width: 480px) { .money { grid-template-columns: minmax(0, 1fr); } .tile { display: flex; justify-content: space-between; align-items: baseline; } }
.rows { display: grid; gap: 6px; }
.row { display: grid; grid-template-columns: minmax(0, 1.4fr) 112px minmax(0, 1.3fr) 118px minmax(0, 1fr); gap: 10px; align-items: center; background: var(--panel-2); border: 1px solid var(--line); border-radius: 10px; padding: 9px 12px; font-size: 15px; }
.row.head { background: none; border: 0; padding-block: 0; font-family: var(--display); font-size: 12px; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); }
.row .biz { font-weight: 600; } .row small { display: block; color: var(--muted); font-weight: 400; font-size: 13px; }
.row .contact { overflow-wrap: anywhere; }
.pill { justify-self: start; font-size: 12px; font-weight: 600; padding: 2px 9px; border-radius: 999px; color: var(--sc); background: color-mix(in srgb, var(--sc) 16%, transparent); white-space: nowrap; }
.due { font-variant-numeric: tabular-nums; font-size: 14px; } .due.over { color: var(--bad); font-weight: 600; } .due.today { color: var(--gold); font-weight: 600; } .due.none { color: var(--muted); }
@media (max-width: 720px) {
  .row { grid-template-columns: minmax(0, 1fr) auto; gap: 3px 10px; } .row.head { display: none; }
  .row .pill { grid-column: 2; grid-row: 1; justify-self: end; } .row .next { grid-column: 1 / -1; }
  .row .due { grid-column: 2; grid-row: 3; justify-self: end; } .row .contact { grid-column: 1; grid-row: 3; font-size: 14px; }
}
.empty { border: 1px dashed var(--line); border-radius: 12px; padding: 16px; color: var(--muted); text-align: center; }
footer { color: var(--muted); font-size: 13px; text-align: center; }
@media (prefers-reduced-motion: reduce) { .hero .art, .eyes, .bulb, .scan { animation: none; } }
"""

SHELL = r"""<title>__TITLE__</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@600;700&family=IBM+Plex+Sans:wght@400;600&family=JetBrains+Mono:wght@500&display=swap">
<style>__CSS__</style>
<div class="wrap" style="--c: __COLOR__">
  <a class="back" href="__HQ__" target="_blank" rel="noopener">← Web Crew HQ</a>
  <header class="hero">
    <div class="art" id="art"></div>
    <div>
      <h1>__NAME____BADGE__</h1>
      <p class="role">__ROLE__</p>
      <p class="intro">__INTRO__</p>
    </div>
  </header>

__TOOL__

  <section class="panel" aria-labelledby="train-h">
    <h2 id="train-h">Teach __NAME__</h2>
    <p class="sub">Write a rule, a preference or an example in plain English. This page uses it straight away. Your Claude Code team picks it up the next time you say <b>"check my agent pages"</b> in a Claude Code session on My-Team.</p>
    <form id="trainForm" class="grid">
      <div class="field full"><label for="lesson">New lesson</label><textarea id="lesson" required placeholder="__LESSON_EG__"></textarea></div>
      <div class="actions full"><button class="btn primary" type="submit">Save lesson</button><span class="note" id="trainNote"></span></div>
    </form>
    <ul class="lessons" id="lessons"></ul>
  </section>

  <section class="panel" aria-labelledby="cc-h">
    <h2 id="cc-h">Use __NAME__ in Claude Code</h2>
    <p class="sub">Open a Claude Code session on <b>sonnybowen-afk/My-Team</b> (at claude.ai/code or in the Code tab of the Claude app), paste one of these and press send. No slash commands needed.</p>
    <div class="cc" id="cc"></div>
  </section>

  <section class="panel">
    <details class="rules">
      <summary>How __NAME__ works</summary>
      <div class="rulegrid">__RULES__</div>
    </details>
  </section>

  <footer>Part of Sonny's Web Crew · sonnybowen-afk/My-Team</footer>
</div>

<script>
(() => {
const AGENT = __AGENT_JSON__;
const CC = __CC_JSON__;
__AVATAR__
document.getElementById("art").innerHTML = avatar(AGENT, false);

const $ = (id) => document.getElementById(id);
const hasClaude = typeof claude !== "undefined" && claude && claude.use;
const dbP = hasClaude ? claude.use("db") : Promise.resolve(null);
const sampleP = hasClaude ? claude.use("sample") : Promise.resolve(null);
const BUSINESS = __BUSINESS__;
const VOICE = __VOICE__;
const LOCAL = __LOCAL__;

function el(tag, cls, text) { const e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }
function todayISO() { const d = new Date(), p = (n) => String(n).padStart(2, "0"); return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`; }
function words(s) { return (s.trim().match(/\S+/g) || []).length; }

function copy(text, btn, node) {
  const label = btn.textContent;
  const done = () => { btn.textContent = "Copied"; setTimeout(() => (btn.textContent = label), 1300); };
  const fallback = () => { if (node) { const r = document.createRange(); r.selectNodeContents(node); const s = getSelection(); s.removeAllRanges(); s.addRange(r); } btn.textContent = "Press Ctrl+C"; };
  try { navigator.clipboard.writeText(text).then(done, fallback); } catch (e) { fallback(); }
}
function copyBtn(getText, node) { const b = el("button", "btn small", "Copy"); b.type = "button"; b.addEventListener("click", () => copy(getText(), b, node)); return b; }

function msgBlock(title, text, meta) {
  const box = el("div", "msg");
  const head = el("div", "msg-head");
  const left = el("div"); left.append(el("b", null, title)); if (meta) { left.append(" "); left.append(el("span", null, meta)); }
  const body = el("div", "msg-body", text);
  head.append(left, copyBtn(() => text, body));
  box.append(head, body);
  return box;
}

function sampleError(e) {
  const code = e && e.code;
  if (["not_granted", "sampling_disabled", "not_declared", "capability_disabled", "capability_removed", "unavailable"].includes(code))
    return "Claude can't run on this page right now. Use the Claude Code instructions further down instead.";
  if (code === "rate_limited") return "Too many requests. Give it a minute and try again.";
  if (code === "session_expired") return "You've been signed out of Claude. Sign in again and retry.";
  if (code === "invalid_json") return "The answer came back jumbled. Press the button again.";
  if (code === "refused") return "Claude wouldn't write that. Try rewording what you entered.";
  if (code === "prompt_too_large") return "That's too much text at once. Shorten it and try again.";
  return "Something went wrong. Press the button to try again.";
}

// Run one Claude request with a Stop button and a thinking message.
async function ask(prompt, { out, button, tier = "default" }) {
  const sample = await sampleP;
  if (!sample) throw { code: "unavailable" };
  const ctl = new AbortController();
  const stop = el("button", "btn", "Stop"); stop.type = "button";
  stop.addEventListener("click", () => ctl.abort());
  button.disabled = true;
  button.after(stop);
  out.hidden = false;
  out.replaceChildren(el("p", "thinking", "Thinking… this usually takes 10–40 seconds."));
  try {
    return await sample.json(prompt, { modelTier: tier, cache: false, signal: ctl.signal });
  } finally {
    button.disabled = false;
    stop.remove();
  }
}

// ---------- Lessons (training) ----------
let lessons = [];
function lessonsText() {
  const list = lessons.filter((l) => l.text).map((l) => "- " + l.text);
  return list.length ? "\n\nSonny has taught you these extra rules. They override anything above:\n" + list.join("\n") : "";
}
(async () => {
  const db = await dbP;
  const note = $("trainNote");
  const listEl = $("lessons");
  if (!db) { note.textContent = "Lessons save when this page is open in Claude."; return; }
  db.collection("lessons").orderBy("created", "desc").limit(100).onSnapshot((snap) => {
    lessons = snap.docs.map((d) => ({ id: d.id, ...d.data() }));
    listEl.replaceChildren();
    if (!lessons.length) { listEl.append(el("li", "empty", "No lessons yet.")); return; }
    lessons.forEach((l) => {
      const li = el("li");
      const text = el("span", null, l.text || "");
      const meta = el("small");
      const chip = el("span", "chip " + (l.status === "applied" ? "applied" : "new"), l.status === "applied" ? "Learned in Claude Code" : "Waiting for Claude Code");
      meta.append(chip, " " + (l.created ? new Date(l.created).toLocaleDateString("en-GB", { day: "numeric", month: "short" }) : ""));
      li.append(text, meta);
      if (l.status !== "applied") {
        const x = el("button", "btn small x", "Remove"); x.type = "button";
        x.addEventListener("click", async () => { x.disabled = true; try { await db.doc("lessons/" + l.id).delete(); } catch (e) { x.disabled = false; note.textContent = "Couldn't remove that lesson. Try again."; } });
        li.append(x);
      }
      listEl.append(li);
    });
  }, () => { note.textContent = "Couldn't load lessons. Reload the page."; });
  $("trainForm").addEventListener("submit", async (ev) => {
    ev.preventDefault();
    const box = $("lesson"), text = box.value.trim();
    if (!text) return;
    const btn = ev.submitter || $("trainForm").querySelector("button");
    btn.disabled = true; note.textContent = "Saving…";
    try {
      await db.collection("lessons").add({ text: text.slice(0, 1000), created: new Date().toISOString(), status: "new" });
      box.value = ""; note.textContent = "Saved. This page uses it from now on.";
    } catch (e) {
      note.textContent = e && e.code === "invalid_argument" ? "Only you can teach this agent." : "Couldn't save. Try again.";
    } finally { btn.disabled = false; }
  });
})();

// ---------- Claude Code instructions ----------
function renderCC(extra) {
  const wrap = $("cc"); wrap.replaceChildren();
  [...(extra || []), ...CC].forEach(([label, text]) => {
    const item = el("div", "cc-item");
    const head = el("div", "cc-head", label);
    const pre = el("pre", "cmd", text);
    head.append(copyBtn(() => pre.textContent, pre));
    item.append(head, pre);
    wrap.append(item);
  });
}
renderCC();

__AGENT_JS__
})();
</script>
"""

# ---------------------------------------------------------------- idea-creator
IDEA_TOOL = r"""
  <section class="panel main" aria-labelledby="tool-h">
    <h2 id="tool-h">Write a pitch</h2>
    <form id="pitchForm" class="grid">
      <div class="field"><label for="biz">Business name</label><input id="biz" required autocomplete="off" placeholder="e.g. Annie's Nails"></div>
      <div class="field"><label for="trade">What they do</label><input id="trade" required autocomplete="off" placeholder="e.g. nail salon"></div>
      <div class="field"><label for="town">Town</label><input id="town" required value="Shrewsbury"></div>
      <div class="field"><label for="channel">How you'll send it</label>
        <select id="channel"><option>WhatsApp</option><option>Text message</option><option>Email</option><option>Instagram DM</option><option>Facebook DM</option></select></div>
      <div class="field"><label for="owner">Owner's first name <small>(if you know it)</small></label><input id="owner" autocomplete="off"></div>
      <div class="field full"><label for="hook">What did you notice about them?</label><textarea id="hook" required placeholder="What would a customer struggle with? e.g. Only on Instagram, no way to see prices or book without messaging"></textarea></div>
      <div class="actions full"><button class="btn primary" type="submit" id="pitchBtn">Write pitch</button></div>
    </form>
    <div class="out" id="pitchOut" hidden></div>
  </section>
"""
IDEA_JS = r"""
const RULES = `You are idea-creator, the pitch writer on Sonny's team. Write a first message and a follow-up (sent about 4 days later if there's no reply) pitching a website to one local business.

${BUSINESS}

${VOICE}

Pitch rules:
- The first message must say exactly "£595 to build" and "£50 a month" (e.g. "£595 to build it and then £50 a month to keep it running"). Never write "GBP". Describe the monthly fee only using what's listed above.
- Length: WhatsApp or text message 2-4 sentences, under 60 words. Instagram or Facebook DM under 50 words. Email under 120 words with a short, plain, lowercase-ish subject line.
- Open with "Hi" or "Hiya" and the business name, or the owner's first name if given. Say who Sonny is in a few words.
- Use the detail Sonny noticed so it's clearly not a mass message. Frame it as a problem the business's CUSTOMERS have (e.g. "people can't see your prices without messaging"), never as a criticism of the owner. End with ONE low-pressure question. Offer the example site link only to beauty businesses; for anything else offer to send an example.
- ${LOCAL}
- WhatsApp only: mention in a few words that this is Sonny's WhatsApp and he's on 07944 539622 for calls.
- The follow-up is 1-2 sentences, under 30 words, friendly, no pressure, and doesn't repeat the price or the pitch.
- Before answering, check both messages against every rule above and fix anything that breaks one.`;

const f = $("pitchForm");
f.addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const v = (id) => $(id).value.trim();
  const channel = v("channel");
  const prompt = `${RULES}${lessonsText()}

The business:
- Name: ${v("biz")}
- What they do: ${v("trade")}
- Town: ${v("town")}
- Owner's first name: ${v("owner") || "not known (don't use one)"}
- Channel: ${channel}
- What Sonny noticed: ${v("hook")}

Reply with only JSON in this shape: {"subject": "email subject line, or empty string if not email", "first": "the first message", "followup": "the follow-up message"}`;
  const out = $("pitchOut");
  try {
    const r = await ask(prompt, { out, button: $("pitchBtn") });
    out.replaceChildren();
    if (channel === "Email" && r.subject) out.append(msgBlock("Subject line", String(r.subject)));
    const first = String(r.first || ""), follow = String(r.followup || "");
    out.append(msgBlock("First message", first, `${channel} · ${words(first)} words`));
    out.append(msgBlock("Follow-up", follow, `send after about 4 days with no reply · ${words(follow)} words`));
    out.append(el("p", "note", "Want a second opinion? Paste it into critique's page first."));
  } catch (e) {
    if (e && e.code === "cancelled") { out.replaceChildren(el("p", "note", "Stopped.")); return; }
    out.replaceChildren(el("p", "note err", sampleError(e)));
  }
});

// Lead-finding instruction builder
const cc = $("cc");
const finder = document.createElement("div");
finder.className = "grid";
finder.innerHTML = `
  <div class="field"><label for="fTown">Town</label><input id="fTown" value="Shrewsbury"></div>
  <div class="field"><label for="fTrade">Type of business</label><input id="fTrade" value="nail salons"></div>
  <div class="field"><label for="fCount">How many</label><input id="fCount" type="number" min="3" max="15" value="8"></div>
  <div class="field"><label for="fChan">Preferred channel</label><select id="fChan"><option>WhatsApp</option><option>text message</option><option>email</option><option>whatever fits each one</option></select></div>`;
cc.before(finder);
function finderText() {
  const g = (id) => $(id).value.trim();
  return `Use the idea-creator agent to find ${g("fCount") || 8} ${g("fTrade") || "small businesses"} in ${g("fTown") || "Shrewsbury"} with no website and draft ${g("fChan") === "whatever fits each one" ? "pitches using whichever channel fits each one" : g("fChan") + " pitches"}. Then have the critique agent check every one, apply its fixes, save any email pitches as Gmail drafts, and show me the final messages.`;
}
function refreshFinder() { renderCC([["Find new leads (from the boxes above)", finderText()]]); }
finder.addEventListener("input", refreshFinder);
refreshFinder();
"""

# ---------------------------------------------------------------- critique
CRIT_TOOL = r"""
  <section class="panel main" aria-labelledby="tool-h">
    <h2 id="tool-h">Check a message</h2>
    <form id="critForm" class="grid">
      <div class="field"><label for="kind">What is it?</label>
        <select id="kind"><option>First pitch</option><option>Follow-up to a pitch</option><option>Chase or payment reminder</option><option>Other message to a client</option></select></div>
      <div class="field"><label for="chan">Channel</label>
        <select id="chan"><option>WhatsApp</option><option>Text message</option><option>Email</option><option>Instagram DM</option><option>Facebook DM</option></select></div>
      <div class="field"><label for="who">Business <small>(optional)</small></label><input id="who" autocomplete="off"></div>
      <div class="field full"><label for="msg">The message</label><textarea id="msg" required rows="6" placeholder="Paste the message here"></textarea></div>
      <div class="actions full"><button class="btn primary" type="submit" id="critBtn">Check it</button><span class="note" id="wc"></span></div>
    </form>
    <div class="out" id="critOut" hidden></div>
  </section>
"""
CRIT_JS = r"""
const RULES = `You are critique, the quality checker on Sonny's team. Review one message before Sonny sends it. Be direct and specific: every issue needs an exact fix.

${BUSINESS}

${VOICE}

Hard rules (breaking one = FAIL):
- A FIRST PITCH must include exactly "£595 to build" and "£50 a month". Wrong numbers, a missing figure, "GBP"/"595gbp", or vague wording like "a small monthly fee" fails. Other message types don't need the price, but any price they mention must be right.
- Any mention of reviews, ratings or stars.
- Made-up facts: being a customer, walking past, "saw you're busy".
- Over-promising ("more customers", "top of Google", "guaranteed") or monthly extras not listed above.
- Fake urgency or scarcity.

Tone and form (NEEDS CHANGES):
- AI or template phrasing (the banned list above), em-dashes, semicolons, a tidy three-part list, flawless formal grammar in a text, bullets or bold in a text.
- Salesy: more than one exclamation mark, hype words, more than one question or ask, a pushy close.
- Too long: WhatsApp or text over 60 words, DM over 50, email over 120, follow-up over 30.
- Generic: nothing specific to this business.
- Wrong for the channel (e.g. an email-style sign-off in a WhatsApp).
- ${LOCAL}
- The example link may only be offered to beauty businesses.

Verdict: PASS if nothing needs changing, NEEDS CHANGES for tone or form problems, FAIL if any hard rule is broken. For anything other than PASS, give the full revised message, ready to send, keeping Sonny's voice and any real details.`;

const msg = $("msg");
msg.addEventListener("input", () => { $("wc").textContent = msg.value.trim() ? words(msg.value) + " words" : ""; });
$("critForm").addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const kind = $("kind").value, chan = $("chan").value, who = $("who").value.trim();
  const text = msg.value.trim();
  const prompt = `${RULES}${lessonsText()}

Message type: ${kind}
Channel: ${chan}
Business: ${who || "not given"}
Word count: ${words(text)}

The message (between the lines):
-----
${text.slice(0, 6000)}
-----

Reply with only JSON in this shape: {"verdict": "PASS" | "NEEDS CHANGES" | "FAIL", "summary": "one short sentence", "issues": [{"quote": "exact words from the message", "problem": "what's wrong", "fix": "replacement words"}], "revised": "the full corrected message, or empty string if PASS"}`;
  const out = $("critOut");
  try {
    const r = await ask(prompt, { out, button: $("critBtn") });
    out.replaceChildren();
    const verdict = String(r.verdict || "").toUpperCase();
    const cls = verdict.startsWith("PASS") ? "PASS" : verdict.startsWith("FAIL") ? "FAIL" : "NEEDS";
    const head = el("div", "msg-head");
    head.append(el("span", "verdict " + cls, cls === "NEEDS" ? "NEEDS CHANGES" : cls));
    out.append(head);
    if (r.summary) out.append(el("p", null, String(r.summary)));
    const issues = Array.isArray(r.issues) ? r.issues : [];
    if (issues.length) {
      const ol = el("ol", "issues");
      issues.forEach((i) => {
        const li = el("li");
        if (i.quote) { li.append(el("q", null, String(i.quote)), " "); }
        li.append(String(i.problem || ""));
        if (i.fix) { li.append(el("br"), el("span", "fix", "Fix: " + String(i.fix))); }
        ol.append(li);
      });
      out.append(ol);
    }
    if (cls !== "PASS" && r.revised) out.append(msgBlock("Revised message", String(r.revised), `${words(String(r.revised))} words`));
    if (cls === "PASS") out.append(el("p", "note", "Good to send."));
  } catch (e) {
    if (e && e.code === "cancelled") { out.replaceChildren(el("p", "note", "Stopped.")); return; }
    out.replaceChildren(el("p", "note err", sampleError(e)));
  }
});
"""

# ---------------------------------------------------------------- web-builder
WEB_TOOL = r"""
  <section class="panel main" aria-labelledby="tool-h">
    <h2 id="tool-h">New client brief</h2>
    <form id="briefForm" class="grid">
      <div class="field"><label for="bName">Business name</label><input id="bName" required autocomplete="off"></div>
      <div class="field"><label for="bType">Type of business</label><input id="bType" autocomplete="off" placeholder="e.g. nail salon"></div>
      <div class="field"><label for="bTown">Town</label><input id="bTown" value="Shrewsbury"></div>
      <div class="field"><label for="bOwner">Owner's name</label><input id="bOwner" autocomplete="off"></div>
      <div class="field"><label for="bPhone">Phone</label><input id="bPhone" inputmode="tel" autocomplete="off"></div>
      <div class="field"><label for="bEmail">Email</label><input id="bEmail" type="email" autocomplete="off"></div>
      <div class="field"><label for="bAddr">Address</label><input id="bAddr" autocomplete="off"></div>
      <div class="field"><label for="bSocial">Instagram / Facebook</label><input id="bSocial" autocomplete="off"></div>
      <div class="field"><label for="bBook">Booking link <small>(if any)</small></label><input id="bBook" autocomplete="off"></div>
      <div class="field"><label for="bTone">Tone</label><select id="bTone"><option>Friendly and local</option><option>Smart and professional</option><option>Fun</option><option>Traditional</option></select></div>
      <div class="field"><label for="bColours">Brand colours</label><input id="bColours" autocomplete="off" placeholder="e.g. match the sign, or you pick"></div>
      <div class="field full"><label for="bServices">Services, menu and prices <small>(one per line: name, price, short description)</small></label><textarea id="bServices" rows="5"></textarea></div>
      <div class="field full"><label for="bHours">Opening hours <small>(all 7 days)</small></label><textarea id="bHours" rows="4" placeholder="Mon closed&#10;Tue–Fri 9–5&#10;Sat 9–4&#10;Sun closed"></textarea></div>
      <div class="field full"><label for="bAbout">About them <small>(2–3 sentences, in their words if you can)</small></label><textarea id="bAbout" rows="3"></textarea></div>
      <div class="field full"><label for="bNeeds">What their customers struggle with <small>(from idea-creator's research: can't see prices, hours, booking…)</small></label><textarea id="bNeeds" rows="2"></textarea></div>
      <div class="field full"><label for="bPhotos">Photos and anything else</label><textarea id="bPhotos" rows="2" placeholder="e.g. Annie will send 6 photos; wants the prices to stand out"></textarea></div>
      <div class="actions full"><button class="btn primary" type="submit" id="gapBtn">What's missing?</button><span class="note">Your brief updates below as you type.</span></div>
    </form>
    <div class="out" id="gapOut" hidden></div>
  </section>
"""
WEB_JS = r"""
const RULES = `You are web-builder on Sonny's team. Sonny is about to build a one-page website for a client. Look at the brief below and work out what's still missing to build a complete site: business name, what they do, phone, email, address or area covered, every service or menu item with a price, opening hours for all 7 days, a short about, photos (a hero shot and about 6 for a gallery), brand colours, and social links. Never invent anything.

Then write ONE short, friendly WhatsApp message from Sonny to the client asking for just the missing things, in plain everyday words.

${VOICE}`;

const g = (id) => $(id).value.trim();
function slug(s) { return s.toLowerCase().replace(/&/g, "and").replace(/['’]/g, "").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "client"; }
function briefText() {
  const lines = (s) => s.split(/\n+/).map((l) => l.trim()).filter(Boolean).map((l) => "- " + l).join("\n") || "- ";
  return `# Client brief: ${g("bName") || "[Business name]"}

## Basics
- **Business name:** ${g("bName")}
- **Type of business:** ${g("bType")}
- **Town / area:** ${g("bTown")}
- **Owner's name:** ${g("bOwner")}

## Contact
- **Phone:** ${g("bPhone")}
- **Email:** ${g("bEmail")}
- **Address:** ${g("bAddr")}
- **Facebook / Instagram:** ${g("bSocial")}
- **Booking link:** ${g("bBook")}

## Services / menu / prices
${lines(g("bServices"))}

## Opening hours
${lines(g("bHours"))}

## About
${g("bAbout")}

## Customer needs (from idea-creator's research)
${lines(g("bNeeds"))}

## Photos and notes
${g("bPhotos")}

## Look and feel
- **Tone:** ${g("bTone")}
- **Brand colours:** ${g("bColours")}`;
}
function refresh() {
  const name = g("bName") || "the client";
  const s = slug(g("bName") || "client");
  renderCC([[`Build ${name}'s site (brief included)`,
    `Save this brief to clients/briefs/${s}.md, then use the web-builder agent to build the site. Have the critique agent review it and web-builder apply the fixes (2 rounds max). Then have boss put ${name} in In progress and sync the HQ page.\n\n${briefText()}`]]);
}
$("briefForm").addEventListener("input", refresh);
refresh();

$("briefForm").addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const out = $("gapOut");
  const prompt = `${RULES}${lessonsText()}

The brief so far:
${briefText()}

Reply with only JSON in this shape: {"ready": true or false, "missing": ["short item", ...], "message": "the WhatsApp to the client, or empty string if nothing is missing"}`;
  try {
    const r = await ask(prompt, { out, button: $("gapBtn") });
    out.replaceChildren();
    const missing = Array.isArray(r.missing) ? r.missing : [];
    if (!missing.length) { out.append(el("p", null, "Nothing important is missing. Copy the brief below into Claude Code to build it.")); return; }
    const ul = el("ul", "issues");
    missing.forEach((m) => ul.append(el("li", null, String(m))));
    out.append(el("b", null, "Still needed:"), ul);
    if (r.message) out.append(msgBlock("Message to the client", String(r.message), "WhatsApp"));
  } catch (e) {
    if (e && e.code === "cancelled") { out.replaceChildren(el("p", "note", "Stopped.")); return; }
    out.replaceChildren(el("p", "note err", sampleError(e)));
  }
});
"""

# ---------------------------------------------------------------- boss
PM_TOOL = r"""
  <section class="panel main" aria-labelledby="pipe-h">
    <div class="actions" style="justify-content: space-between"><h2 id="pipe-h">Pipeline</h2><span class="note" id="pipeUpdated">Connecting…</span></div>
    <div class="money">
      <div class="tile" id="tDue"><span>Chase today or overdue</span><b id="mDue">0</b></div>
      <div class="tile" id="tOwed"><span>Build fees owed</span><b id="mOwed">£0</b></div>
      <div class="tile good"><span>Monthly income</span><b id="mMonthly">£0</b></div>
    </div>
    <div class="rows" id="rows" hidden></div>
    <p class="empty" id="pipeEmpty">No clients yet. Head to idea-creator's page, or ask Claude Code to find you some leads.</p>
    <div class="actions"><button class="btn primary" type="button" id="todayBtn">What should I do today?</button></div>
    <div class="out" id="todayOut" hidden></div>
  </section>

  <section class="panel" aria-labelledby="log-h">
    <h2 id="log-h">Log what happened</h2>
    <p class="sub">Sent a pitch, got a reply, got paid? Log it here. Your Claude Code team updates the pipeline the next time you say <b>"check my agent pages"</b>.</p>
    <form id="logForm" class="grid">
      <div class="field"><label for="lBiz">Business</label><input id="lBiz" list="bizList" required autocomplete="off"><datalist id="bizList"></datalist></div>
      <div class="field"><label for="lWhat">What happened</label>
        <select id="lWhat"><option>I sent the pitch</option><option>I sent a follow-up</option><option>They replied</option><option>They said yes</option><option>Not interested</option><option>Site delivered and invoice sent</option><option>They paid the £595</option><option>They paid the £50 maintenance</option><option>Other</option></select></div>
      <div class="field"><label for="lDate">Date</label><input id="lDate" type="date"></div>
      <div class="field full"><label for="lNote">Details <small>(optional: what they said, contact details, channel)</small></label><textarea id="lNote" rows="2"></textarea></div>
      <div class="actions full"><button class="btn primary" type="submit">Log it</button><span class="note" id="logNote"></span></div>
    </form>
    <ul class="lessons" id="updates"></ul>
  </section>
"""
PM_JS = r"""
const STAGES = { pitched: ["Pitched", "#3ddc97"], replied: ["Replied", "#ffd166"], in_progress: ["In progress", "#4fb3ff"], delivered: ["Delivered", "#b98bff"], maintenance: ["Maintenance", "#6fe3c1"], closed: ["Closed", "#8a93b3"] };
const today = todayISO();
$("lDate").value = today;
const dayDiff = (d) => Math.round((Date.parse(d + "T00:00:00") - Date.parse(today + "T00:00:00")) / 86400000);
const fmt = (d) => new Date(d + "T00:00:00").toLocaleDateString("en-GB", { day: "numeric", month: "short" });
let pipeline = { updated: "", clients: [] };

function dueInfo(c) {
  if (!c.due || c.stage === "closed") return { cls: "none", text: "—", rank: 1e6 };
  const n = dayDiff(c.due);
  if (isNaN(n)) return { cls: "none", text: c.due, rank: 1e5 };
  if (n < 0) return { cls: "over", text: `${-n} day${n === -1 ? "" : "s"} overdue`, rank: n };
  if (n === 0) return { cls: "today", text: "Today", rank: 0 };
  return { cls: "", text: n <= 7 ? `${fmt(c.due)} · ${n}d` : fmt(c.due), rank: n };
}
function renderPipeline() {
  const clients = (pipeline.clients || []).filter((c) => c && STAGES[c.stage]);
  $("pipeUpdated").textContent = pipeline.updated ? "Updated " + fmt(pipeline.updated) : "Not synced yet";
  const count = (s) => clients.filter((c) => c.stage === s).length;
  const chase = clients.filter((c) => c.stage !== "closed" && c.due && dayDiff(c.due) <= 0).length;
  $("mDue").textContent = chase; $("tDue").classList.toggle("alert", chase > 0);
  $("mOwed").textContent = "£" + (count("delivered") * 595).toLocaleString("en-GB"); $("tOwed").classList.toggle("alert", count("delivered") > 0);
  $("mMonthly").textContent = "£" + (count("maintenance") * 50).toLocaleString("en-GB");
  const dl = $("bizList"); dl.replaceChildren(); clients.forEach((c) => { const o = document.createElement("option"); o.value = c.business || ""; dl.append(o); });
  const rows = $("rows"); rows.replaceChildren();
  $("pipeEmpty").hidden = clients.length > 0; rows.hidden = !clients.length;
  if (!clients.length) return;
  const head = el("div", "row head"); ["Business", "Stage", "Next", "Due", "Contact"].forEach((t) => head.append(el("span", null, t))); rows.append(head);
  clients.map((c) => ({ c, d: dueInfo(c) }))
    .sort((a, b) => (a.c.stage === "closed") - (b.c.stage === "closed") || a.d.rank - b.d.rank)
    .forEach(({ c, d }) => {
      const r = el("div", "row");
      const biz = el("span", "biz", c.business || "Unnamed"); if (c.notes) biz.append(el("small", null, c.notes));
      const pill = el("span", "pill", STAGES[c.stage][0]); pill.style.setProperty("--sc", STAGES[c.stage][1]);
      const contact = el("span", "contact", c.contact || "—"); if (c.channel) contact.append(el("small", null, c.channel));
      r.append(biz, pill, el("span", "next", c.next_action || "—"), el("span", "due " + d.cls, d.text), contact);
      rows.append(r);
    });
}

const RULES = `You are boss, the master of Sonny's team. Look at Sonny's pipeline and tell him exactly what to do today, most urgent first, with a ready-to-send message for everyone he needs to chase.

${BUSINESS}

Follow-up rules: no reply to a pitch, chase 4 days after pitching, then 7 days after that, and after 2 follow-ups suggest closing them. Replied but the next step is unclear: chase after 2 days. Waiting on the client for info (photos, menu, hours): chase after 3 days. Build fee due 7 days after delivery, chase from the day after. £50 maintenance: flag 3 days before it's due, chase if overdue.

Chase messages: 1-2 short, friendly sentences, like a real person texting. No guilt-tripping, and signed "Sonny". For payments be clear and polite, e.g. "Hi Dave, just a heads up the £595 for the site is due today. Bank details are on the invoice. Cheers, Sonny".
${VOICE}

If the pipeline is empty or nothing is due, say so in the headline and suggest the most useful next step (e.g. finding new leads in a Shropshire town and trade Sonny hasn't tried yet).`;

$("todayBtn").addEventListener("click", async () => {
  const out = $("todayOut");
  const prompt = `${RULES}${lessonsText()}

Today is ${today}.
The pipeline (JSON):
${JSON.stringify(pipeline).slice(0, 20000)}

Reply with only JSON in this shape: {"headline": "one sentence", "today": [{"business": "", "action": "what to do", "channel": "", "message": "ready-to-send message, or empty string"}], "soon": [{"business": "", "action": "", "date": "YYYY-MM-DD"}]}`;
  try {
    const r = await ask(prompt, { out, button: $("todayBtn") });
    out.replaceChildren(el("p", null, String(r.headline || "")));
    (Array.isArray(r.today) ? r.today : []).forEach((t) => {
      const title = `${t.business || ""}: ${t.action || ""}`;
      if (t.message) out.append(msgBlock(title, String(t.message), t.channel ? String(t.channel) : ""));
      else out.append(el("p", null, "• " + title));
    });
    const soon = Array.isArray(r.soon) ? r.soon : [];
    if (soon.length) {
      out.append(el("b", null, "Coming up"));
      const ul = el("ul", "issues");
      soon.forEach((s) => ul.append(el("li", null, `${s.business || ""}: ${s.action || ""}${s.date ? " (" + fmt(s.date) + ")" : ""}`)));
      out.append(ul);
    }
  } catch (e) {
    if (e && e.code === "cancelled") { out.replaceChildren(el("p", "note", "Stopped.")); return; }
    out.replaceChildren(el("p", "note err", sampleError(e)));
  }
});

(async () => {
  const db = await dbP;
  renderPipeline();
  if (!db) { $("pipeUpdated").textContent = "Open this page in Claude to see your live pipeline"; $("logNote").textContent = "Logging works when this page is open in Claude."; return; }
  db.doc("pipeline/current").onSnapshot((snap) => { pipeline = snap.exists ? snap.data() : { updated: "", clients: [] }; renderPipeline(); },
    () => { $("pipeUpdated").textContent = "Couldn't load the pipeline. Reload the page."; });
  const upEl = $("updates");
  db.collection("updates").orderBy("created", "desc").limit(50).onSnapshot((snap) => {
    upEl.replaceChildren();
    snap.docs.forEach((d) => {
      const u = d.data();
      const li = el("li");
      li.append(el("span", null, `${u.business}: ${u.event}${u.note ? " (" + u.note + ")" : ""}`));
      const meta = el("small");
      meta.append(el("span", "chip " + (u.status === "applied" ? "applied" : "new"), u.status === "applied" ? "In the pipeline" : "Waiting for Claude Code"), " " + (u.date ? fmt(u.date) : ""));
      li.append(meta);
      if (u.status !== "applied") {
        const x = el("button", "btn small x", "Remove"); x.type = "button";
        x.addEventListener("click", async () => { x.disabled = true; try { await db.doc("updates/" + d.id).delete(); } catch (e) { x.disabled = false; } });
        li.append(x);
      }
      upEl.append(li);
    });
  }, () => { $("logNote").textContent = "Couldn't load your log. Reload the page."; });
  $("logForm").addEventListener("submit", async (ev) => {
    ev.preventDefault();
    const btn = ev.submitter || $("logForm").querySelector("button");
    const note = $("logNote");
    btn.disabled = true; note.textContent = "Saving…";
    try {
      await db.collection("updates").add({ business: $("lBiz").value.trim().slice(0, 200), event: $("lWhat").value, date: $("lDate").value || today,
        note: $("lNote").value.trim().slice(0, 1000), created: new Date().toISOString(), status: "new" });
      $("lBiz").value = ""; $("lNote").value = ""; note.textContent = "Logged. Say \"check my agent pages\" in Claude Code to update the pipeline.";
    } catch (e) { note.textContent = e && e.code === "invalid_argument" ? "Only you can log updates here." : "Couldn't save. Try again."; }
    finally { btn.disabled = false; }
  });
})();
"""

TOOLS = {
  "idea-creator": (IDEA_TOOL, IDEA_JS, "e.g. Always mention I can have a draft ready within a week"),
  "critique": (CRIT_TOOL, CRIT_JS, "e.g. Flag any message over 40 words"),
  "web-builder": (WEB_TOOL, WEB_JS, "e.g. Always put the booking button above the prices"),
  "boss": (PM_TOOL, PM_JS, "e.g. Chase unpaid build fees after 5 days, not 7"),
}

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

for name, a in AGENTS.items():
    tool_html, tool_js, lesson_eg = TOOLS[name]
    rules_html = "".join(
        f"<div><h3>{esc(h)}</h3><ul>{''.join(f'<li>{esc(i)}</li>' for i in items)}</ul></div>" for h, items in a["rules"])
    agent = {"key": a["key"], "c": a["c"], "eye": a["eye"], "id": name}
    page = (SHELL
        .replace("__CSS__", CSS)
        .replace("__TOOL__", tool_html)
        .replace("__AGENT_JS__", tool_js)
        .replace("__AVATAR__", AVATAR_JS)
        .replace("__AGENT_JSON__", json.dumps(agent))
        .replace("__CC_JSON__", json.dumps(a["claude_code"]))
        .replace("__BUSINESS__", json.dumps(BUSINESS))
        .replace("__VOICE__", json.dumps(VOICE))
        .replace("__LOCAL__", json.dumps(LOCAL))
        .replace("__RULES__", rules_html)
        .replace("__LESSON_EG__", esc(lesson_eg))
        .replace("__HQ__", HQ_URL)
        .replace("__TITLE__", {"idea-creator": "Idea Creator", "web-builder": "Web Builder", "critique": "Critique", "boss": "Boss"}[name])
        .replace("__COLOR__", a["c"])
        .replace("__BADGE__", '<span class="badge">MASTER</span>' if a.get("master") else "")
        .replace("__NAME__", name)
        .replace("__ROLE__", esc(a["role"]))
        .replace("__INTRO__", esc(a["intro"])))
    assert "__" not in page.replace("__delete__", ""), (name, [l for l in page.splitlines() if "__" in l][:3])
    with open(os.path.join(HERE, f"{name}.html"), "w") as f:
        f.write(page)
    print("wrote", name)
