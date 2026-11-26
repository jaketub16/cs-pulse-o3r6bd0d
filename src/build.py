#!/usr/bin/env python3
"""CS Pulse Check team page. Clients, health, metrics and ad spend only."""
import json, html, os
E = html.escape
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'index.html')
WEEK = 'Week of Fri Nov 20 to Thu Nov 26, 2026'
BUILT = 'Built Thu Nov 26, 2026, 10:05 Madrid (CET). Covers Fri Nov 20 to Thu morning so far'
TILES = (2, 9, 4)  # replies over 6h, late promises, client calls recorded so far

PRIORITIES = [
  ('William', 'FamCare', 'Reply to Kim about the two videos that stutter: what you found and when fixed files are ready, or ask which device she watched on.', 'Today, Thu Nov 26, morning', 'Kim raised it Mon 14:04. Still no answer, about 23 business hours. Red flag'),
  ('Shane', 'Rigol', 'Send Mike the finished product you promised for Wed and a go-live date, with Jake on cc. Then the recap and his written okay on AD20, AD14 and AD17.', 'Today, Thu Nov 26', 'Finished product missed Wed 18:00. Recap 14 days late, launch 8 business days late'),
  ('Shane', 'DBSync', 'Shut DBSync down: GHL phone number, automations and everything tied to the account. Reply "done" to Jake item by item.', 'Late since Wed night', 'Client has ended. Everything gets turned off the same day'),
  ('Shane', 'Lockton', 'Send Aaron the written answer on automated messages. Ship the updated page and worksheet and email IT about the calendar approval.', 'Today, then before Mon Nov 30', 'Answer was due Tue 18:00, now 2 days late'),
  ('Yona', 'HRG', 'Scott said "Let\'s skip this week". Cancel Friday\'s invite and rebook him with Jake for the week of Dec 1, 9am to 2pm CT.', 'Today, Thu Nov 26', 'Call is tomorrow, Fri Nov 27 17:00 Madrid'),
  ('Shane', 'Workzone', 'Fix the GHL to HubSpot sync and tell Steve when it works.', 'Today, Thu Nov 26', 'Steve still enters every lead by hand (raised Tue and at Wed\'s weekly)'),
]

# (status, client, owner, reason, last touch, next step)
HEALTH = [
  ('r','Rigol','Shane · William','The finished product Shane promised Mike for Wed wasn\'t sent. Launch 8 business days late with no go-live date. Recap 14 days late.','Shane email, Mon Nov 23 18:48 ("finished product in 1-2 days")','Finished product and go-live date to Mike today, with Jake on cc.'),
  ('r','Xplor / FieldEdge','Shane · William','CPL $143.27 (Nov 13 to 19) vs $55 ceiling. 0 booked last week. Day 24 of 30. Garbled AI-text ad turned off Wed night (William).','William email to Jake, Wed Nov 25 22:00 (ad off)','William ships the new page and creative batch. Shane sends Brittany the regenerated creative.'),
  ('r','DBSync','Shane · Jake','Client has ended. Jake sent Joel the next steps Wed night. Shutdown of the account not confirmed yet.','Jake email to Joel, Wed Nov 25 21:30','Shane turns everything off and confirms item by item.'),
  ('r','Dan Greenberg (RGA)','Shane','Lead magnet range and logo swap promised "first thing" Nov 3. 23 days. The live PDF still shows the old range and logo.','Shane email, Tue Nov 3','Send Dan the change today by 12:00, Jake on cc.'),
  ('y','FamCare','William · Shane','Kim\'s report of two stuttering videos has had no answer since Mon 14:04 (red flag). William plans video 2 feedback for George next week, when he\'s back.','William email, Tue Nov 24 19:28 (birthday note)','Reply to Kim this morning.'),
  ('y','Sandler','William · Yona','Michael was upset Wed: Jake\'s sync didn\'t happen (Jake ill) and the bot kept messaging a lead he had turned off. William added the stop tag, sent screenshots and the full sequence the same evening. Michael now says "All good".','William email, Wed Nov 25 19:55 (sequence)','Michael picks a Friday or Tuesday time with Jake. Michael sends feedback on the sequence.'),
  ('y','Lockton','Shane · William · Yona','Launch call Mon Nov 30. Updated page and worksheet due before then. GHL calendars blocked until Lockton IT approves Outlook/Teams. Aaron\'s automated-message question still has no written answer.','Shane email, Tue Nov 24 18:35 (lead magnet)','Written answer to Aaron. Updated assets and IT email before Mon. Calling playbook before launch.'),
  ('y','Workzone','William · Shane · Yona','0 booked calls this week, cost per MQL steady at about $46 to $48. New VSL campaign live Wed at $25/day. GHL to HubSpot sync still broken. "WorkZone" sender name fixed Wed.','William email, Wed Nov 25 22:46 (VSL campaign live)','Shane fixes the HubSpot sync. William revises the SMS sequence and fixes the report bug. Ash books a call with Jake.'),
  ('y','Heal Clinical','William · Shane','Dylan flagged 4 unqualified leads and falling volume. William found broad ads and a new batch not running, paused the broad ads and fixed the batch Wed.','William email, Wed Nov 25 14:51','Watch lead quality daily. Expect normal volume within a week.'),
  ('y','Clockspring','William','About $130 CPL at $100/day. Leads 6, 5, then 3 per week. Broad funnel has stalled.','Weekly report, Fri Nov 20','Ship the problem-focused funnel and freebie, plus new DirectVSL and Freebie creatives.'),
  ('y','Imorgon','William · Yona','Andy sent his first 2 RSNA videos Wed. Weekly skipped for RSNA. Instagram login (2FA to a dead number) still blocks ads on the main account.','William email, Wed Nov 25 19:48 (video feedback)','Edit the 2 videos. Andy records more with more energy. Fix the Instagram login.'),
  ('y','All Tips Matter','William','Opt-in 4.11% vs 10% target. Volume thin.','Weekly report, Fri Nov 20','Send a test lead to confirm forms reach GHL. Book this week\'s call.'),
  ('y','VBO Tickets','William · Shane','Churn risk easing after Jake\'s Nov 13 call. Demos still blocked: leads set DND or take the white paper only. Weekly skipped for Thanksgiving.','William email, Mon Nov 23 20:10','Shane books a 1:1 with Mike. Shannon\'s call cadence ready for Dec 1.'),
  ('y','Evolve','Jake · Yona · William','Ads paused since Nov 4. The 16-week flight ends Nov 30. Wed\'s call with Jake was moved because Jake was ill. Now Wed Dec 2, 16:30 Madrid.','Yona invite, Wed Nov 25 20:52','The Dec 2 call agrees the next step.'),
  ('g','HRG','William · Jake · Yona','Funnel 2 strong and its pipelines are built. Scott asked to skip Friday\'s call with Jake. Rebook for the week of Dec 1.','Jake email to Yona, Wed Nov 25 21:55','Yona rebooks Scott. Shane confirms the Jan 1 LinkedIn start with Scott in writing.'),
  ('g','Aviro360','William · Yona · Jake','Brian\'s call with Stanley, a buyer who booked from our ads, went well. Weekly Mon Nov 30 noon ET. Dec 4 times offered for Jake.','William email, Tue Nov 24 14:58','Brian picks a Dec 4 time. Weekly Mon Nov 30.'),
  ('g','BlueStar Telehealth','William · Shane · Yona','New creatives (Nov 5) took one week from 2 leads to 8 leads, 7 MQLs, 6 booked. Rob lost his mother. He thanked William for the team\'s condolences.','William email, Tue Nov 24 19:28','Keep pausing weak ads. Go gentle with Rob.'),
]

HERO = [
  ('Xplor / FieldEdge','In window','Day 24 of 30 · window ends Wed Dec 2','27','Nov 6 to 19 (William\'s weekly reports; Nov 3 to 5 not in reports). Next update Fri Nov 27','$116.65','Nov 6 to 19 · last week $143.27','6','Likely CPL miss. Leads near pace for about 50. Data is stale (Nov 19); no live GHL key for Xplor','r'),
  ('Workzone','Closed Thu Nov 19','Day 30 reached','58','Oct 21 to Nov 19 (William\'s weekly reports, not checked in GHL)','$54.86','final · ad spend $3,181.88','0','Leads goal hit. CPL over the $40 goal, just inside the $55 ceiling','y'),
  ('Sandler','Closed Fri Nov 6','Day 30 reached','7','final','$194','final, Meta via Windsor','0','Missed','r'),
]
NOT_STARTED = 'Not started yet: Rigol (no launch date; the finished product promised for Wed Nov 25 was not sent), Lockton (launch call Mon Nov 30), Tiger Capital (asset call Tue Dec 1, 16:00 Madrid) and Daniel / City of Angles (kickoff Mon Nov 30). Hero metrics start on launch day.'

TEAM = [
  ('Shane', (4,0.03,27.0,1), (6,0.62,26.63,1), 9, 2, 3, 'No client emails to score Wed. The Rigol finished product and the DBSync shutdown were missed. Proof for 4 items is due today at 12:00.',
   ['Rigol: finished product and go-live date (due Wed Nov 25)','Rigol: recap and Mike\'s written okay (due Nov 12)','Rigol: go-live (due Nov 16)','Lockton: written answer to Aaron (due Tue Nov 24)','DBSync: shutdown, confirm item by item (due Wed Nov 25)','Dan: lead magnet and logo (due Nov 3)','Xplor: regenerated garbled-text creative (due Nov 5)','Xplor: Alyssa follow-up on the chatbot phone number','Anchor Point: Kyle on the mid-December kickoff'],
   ['Proof for the 4 items above (today 12:00)','HRG: confirm the Jan 1 LinkedIn start with Scott (today 12:00)','Workzone: fix the HubSpot sync','LLH: reconnect Facebook in GHL','Lockton: updated assets and IT email (before Mon Nov 30)','Tiger Capital: assets for the Tue Dec 1 call']),
  ('William', (20,0.95,5.93,0), (13,0.0,9.0,1), 0, 1, 4, 'Fast Wed: 6 replies, median 0.12. Sandler handled well. Dylan got a real plan on time. The garbled Xplor ad is off. But Kim is still waiting since Mon (red flag), and Ash waited 5.93, just under the line.',
   [], ['FamCare: reply to Kim on the video playback (red flag)','Workzone: SMS sequence, report bug, handoff sheet','FamCare: video 2 feedback for George (next week)']),
  ('Yona', (10,1.04,4.58,0), (9,1.12,5.88,0), 0, 1, 1, 'No red flags. Rebooked Dave for Wed Dec 2 within hours and calmed Michael after the missed sync.',
   [], ['HRG: rebook Scott for the week of Dec 1','Sandler: lock Michael\'s time once he picks','Anchor Point: chase Kyle on the Dec 14 kickoff']),
]
TEAM_NOTE = 'Emails: cs-log and Jake\'s Gmail, Fri Nov 20 to Thu Nov 26 09:45 (weekend and evening replies count 0 business hours). Previous week = Fri Nov 13 to Thu Nov 19. Client calls = recorded Fathom client calls so far this week.'

MISSED = [
  ('FamCare','William','"Re: This week\'s meeting": Kim reported video playback problems Mon Nov 23 14:04. Reply covered only the holiday. About 23 business hours with no answer on the videos. Red flag.'),
  ('Rigol','Shane','"Re: Discovery Questions": Mike replied Thu Nov 19 07:38 approving the form questions. Answered Mon Nov 23 18:48, 27.0 business hours. Red flag. The promised finished product (Wed) did not go out.'),
]
MISSED_NOTE = 'Two client emails waited more than 6 business hours this week. Closest call Wed: Workzone at 5.93. Send a short holding reply first thing, then the fix.'
WAITING = [
  ('FamCare','William','Kim: two new videos with playback problems. No answer on them since Mon.'),
  ('Rigol','Shane','Mike: finished product and a go-live date, promised for Wed.'),
  ('Lockton','Shane','Aaron\'s question on what stops his leads getting confusing automated messages.'),
  ('Workzone','Shane','Steve: GHL to HubSpot sync broken, leads entered by hand.'),
  ('HRG','Yona','Scott asked to skip Friday\'s call with Jake. Rebook for the week of Dec 1.'),
]

CHURN = [
  ('Xplor','CPL $143 last week, 0 booked, day 24 of 30. Garbled ad only turned off Wed.'),
  ('Rigol','Mike engaged and positive, but the promised finished product didn\'t arrive and there\'s still no go-live date.'),
  ('Sandler','Missed sync and a bot that kept messaging a lead upset Michael Wed. Recovered the same evening. He has complained about too many emails before.'),
  ('Evolve','Ads paused since Nov 4, flight ends Nov 30. Call with Jake moved to Wed Dec 2.'),
  ('Dan Greenberg','23 days without a confirmed change.'),
  ('Heal Clinical','Lead quality dipped. Fix shipped Wed. Watch it this week.'),
]
ASCEND = [
  ('Workzone','Jake wants to meet Ash on more strategies. William sent the booking link Wed. New VSL campaign testing booked calls.'),
  ('Aviro360','Stanley, a buyer who booked straight from our ads, had a good call. Brian is open to meeting Jake in early December.'),
  ('HRG Funnel 2','Funnel 2 strong (7 to 11 leads a week). Rebook Scott with Jake for the week of Dec 1.'),
  ('BlueStar Telehealth','Leads, MQLs and bookings jumped after the Nov 5 creatives. Strong case study.'),
  ('Heal Clinical','Tim asked for help on 2 new projects (Nov 13). Worth a conversation once bookings recover.'),
]
WINS = [
  ('Sandler','William turned a frustrated Michael around in one evening: stop tag, screenshots and the full sequence. Yona followed up and Michael said "All good".'),
  ('Heal Clinical','William sent Dylan a real plan before the deadline: broad ads paused, new batch fixed.'),
  ('Evolve','Yona rebooked Jake\'s call with Dave for Wed Dec 2 within hours.'),
  ('Imorgon','Andy recorded his first 2 RSNA videos. William gave clear feedback the same evening.'),
  ('Workzone','"WorkZone" sender name fixed (William). New VSL campaign live. Weekly held.'),
  ('Xplor','Garbled AI-text ad turned off the same night Jake asked (William).'),
  ('Workzone','Sales training held with Steve. Yona fixed the missing meeting link within a minute.'),
  ('Lockton','Asset review held and launch call booked for Mon Nov 30 (Shane).'),
  ('BlueStar Telehealth','Rob thanked the team for the condolence note (William).'),
]

# Last full Windsor week. License expired; Meta data stops Nov 3.
SPEND = [('BlueStar Telehealth',1557.12,2.47),('HRG (both funnels)',1400.19,1.79),('All Tips Matter',1335.15,1.32),('Clockspring',1242.18,0.54),('Heal Clinical',1056.69,1.32),('Imorgon',837.60,0.88),('FamCare',833.54,1.29),('VBO Tickets',758.37,1.20),('Aviro360',747.01,1.11),('Workzone',691.98,0.53),('Evolve',680.65,0.79),('Sandler',344.25,0.88)]
SPEND_NOW = ['Workzone: new VSL campaign live Wed Nov 25 at $25/day; first campaign now $75/day (William email).','Xplor: $2,292.30 for Nov 13 to 19 at $143.27 CPL (William\'s weekly report).','Workzone: $749.40 for Nov 13 to 19 at $46.84 CPL (William\'s weekly report).','Clockspring: $100/day (call Nov 17).','Imorgon: Letter and Roadmaps at $100/day each (call Nov 18).','Evolve: paused since Nov 4.']

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
 'DBSync':'Client has ended. Shutdown with Shane.',
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
<div class="tile"><b>{TILES[0]}</b><span>replies over 6h</span></div><div class="tile"><b>{TILES[1]}</b><span>late promises</span></div><div class="tile"><b>{TILES[2]}</b><span>client calls so far</span></div></div>
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
    a('<p class="note">Sources: Gmail and cs-log threads Fri Nov 20 to Thu Nov 26 09:45, William\'s weekly reports sent Fri Nov 20 (Nov 13 to 19), Fathom calls to Wed Nov 25, CS Rundown Thu Nov 26, GHL (Aviro360 and FamCare live keys, pulled Fri Nov 20 08:20).</p></section>')
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
    a(f'<p class="note">{E(TEAM_NOTE)}</p></section>')
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
