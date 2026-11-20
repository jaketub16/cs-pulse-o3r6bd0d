#!/usr/bin/env python3
"""CS Pulse Check team page. Clients, health, metrics and ad spend only."""
import json, html, os
E = html.escape
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'index.html')
WEEK = 'Week of Fri Nov 13 to Thu Nov 19, 2026'
BUILT = 'Built Fri Nov 20, 2026, 10:45 Madrid (CET)'

PRIORITIES = [
  ('Shane', 'Rigol', 'Email Mike the call recap, get his written okay on AD20, AD14 and AD17, and give Mike and Jake a new go-live date.', 'Today, Fri Nov 20, 18:00', 'Recap 8 days late, launch 4 business days late'),
  ('William', 'FamCare', 'Send George feedback on video 1 before he leaves. Add Mohamed\'s phone for SMS lead alerts. Get Mark to clear the long Outlook blocks so the VSL calendar shows slots. Check go-famcare.com/vsl against George\'s scripts.', 'Today, Fri Nov 20, 15:00 (feedback) and 18:00', 'Bookings are blocked until Mark\'s calendar is open'),
  ('Shane', 'FamCare', 'Create Mohamed\'s GHL login so he can shadow Mark next week.', 'Today, Fri Nov 20, 18:00', 'George asked for it Thursday'),
  ('Shane', 'Xplor / FieldEdge', 'Confirm the new Meta daily ad spend to Jon in writing. Answer Brittany on raw-data access and the 40% Facebook recommend rating. Bring a plan to get CPL under $55.', 'Late since Nov 11', 'CPL $77.94 vs $55 ceiling, Jon cooling'),
  ('Yona', 'Workzone', 'Send the invite for the rebooked sales training, Tue Nov 24, 19:00 Madrid, and make sure it is on Jake\'s calendar.', 'Today, Fri Nov 20, 12:00', 'Steve was told the invite was set'),
]

# (status, client, owner, reason, last touch, next step)
HEALTH = [
  ('r','DBSync','Jake','Joel has asked 3 times for the two proposals (CRM and text Nov 18, email Nov 19 18:29). No reply yet.','Joel email, Thu Nov 19 18:29 (waiting on us)','Jake replies today. Route anything from DBSync to Jake.'),
  ('r','Rigol','Shane · William','Launch 4 business days late with no new date. Mike\'s discovery questions waited 26.6 business hours.','Shane email, Wed Nov 18 17:38','Recap, written okay and new go-live date to Mike today.'),
  ('r','Xplor / FieldEdge','Shane · William','CPL $77.94 (Nov 6 to 12) vs $55 ceiling. Jon cooling. Meta spend increase unconfirmed since Nov 11.','Shane email, Thu Nov 19 17:57 · no call this week','Written spend confirmation, answer Brittany, CPL plan.'),
  ('r','Evolve','William · Shane','Ads paused since Nov 4 at Dave\'s request. No leads since. Sentiment negative.','Email, Wed Nov 18 14:29','Jake and Dave call today 15:30 Madrid: restart plan or clean wind-down.'),
  ('r','Dan Greenberg (RGA)','Shane','Lead magnet range and logo swap promised "first thing" Nov 3. 17 days, no update.','Shane email, Fri Nov 6 12:49','Ship both and email Dan today.'),
  ('y','Clockspring','William','About $130 CPL at $100/day. Leads 6, 5, then 3 per week. Broad funnel has stalled.','Call, Tue Nov 17','Ship the problem-focused funnel and freebie for next week\'s test, plus new DirectVSL and Freebie creatives.'),
  ('y','Workzone','William · Shane','Day 30 closed Nov 19: 42 leads through Nov 12, CPL $57.92. Likely miss on CPL. Recent run is 12 to 13 leads a week at $46.','Call, Wed Nov 18 · Yona email, Fri Nov 20 02:22','Route leads to Steve Atwood, SMS and Slack lead alerts, fix sender name, rotate sub-1% CTR ads.'),
  ('y','HRG','William','Funnel 1: 0 booked from 4 MQLs. Mellissa waited 9.0 business hours. Meta ad-account error not confirmed fixed.','Call, Wed Nov 18 · William email, Thu Nov 19 00:51','Confirm ads are running, new Funnel 1 creatives, separate Funnel 1 and 2 pipelines.'),
  ('y','FamCare','William · Shane','Mark\'s Outlook blocks hide every booking slot. New VSL page brings fewer leads than the old one. GHL: 4 leads, 2 MQLs, 1 booked.','Call, Thu Nov 19 · William email, Thu Nov 19 23:33','Today\'s four items, then decide old vs new page in the next few days.'),
  ('y','Imorgon','William','Instagram login (2FA to a dead number) blocks ads on the main account. 2 booked calls no-showed.','Call, Wed Nov 18 · William email, Thu Nov 19 17:23','Fix the Instagram login. Compare Letter vs Roadmaps ($100/day each) after 7 days.'),
  ('y','All Tips Matter','William','Opt-in 4.11% vs 10% target. Volume thin. No call this week.','William email, Wed Nov 18 20:05','Send a test lead to confirm forms reach GHL. Book this week\'s call.'),
  ('y','Aviro360','William · Yona','GHL: 2 leads this week (1 the week before), 0 MQLs, 0 calls logged.','Call, Fri Nov 13 · William email, Thu Nov 19 21:57','Brian logs every call in GHL. Read the gate campaign (live Nov 16) after 1 to 2 weeks.'),
  ('y','VBO Tickets','William · Shane','Churn risk easing after Jake\'s Nov 13 call. Demos still blocked: leads set DND or take the white paper only.','Call, Wed Nov 18','Shane books a 1:1 with Mike next week. Have Shannon\'s call cadence ready for Dec 1.'),
  ('y','Heal Clinical','William · Shane','Booked calls down 2 weeks running. "Yes" leads going dark. Opt-in 0.81%.','Call, Mon Nov 16','Confirm the calendar on the VSL page and new Direct VSL creatives shipped Nov 18.'),
  ('y','Sandler','William · Shane','Hero window missed (7 leads, CPL $194), but Michael is engaged and collaborative.','Call, Thu Nov 19','Embedded calendar and 15-minute intro live. Michael rewrites the follow-up sequence.'),
  ('g','BlueStar Telehealth','William · Shane · Yona','New creatives (Nov 5) took one week from 2 leads to 8 leads, 7 MQLs, 6 booked. Rob lost his mother; Yona sent condolences.','Call, Wed Nov 18 · Yona note, Thu Nov 19','Keep pausing weak ads. Fix duplicate company fields in the CRM. Go gentle with Rob.'),
  ('g','Lockton','Shane · William · Yona','Kickoff Nov 16 and tech call Nov 18 done. Assets in build. Aaron positive.','Tech call, Wed Nov 18','Asset review Tue Nov 24, 18:00 Madrid. Shane sends the inbound calling playbook before launch.'),
]

HERO = [
  ('Xplor / FieldEdge','In window','Day 18 of 30 · window ends Wed Dec 2','19','as of Nov 13 (GHL, no live key yet)','$77.94','Nov 6 to 12','12','On pace for about 52 leads, but CPL is over the $55 ceiling','y'),
  ('Workzone','Closed Thu Nov 19','Day 30 reached','42','through Nov 12 (William\'s reports; final count not verified in GHL)','$57.92','through Nov 12 · about $46 since','0','Likely miss on CPL. Leads probably close to 50','r'),
  ('Sandler','Closed Fri Nov 6','Day 30 reached','7','final','$194','final, Meta via Windsor','0','Missed','r'),
]
NOT_STARTED = 'Not started yet: Rigol (no new launch date) and Lockton (ads launch after the Tue Nov 24 asset review). Hero metrics start on launch day.'

TEAM = [
  ('Shane', (6,0.62,26.63,1), (10,0.32,14.98,1), 6, 1, 12, 'Red flag: Rigol, Mike\'s discovery questions, 26.6h.',
   ['Dan: lead magnet and logo (due Nov 3)','HRG: LinkedIn ads test (due Nov 6)','Xplor: regenerate the creative with garbled AI text (due Nov 5)','Xplor: confirm the higher Meta spend to Jon (since Nov 11)','Rigol: recap and Mike\'s written okay (due Nov 12)','Rigol: go-live (due Nov 16)'],
   ['FamCare: Mohamed\'s GHL login (today 18:00)']),
  ('William', (13,0.0,9.0,1), (9,1.25,5.05,0), 0, 2, 10, 'Red flag: HRG, Mellissa\'s Outlook and GHL questions, 9.0h.',
   [], ['FamCare: video 1 feedback to George (today 15:00)','FamCare: Mohamed\'s SMS lead alerts (today 18:00)','Workzone: Steve\'s SMS alert and webhook (waiting on Ash\'s phone and URL)']),
  ('Yona', (9,1.12,5.88,0), (7,0.52,2.08,0), 0, 1, 0, 'No red flags. Slowest reply 5.88h, close to the 6h line.',
   [], ['Workzone: training invite on Jake\'s calendar (today 12:00)']),
]

MISSED = [
  ('Rigol','Shane','Mike sent his discovery questions Fri Nov 13 at 23:21. Shane answered Wed Nov 18 at 17:38. 26.6 business hours.'),
  ('HRG','William','Mellissa emailed Mon Nov 16 at 22:39 about a missing Outlook appointment and 4 GHL questions. William replied Tue Nov 17 at 20:41. 9.0 business hours.'),
]
MISSED_NOTE = 'Both only showed up as quoted text inside later replies. Reply on the thread itself so it is counted on time.'
WAITING = [
  ('DBSync','Jake','Joel asked for the two proposals 3 times. Last ask Thu Nov 19 18:29: "Can I expect something this week?"'),
  ('Xplor','Shane','Jon: confirmation of the higher Meta spend, open since Nov 11. Brittany: raw-data access and the 40% recommend rating.'),
  ('FamCare','William','George is waiting on video 1 feedback before he records videos 2 to 4.'),
  ('Dan Greenberg','Shane','Lead magnet range and logo swap, no update since Nov 6.'),
  ('Workzone','Yona','Steve was told the training invite was set. It is not on Jake\'s calendar yet.'),
]

CHURN = [
  ('DBSync','Joel upset and escalating. Jake owns it.'),
  ('Evolve','Ads paused 16 days, sentiment negative. Today\'s call decides restart or wind-down.'),
  ('Xplor','Jon cooling, CPL over ceiling, promises open.'),
  ('Rigol','Mike patient but still waiting on a date.'),
  ('Dan Greenberg','17 days without the promised change.'),
]
ASCEND = [
  ('BlueStar Telehealth','Leads, MQLs and bookings jumped after the Nov 5 creatives. Steve has 4 of their own prospects at proposal stage, 2 targeted by Dec 1. Strong case study.'),
  ('HRG Funnel 2','Calendar on the VSL page took booking rate from 5 to 6% up to 16%. Holding 7 to 11 leads a week.'),
  ('Workzone','12 to 13 leads a week at $46 CPL, A2P done, calendar booking. Ash smoothed over after the day-30 email.'),
  ('Sandler','Michael is booking a consult with Jake himself.'),
  ('Heal Clinical','Tim asked for help on 2 new projects (Nov 13). Worth a conversation once bookings recover.'),
]
WINS = [
  ('FamCare','George recorded video 1 of 4, the VSL page fix went live Thu, and Mohamed is onboarding as the lead qualifier.'),
  ('BlueStar','New creatives: 8 leads, 7 MQLs, 6 booked in the week after Nov 5, with a strong show rate.'),
  ('Imorgon','The Letter page and campaign went live Wed Nov 18. Andy recorded RSNA videos.'),
  ('Workzone','A2P approved, SMS alerts unlocked, Steve Atwood set as the AE with dashboard access.'),
  ('Sandler','Michael agreed to an embedded calendar and a 15-minute intro, and will rewrite the follow-up in his own voice.'),
  ('Lockton','Kickoff and tech setup done in 3 days. Aaron positive.'),
  ('Team','12 recorded client calls this week. William\'s median reply was 0.0 business hours on 13 emails.'),
]

# Last full Windsor week. License expired; Meta data stops Nov 3.
SPEND = [('BlueStar Telehealth',1557.12,2.47),('HRG (both funnels)',1400.19,1.79),('All Tips Matter',1335.15,1.32),('Clockspring',1242.18,0.54),('Heal Clinical',1056.69,1.32),('Imorgon',837.60,0.88),('FamCare',833.54,1.29),('VBO Tickets',758.37,1.20),('Aviro360',747.01,1.11),('Workzone',691.98,0.53),('Evolve',680.65,0.79),('Sandler',344.25,0.88)]
SPEND_NOW = ['Clockspring: $100/day (call Nov 17).','Imorgon: Letter and Roadmaps at $100/day each for one week (call Nov 18).','Workzone: $825.75 for Nov 6 to 12 at $58.98 CPL (William\'s client report).','Evolve: paused since Nov 4.']

COMPLIANCE = {
 'VBO Tickets':'Courtney is calling, but calls are short and the one booking was cancelled.',
 'Workzone':'No calls logged in GHL. Outreach is email only.',
 'Xplor / FieldEdge':'No calls logged in GHL. Email only, none booked.',
 'Aviro360':'16 leads and 1 call. Leads are not being worked.',
 'FamCare':'Heavy dialing and 7 bookings, but 6 no-shows.',
 'HRG':'Strongest follow-up in the group. 5 booked, 1 showed.',
 'Clockspring':'No calls logged. 3 booked, none showed.',
 'Imorgon':'No calls logged. 5 booked and confirmed.',
 'All Tips Matter':'Calling, but 4 of 7 bookings no-showed.',
 'Sandler':'Solid calling. 3 booked, 1 showed.',
 'Rigol':'Not launched.',
 'DBSync':'Handled by Jake.',
}

def light(s): return {'r':'Red','y':'Yellow','g':'Green'}[s]
def f2(v): return f'{v:g}'

def build():
    atd = json.load(open(os.path.join(HERE, 'atd_2026-11-13.json')))
    H = []
    a = H.append
    cnt = {k: sum(1 for h in HEALTH if h[0]==k) for k in 'ryg'}
    a(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow, noarchive"><meta name="googlebot" content="noindex, nofollow">
<title>Aletto CS Pulse Check · {WEEK}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body><main>''')
    a(f'''<header class="hero glass"><div class="brand">aletto<span>.</span></div><div class="eyebrow">CS Pulse Check · Shane, William, Yona</div>
<h1>{WEEK}</h1><p class="muted">Madrid time (CET). {BUILT}. Older data is marked with its date.</p>
<div class="tiles"><div class="tile"><b class="c-r">{cnt['r']}</b><span>red</span></div><div class="tile"><b class="c-y">{cnt['y']}</b><span>yellow</span></div><div class="tile"><b class="c-g">{cnt['g']}</b><span>green</span></div>
<div class="tile"><b>2</b><span>replies over 6h</span></div><div class="tile"><b>6</b><span>late promises</span></div><div class="tile"><b>12</b><span>client calls</span></div></div>
<nav><a href="#prio">Priorities</a><a href="#health">Health</a><a href="#hero-m">Hero metrics</a><a href="#team">Team</a><a href="#emails">Emails</a><a href="#risk">Risk and growth</a><a href="#wins">Wins</a><a href="#spend">Ad spend</a><a href="#atd">All-time</a></nav></header>''')
    # priorities
    a('<section id="prio"><h2>This week\'s 5 priorities</h2><p class="muted">Reply on the team thread the moment each one is done.</p>')
    for i,(o,c,t,d,why) in enumerate(PRIORITIES,1):
        a(f'<div class="glass card prio"><div class="row"><span class="num">{i}</span><span class="pill">{E(o)}</span><span class="client">{E(c)}</span></div><p class="big">{E(t)}</p><div class="meta"><span><b>Due</b> {E(d)}</span><span><b>Why</b> {E(why)}</span></div></div>')
    a('</section>')
    # health
    a(f'<section id="health"><h2>Client health board</h2><p class="muted">{len(HEALTH)} active clients, red first. One reason each. Status reflects results, client mood and our follow-through this week.</p>')
    for s,c,o,r,lt,nx in HEALTH:
        a(f'<div class="glass card hc b-{s}"><div class="row"><span class="dot d-{s}"></span><span class="client">{E(c)}</span><span class="tag t-{s}">{light(s)}</span></div><p class="big">{E(r)}</p><dl><dt>Owner</dt><dd>{E(o)}</dd><dt>Last touch</dt><dd>{E(lt)}</dd><dt>Next</dt><dd>{E(nx)}</dd></dl></div>')
    a('<p class="note">Sources: Gmail and cs-log threads, Fathom calls Nov 13 to 19, GHL (Aviro360 and FamCare live keys, pulled Fri Nov 20 08:20), CEO client report built Fri Nov 20.</p></section>')
    # hero
    a('<section id="hero-m"><h2>First-month hero metrics</h2><p class="muted">First 30 days after launch: 50+ leads, CPL $40 goal, $55 ceiling. Leads from GHL or client reports, never from Meta.</p>')
    for c,st,day,ld,ldn,cpl,cpln,left,verdict,s in HERO:
        a(f'<div class="glass card b-{s}"><div class="row"><span class="client">{E(c)}</span><span class="tag t-{s}">{E(st)}</span></div><p class="muted">{E(day)}</p><div class="kpis"><div><b>{E(ld)}<small>/50</small></b><span>leads · {E(ldn)}</span></div><div><b>{E(cpl)}</b><span>CPL · {E(cpln)}</span></div><div><b>{E(left)}</b><span>days left</span></div></div><p class="big">{E(verdict)}</p></div>')
    a(f'<p class="note">{E(NOT_STARTED)}</p></section>')
    # team
    a(f'<section id="team"><h2>Team scorecard</h2><p class="muted">{WEEK}. Business hours, Mon to Fri. Red flag = a client reply over 6 business hours. Previous week in grey.</p>')
    for n,cur,prev,late,today,calls,flag,latel,todayl in TEAM:
        def cmp(i, lower_better=True):
            c,p=cur[i],prev[i]
            if c==p: return 'same'
            return ('better' if (c<p)==lower_better else 'worse')
        a(f'<div class="glass card"><div class="row"><span class="client">{E(n)}</span></div><div class="kpis k4"><div><b>{cur[0]}</b><span>emails · prev {prev[0]}</span></div><div><b>{f2(cur[1])}h</b><span>median · prev {f2(prev[1])}h</span></div><div><b>{f2(cur[2])}h</b><span>slowest · prev {f2(prev[2])}h</span></div><div><b class="{"c-r" if cur[3] else "c-g"}">{cur[3]}</b><span>red flags · prev {prev[3]}</span></div></div>'
          f'<div class="kpis k3"><div><b class="{"c-r" if late else "c-g"}">{late}</b><span>late promises</span></div><div><b>{today}</b><span>due today</span></div><div><b>{calls}</b><span>client calls (Fathom)</span></div></div><p class="big">{E(flag)}</p>')
        if latel: a('<div class="sub">Late</div><ul>'+''.join(f'<li>{E(x)}</li>' for x in latel)+'</ul>')
        if todayl: a('<div class="sub">Due today or waiting</div><ul>'+''.join(f'<li>{E(x)}</li>' for x in todayl)+'</ul>')
        a('</div>')
    a('<p class="note">Emails: cs-log and Jake\'s Gmail, Fri Nov 13 to Thu Nov 19. The Wed and Thu daily runs failed, so Nov 17 to 19 were rebuilt in one pass Fri Nov 20. No day is missing. Client calls = recorded Fathom client calls attended Nov 13 to 19.</p></section>')
    # emails
    a('<section id="emails"><h2>Missed or late emails</h2>')
    for c,o,t in MISSED: a(f'<div class="glass card b-r"><div class="row"><span class="client">{E(c)}</span><span class="pill">{E(o)}</span></div><p class="big">{E(t)}</p></div>')
    a(f'<p class="note">{E(MISSED_NOTE)}</p><h3>Threads waiting on us</h3>')
    for c,o,t in WAITING: a(f'<div class="glass card line"><div class="row"><span class="client">{E(c)}</span><span class="pill">{E(o)}</span></div><p>{E(t)}</p></div>')
    a('</section>')
    # risk & growth
    a('<section id="risk"><h2>Churn risk</h2>')
    for c,t in CHURN: a(f'<div class="glass card line b-r"><span class="client">{E(c)}</span><p>{E(t)}</p></div>')
    a('<h2>Growth signals worth a meeting</h2>')
    for c,t in ASCEND: a(f'<div class="glass card line b-g"><span class="client">{E(c)}</span><p>{E(t)}</p></div>')
    a('</section>')
    a('<section id="wins"><h2>Wins of the week</h2>')
    for c,t in WINS: a(f'<div class="glass card line"><span class="client">🏆 {E(c)}</span><p>{E(t)}</p></div>')
    a('</section>')
    # spend
    a('<section id="spend"><h2>Ad spend</h2><p class="muted"><b class="c-y">Stale:</b> the Windsor license expired, so Meta ad spend and CTR stop at Nov 3. This is the last full week, Mon Oct 27 to Sun Nov 2. Leads always come from GHL, not from here.</p><div class="glass card"><div class="spend">')
    for c,s,ctr in SPEND:
        a(f'<div class="sp"><span>{E(c)}</span><b>${s:,.2f}</b><small class="{"c-r" if ctr<1 else ""}">CTR {ctr:.2f}%</small></div>')
    a('</div></div><h3>Known this week</h3><ul class="plain">'+''.join(f'<li>{E(x)}</li>' for x in SPEND_NOW)+'</ul><p class="note">CTR under 1% in red: rotate those creatives first.</p></section>')
    # atd
    a('<section id="atd"><h2>Accounts to date (all-time history)</h2><p class="muted">All-time, from each client\'s own GHL sub-account, through Fri Nov 13, 2026. Not this week. The verdict line is lead follow-up from GHL, Oct 21 to Nov 12.</p>')
    for c in atd['clients']:
        b, sh = c['booked'], c['showed']
        rate = f'{sh/b*100:.1f}%'.replace('.0%','%') if b else 'n/a'
        verdict = COMPLIANCE.get(c['name'],'')
        lk = 'unverified' if c['leadsKind']=='unverified' else 'net'
        months = ' · '.join(f"{m['label'].replace(chr(8211),' to ').replace(' 26','')}: {m['n']}" for m in (c.get('months') or [])[-4:])
        a(f'<div class="glass card"><div class="row"><span class="client">{E(c["name"])}</span><span class="muted small">since {E(c["first"])}</span></div><div class="kpis k4"><div><b>{c["leads"]:,}</b><span>leads ({lk})</span></div><div><b>{c["calls"]:,}</b><span>calls</span></div><div><b>{b}</b><span>booked</span></div><div><b>{rate}</b><span>show rate · {sh} showed, {c["noshow"]} no-show</span></div></div>'
          + (f'<p class="muted small">Recent months: {E(months)}</p>' if months else '') + (f'<p class="big">{E(verdict)}</p>' if verdict else '') + '</div>')
    a('<p class="note">Heal Clinical, Evolve and BlueStar Telehealth are not tracked in GHL. Lockton has no sub-account yet. Answered calls and some call totals may include staff or test activity.</p></section>')
    a('<footer class="muted small">Aletto · CS Pulse Check · team only, not for clients.</footer></main></body></html>')
    open(OUT,'w').write('\n'.join(H))
    print('wrote', OUT)

CSS = r'''
:root{--bg:#07080A;--tx:#F5F6F7;--mu:#9AA0AA;--mu2:#6B7079;--line:rgba(255,255,255,.10);--glass:rgba(255,255,255,.045);--red:#FF4438;--grn:#3ECF6E;--yel:#F5B544}
*{box-sizing:border-box;margin:0;padding:0}
html{-webkit-text-size-adjust:100%}
body{background:radial-gradient(900px 600px at 100% -10%,rgba(255,68,56,.14),transparent 60%),radial-gradient(700px 500px at -20% 30%,rgba(90,120,255,.08),transparent 60%),var(--bg);background-attachment:fixed;color:var(--tx);font:400 17px/1.5 Geist,system-ui,-apple-system,sans-serif;-webkit-font-smoothing:antialiased}
main{max-width:760px;margin:0 auto;padding:10px 10px 40px}
.glass{background:var(--glass);border:1px solid var(--line);border-radius:18px;backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px)}
.hero{padding:20px 16px;margin-bottom:8px}
.brand{font:800 22px/1 Geist;letter-spacing:-.04em}.brand span{color:var(--red)}
.eyebrow{margin-top:14px;font:600 12px/1.3 "JetBrains Mono",monospace;letter-spacing:.1em;text-transform:uppercase;color:var(--mu)}
h1{font-size:32px;line-height:1.08;letter-spacing:-.03em;margin:8px 0 6px;font-weight:750}
h2{font-size:26px;letter-spacing:-.02em;margin:30px 4px 4px;font-weight:700}
h3{font-size:19px;margin:18px 4px 8px}
.muted{color:var(--mu)}.small{font-size:14px}.note{color:var(--mu2);font-size:14px;margin:8px 4px}
section>.muted{margin:0 4px 10px}
.tiles{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:16px}
.tile{background:rgba(255,255,255,.04);border:1px solid var(--line);border-radius:14px;padding:10px}
.tile b{display:block;font:700 30px/1 Geist}.tile span{font-size:13px;color:var(--mu)}
nav{display:flex;gap:6px;overflow-x:auto;margin-top:14px;padding-bottom:2px;scrollbar-width:none}
nav a{flex:none;color:var(--tx);text-decoration:none;font-size:14px;border:1px solid var(--line);border-radius:999px;padding:7px 12px;background:rgba(255,255,255,.03)}
.card{padding:14px 14px;margin:8px 0;border-left-width:4px}
.b-r{border-left-color:var(--red)}.b-y{border-left-color:var(--yel)}.b-g{border-left-color:var(--grn)}
.row{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.client{font-weight:700;font-size:19px;letter-spacing:-.01em}
.big{font-size:17px;margin-top:6px}
.card p{margin-top:6px}
.num{font:700 15px/1 "JetBrains Mono";background:var(--red);color:#fff;border-radius:8px;padding:5px 8px}
.pill{font:600 12px/1 "JetBrains Mono",monospace;letter-spacing:.05em;text-transform:uppercase;border:1px solid var(--line);border-radius:999px;padding:5px 9px;color:var(--mu)}
.tag{margin-left:auto;font:600 12px/1 "JetBrains Mono",monospace;text-transform:uppercase;border-radius:999px;padding:5px 9px}
.t-r{background:rgba(255,68,56,.16);color:#FF7A70}.t-y{background:rgba(245,181,68,.15);color:var(--yel)}.t-g{background:rgba(62,207,110,.14);color:var(--grn)}
.dot{width:11px;height:11px;border-radius:50%}.d-r{background:var(--red)}.d-y{background:var(--yel)}.d-g{background:var(--grn)}
.c-r{color:#FF6A5F}.c-y{color:var(--yel)}.c-g{color:var(--grn)}
.meta{display:grid;gap:4px;margin-top:10px;font-size:15px;color:var(--mu)}.meta b{color:var(--tx);font-weight:600;margin-right:4px}
dl{display:grid;grid-template-columns:auto 1fr;gap:4px 10px;margin-top:10px;font-size:15px}dt{color:var(--mu2);font-weight:600}dd{color:#D9DCE0}
.kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:10px}.kpis.k4{grid-template-columns:repeat(2,1fr)}
.kpis div{background:rgba(255,255,255,.035);border-radius:12px;padding:10px}
.kpis b{display:block;font:700 24px/1.1 Geist}.kpis b small{font-size:15px;color:var(--mu)}.kpis span{font-size:13px;color:var(--mu);line-height:1.3;display:block;margin-top:3px}
.sub{margin-top:12px;font:600 12px/1 "JetBrains Mono";text-transform:uppercase;letter-spacing:.08em;color:var(--mu2)}
ul{margin:6px 0 0 20px}li{margin:3px 0;font-size:16px}ul.plain{margin:0 4px 0 24px}
.line p{margin-top:2px}
.spend{display:grid;gap:2px}
.sp{display:grid;grid-template-columns:1fr auto;gap:0 10px;padding:8px 0;border-bottom:1px solid var(--line)}.sp:last-child{border:0}
.sp b{font-family:"JetBrains Mono";font-size:16px}.sp small{grid-column:1/3;font-size:13px;color:var(--mu)}
footer{margin:30px 4px 0}
@media(min-width:700px){main{padding:24px 18px 60px}h1{font-size:40px}.tiles{grid-template-columns:repeat(6,1fr)}.kpis.k4{grid-template-columns:repeat(4,1fr)}.card{padding:18px 20px}}
'''
if __name__ == '__main__':
    build()
