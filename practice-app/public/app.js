"use strict";
// Algebra II Practice: one page for students, the teacher and administrators.
// Data comes from /api/*; answer keys stay on the server for students.

const LETTERS = "ABCDEF";
const CATS = { SO: "Structure & Operations", EI: "Equations & Inequalities", FN: "Functions", SP: "Statistics & Probability" };
const base = s => s.split(".").slice(0, 5).join(".");
const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const lc = s => s.replace(/^[A-Z][a-z]/, m => m.toLowerCase());
const pct = (c, n) => n ? Math.round(100 * c / n) : 0;
const fmtDay = d => new Date(d + "T12:00:00").toLocaleDateString("en-US", { month: "short", day: "numeric" });
const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
const fillColor = p => p < 50 ? "var(--crit)" : p < 70 ? "var(--warn)" : p < 85 ? "var(--ok)" : "var(--good)";
const heatClass = (c, n) => n < 3 ? "h0" : (p => p < 50 ? "h1" : p < 70 ? "h2" : p < 85 ? "h3" : "h4")(pct(c, n));

const app = document.getElementById("app");
const ui = {
  me: null, bank: null, ITEM: {}, STD: {}, view: null, msg: "", err: "",
  t: null, cls: null, student: null, made: null, cardsFor: null,
  s: null, practice: { cat: "ALL", std: "ALL" }, run: null,
  admin: null, bankf: { cat: "ALL", std: "ALL", type: "ALL", q: "", page: 0 },
};

// ---------- network
async function api(path, body) {
  const opt = body ? { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) } : {};
  const r = await fetch(path, { credentials: "same-origin", cache: "no-store", ...opt });
  let data = {};
  try { data = await r.json(); } catch (e) {}
  if (r.status === 401 && path !== "/api/auth") { ui.me = null; render(); throw new Error(data.error || "Please sign in again."); }
  if (!r.ok) throw new Error(data.error || "Something went wrong. Try again.");
  return data;
}
async function act(path, body, okMsg) {
  ui.err = ""; ui.msg = "";
  try { const r = await api(path, body); if (okMsg) ui.msg = okMsg; return r; }
  catch (e) { ui.err = e.message; render(); return null; }
}

// ---------- start
async function boot() {
  try { ui.me = await api("/api/auth"); } catch (e) { ui.me = { signedIn: false }; ui.err = e.message; }
  if (ui.me.signedIn) await enter();
  render();
}
async function enter() {
  if (!ui.bank) {
    ui.bank = await api("/api/bank");
    ui.ITEM = Object.fromEntries(ui.bank.items.map(q => [q.id, q]));
    ui.STD = Object.fromEntries(ui.bank.standardList.map(s => [s.code, s]));
  }
  if (ui.me.role === "teacher") { ui.view = ui.view || "overview"; await loadTeacher(); }
  else if (ui.me.role === "student") { ui.view = "home"; await loadStudent(); }
  else { ui.view = "summary"; ui.admin = await api("/api/admin"); }
}
async function loadTeacher(classId) {
  const id = classId ?? ui.cls;
  ui.t = await api("/api/teacher" + (id ? `?classId=${id}` : ""));
  ui.cls = ui.t.classId;
}
async function loadStudent() { ui.s = await api("/api/student"); }

// ---------- math
function typeset() {
  if (window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise([app]).catch(() => {});
}
window.typesetApp = typeset;

// ---------- render
function render() {
  const nav = document.getElementById("nav"), who = document.getElementById("whoami");
  if (!ui.me || !ui.me.signedIn) {
    nav.innerHTML = ""; who.innerHTML = installBtn();
    app.innerHTML = viewSignIn();
    wireInstall();
    return;
  }
  const tabs = ui.me.role === "teacher"
    ? [["overview", "Overview"], ["classes", "Classes & codes"], ["bank", "Question bank"]]
    : ui.me.role === "admin" ? [["summary", "Results"], ["bank", "Question bank"]] : [];
  nav.innerHTML = ui.run ? "" : tabs.map(([k, v]) => `<button type="button" data-view="${k}" aria-pressed="${ui.view === k}">${v}</button>`).join("");
  const roleName = { teacher: "Teacher", admin: "Administrator", student: "Student" }[ui.me.role];
  who.innerHTML = `${installBtn()}<span>${esc(ui.me.label || roleName)}${ui.me.className ? " · " + esc(ui.me.className) : ""}</span><button type="button" class="btn quiet small" data-signout>Sign out</button>`;
  wireInstall();
  let h = "";
  if (ui.err) h += `<p class="error" role="alert">${esc(ui.err)}</p>`;
  if (ui.msg) h += `<p class="okmsg" role="status">${esc(ui.msg)}</p>`;
  if (ui.run) h += viewRun();
  else if (ui.me.role === "student") h += viewStudent();
  else if (ui.view === "bank") h += viewBank();
  else if (ui.me.role === "teacher") h += ui.view === "classes" ? viewClasses() : viewTeacher();
  else h += viewAdmin();
  app.innerHTML = h;
  typeset();
}

// ---------- sign in and first-time setup
function viewSignIn() {
  if (ui.setup) {
    return `<div class="signin"><div><div class="eyebrow">First-time setup</div><h1>Create the teacher code</h1></div>
      <div class="panel">${ui.setupCode
        ? `<p>This is your teacher code. Write it down and keep it private: it is the only way to manage classes and student codes.</p><div class="bigcode">${esc(ui.setupCode)}</div><button type="button" class="btn" data-continue>Continue</button>`
        : `<p class="muted">Enter the setup key you added to Vercel as <span class="mono">SETUP_KEY</span>. This works only once, before any teacher code exists.</p>
          <form id="setup-form" class="stack"><label for="setup-key">Setup key</label><input type="password" id="setup-key" class="field" autocomplete="off" required style="font:inherit;padding:10px;border:1px solid var(--line);border-radius:8px;background:var(--surface);color:var(--ink)">
          ${ui.err ? `<p class="error" role="alert">${esc(ui.err)}</p>` : ""}<button class="btn" type="submit">Create teacher code</button></form>`}</div>
      ${ui.setupCode ? "" : `<button type="button" class="linkbtn" data-setup="0" style="color:var(--accent)">Back to sign in</button>`}</div>`;
  }
  return `<div class="signin"><div><div class="eyebrow">Welcome</div><h1>Sign in with your code</h1>
      <p class="muted">Your teacher gives you an 8-character code. You do not need an email or password.</p></div>
    <form id="signin-form" class="panel stack"><label for="code">Your code</label>
      <input id="code" class="codebox" autocomplete="off" autocapitalize="characters" spellcheck="false" inputmode="text" maxlength="12" placeholder="ABCD-2345" required>
      ${ui.err ? `<p class="error" role="alert">${esc(ui.err)}</p>` : ""}
      <button class="btn" type="submit">Sign in</button></form>
    <p class="hint">On a phone, use your browser's Share or menu button and choose “Add to Home Screen” to keep the app one tap away.</p>
    ${ui.me && ui.me.setupNeeded ? `<button type="button" class="linkbtn" data-setup="1" style="color:var(--accent)">First-time setup for the teacher</button>` : ""}</div>`;
}

// ---------- install as an app
let installEvt = null;
window.addEventListener("beforeinstallprompt", e => { e.preventDefault(); installEvt = e; render(); });
function installBtn() { return installEvt ? `<button type="button" class="btn ghost small" id="install-btn">Install app</button>` : ""; }
function wireInstall() {
  const b = document.getElementById("install-btn");
  if (b) b.onclick = async () => { installEvt.prompt(); try { await installEvt.userChoice; } catch (e) {} installEvt = null; render(); };
}
if ("serviceWorker" in navigator) navigator.serviceWorker.register("/sw.js").catch(() => {});

// ---------- shared pieces
function bar(label, c, n) {
  const p = pct(c, n);
  return `<div class="bar"><span class="lab" title="${esc(label)}">${esc(label)}</span><span class="track"><span class="fill" style="width:${p}%;background:${fillColor(p)}"></span></span><span class="num">${p}% · ${n}</span></div>`;
}
const stdName = code => ui.STD[code]?.name || code;
const errLabel = e => ui.bank.errorTypes?.[e] || "";

// ---------- teacher analysis
function classStudents() { return ui.t.users.filter(u => u.role === "student" && u.classId === ui.cls); }
function rows() { return ui.t.answers.map(a => ({ uid: a[0], qid: a[1], day: a[2], ok: !!a[3], err: a[4], aid: a[5] })); }
function analyze() {
  const per = {};
  for (const a of rows()) {
    const q = ui.ITEM[a.qid]; if (!q) continue;
    const st = base(q.standard);
    const p = per[a.uid] ||= { n: 0, c: 0, std: {}, err: {}, days: new Set() };
    p.n++; if (a.ok) p.c++; p.days.add(a.day);
    const s = p.std[st] ||= { n: 0, c: 0, days: new Set() };
    s.n++; if (a.ok) s.c++; s.days.add(a.day);
    if (!a.ok && a.err && errLabel(a.err)) { const x = p.err[a.err] ||= { n: 0, std: {} }; x.n++; x.std[st] = (x.std[st] || 0) + 1; }
  }
  return per;
}
function groups(per) {
  const R = ui.t.rules, flags = {};
  const active = new Set(classStudents().filter(s => s.active).map(s => s.id));
  for (const [uid, p] of Object.entries(per)) {
    if (!active.has(+uid)) continue;
    for (const [st, s] of Object.entries(p.std)) {
      if (s.n >= R.minN && s.days.size >= R.minDays && pct(s.c, s.n) < R.cut) (flags[st] ||= {})[uid] = { kind: "acc", n: s.n, c: s.c };
    }
    for (const [e, x] of Object.entries(p.err)) {
      if (x.n >= R.errN) {
        const st = Object.entries(x.std).sort((a, b) => b[1] - a[1])[0][0];
        (flags[st] ||= {})[uid] ||= { kind: "err", n: p.std[st]?.n || 0, c: p.std[st]?.c || 0 };
      }
    }
  }
  const dismissed = new Set(ui.t.dismissed.filter(d => d[0] === ui.cls).map(d => d[1]));
  return Object.entries(flags).filter(([st]) => !dismissed.has(st)).map(([st, who]) => {
    const ec = {};
    for (const uid of Object.keys(who)) for (const [e, x] of Object.entries(per[uid].err)) if (x.std[st]) ec[e] = (ec[e] || 0) + x.std[st];
    return { st, who, topErr: Object.entries(ec).sort((a, b) => b[1] - a[1]).slice(0, 2) };
  }).sort((a, b) => Object.keys(b.who).length - Object.keys(a.who).length || a.st.localeCompare(b.st));
}
function suggestSet(g) {
  const seen = new Set(rows().filter(a => g.who[a.uid]).map(a => a.qid));
  const top = new Set(g.topErr.map(e => e[0]));
  const score = q => (q.errors.some(e => top.has(e)) ? 2 : 0) + (seen.has(q.id) ? 0 : 1);
  return ui.bank.items.filter(q => base(q.standard) === g.st).sort((a, b) => score(b) - score(a) || (Math.random() - .5)).slice(0, 10).map(q => q.id);
}
function reteachNote(g) {
  const name = lc(stdName(g.st)), err = g.topErr[0] ? errLabel(g.topErr[0][0]) : "";
  return err
    ? `Reteach ${name} with one worked example built around the most common error: “${err}.” Have students explain that step aloud before they start the set.`
    : `Reteach ${name} with a worked example and two guided problems, then assign the set.`;
}

function viewTeacher() {
  const t = ui.t;
  if (!t.classes.length) {
    return `<div class="eyebrow">Teacher</div><h1>Welcome</h1><div class="empty" style="margin-top:16px">Start by adding a class and making student codes. <button type="button" class="btn" data-view="classes" style="margin-left:8px">Add a class</button></div>`;
  }
  const cls = t.classes.find(c => c.id === ui.cls);
  const studs = classStudents();
  const per = analyze();
  const gs = groups(per);
  const all = rows();
  const weekStart = new Date(Date.parse(t.today + "T12:00:00Z") - 6 * 864e5).toISOString().slice(0, 10);
  const week = all.filter(a => a.day >= weekStart);
  const flagged = new Set(gs.flatMap(g => Object.keys(g.who)));
  const assigned = t.assignments.filter(a => a.classId === ui.cls);
  const assignedStd = new Set(assigned.map(a => a.standard));
  const R = t.rules;
  let h = `<div class="section-head"><div><div class="eyebrow">Teacher overview</div><h1>${esc(cls.name)}</h1></div>
    <div class="tabs" role="group" aria-label="Class">${t.classes.map(c => `<button type="button" data-cls="${c.id}" aria-pressed="${c.id === ui.cls}">${esc(c.name)}</button>`).join("")}</div></div>`;
  if (!studs.length) return h + `<div class="empty" style="margin-top:16px">This class has no student codes yet. <button type="button" class="btn" data-view="classes" style="margin-left:8px">Make codes</button></div>`;
  h += `<div class="kpis" style="margin-top:16px">
    <div class="kpi"><div class="eyebrow">Students</div><div class="v">${studs.filter(s => s.active).length}</div><div class="s">${new Set(week.map(a => a.uid)).size} practiced in the last 7 days</div></div>
    <div class="kpi"><div class="eyebrow">Questions answered</div><div class="v">${all.length.toLocaleString()}</div><div class="s">${week.length.toLocaleString()} in the last 7 days</div></div>
    <div class="kpi"><div class="eyebrow">Class accuracy</div><div class="v">${all.length ? pct(all.filter(a => a.ok).length, all.length) + "%" : "–"}</div><div class="s">all practice so far</div></div>
    <div class="kpi alert"><div class="eyebrow">Students flagged</div><div class="v">${flagged.size}</div><div class="s">across ${gs.length} standard${gs.length === 1 ? "" : "s"}</div></div></div>
  <section class="section"><div class="section-head"><h2>Needs attention</h2><span class="muted">Nothing is assigned until you approve it.</span></div>
  <details class="rules"><summary>Pattern rules: below ${R.cut}% on a standard after ${R.minN}+ questions on ${R.minDays}+ days, or the same error ${R.errN}+ times</summary>
    <form id="rules-form" class="row">
      <label for="r-minN">Questions at least <input type="number" id="r-minN" name="minN" min="3" max="30" value="${R.minN}"></label>
      <label for="r-minDays">Different days at least <input type="number" id="r-minDays" name="minDays" min="1" max="10" value="${R.minDays}"></label>
      <label for="r-cut">Accuracy below <input type="number" id="r-cut" name="cut" min="20" max="95" step="5" value="${R.cut}">%</label>
      <label for="r-errN">Same error at least <input type="number" id="r-errN" name="errN" min="2" max="10" value="${R.errN}"> times</label>
      <button class="btn small" type="submit">Save rules</button>
      ${t.dismissed.some(d => d[0] === ui.cls) ? `<button type="button" class="btn quiet small" data-restore>Show dismissed groups again</button>` : ""}
    </form></details>`;
  const open = gs.filter(g => !assignedStd.has(g.st));
  h += open.length ? `<div class="groups">${open.map(groupCard).join("")}</div>`
    : `<div class="empty">${all.length ? "No new patterns with the current rules." : "Patterns appear here once students have practiced on at least two days."}</div>`;
  h += `</section>`;
  if (assigned.length) h += `<section class="section"><div class="section-head"><h2>Interventions in progress</h2><span class="muted">Each set is tracked until the student finishes it.</span></div><div class="groups">${assigned.map(assignedCard).join("")}</div></section>`;
  h += heatmap(per, studs, gs);
  if (ui.student && studs.some(s => s.id === ui.student)) h += studentPanel(ui.student, per[ui.student]);
  return h;
}
function label(uid) { return ui.t.users.find(u => u.id === +uid)?.label || "Student"; }
function groupCard(g) {
  const s = ui.STD[g.st];
  const who = Object.entries(g.who).sort((a, b) => pct(a[1].c, a[1].n) - pct(b[1].c, b[1].n));
  const errs = g.topErr.map(([e, n]) => `<li>${errLabel(e)} <span class="muted">(${n}×)</span></li>`).join("");
  return `<article class="group"><div class="eyebrow">${CATS[s.cat]}</div>
    <h3>${esc(s.name)} <span class="mono muted">${g.st}</span></h3>
    <div class="who">${who.map(([uid, f]) => `<button type="button" data-student="${uid}">${esc(label(uid))}<span>${f.n ? pct(f.c, f.n) + "%" : "error"}</span></button>`).join("")}</div>
    <div class="why">${who.length} student${who.length === 1 ? "" : "s"}. ${errs ? "Most common errors:" : "Accuracy has stayed below the rule across enough questions and days."}</div>
    ${errs ? `<ul class="why" style="margin:0;padding-left:18px">${errs}</ul>` : ""}
    <div class="note"><b>Suggested:</b> a 10-question set on ${esc(lc(s.name))}. ${reteachNote(g)}</div>
    <div class="row"><button type="button" class="btn" data-approve="${g.st}">Approve and assign</button><button type="button" class="btn quiet" data-dismiss="${g.st}">Dismiss</button></div></article>`;
}
function assignedCard(a) {
  const done = a.userIds.filter(uid => (a.progress[uid]?.[1] || 0) >= a.itemIds.length).length;
  return `<article class="group assigned"><div class="eyebrow">Assigned ${fmtDay(a.day)}</div>
    <h3>${esc(stdName(a.standard))} <span class="mono muted">${a.standard}</span></h3>
    <div class="why">${done} of ${a.userIds.length} finished the ${a.itemIds.length}-question set</div>
    <div class="who">${a.userIds.map(uid => { const p = a.progress[uid]; const fin = p && p[1] >= a.itemIds.length;
      return `<button type="button" data-student="${uid}">${esc(label(uid))}${fin ? `<span style="color:${p[0] / p[1] >= .7 ? "var(--ok)" : "var(--crit)"}">${p[0]}/${p[1]}</span>` : `<span style="color:var(--muted)">${p ? p[1] + "/" + a.itemIds.length : "not started"}</span>`}</button>`; }).join("")}</div>
    ${a.note ? `<div class="note">${a.note}</div>` : ""}
    <div class="row"><button type="button" class="btn quiet" data-close-assignment="${a.id}">Close intervention</button></div></article>`;
}
function heatmap(per, studs, gs) {
  const flagSet = new Set(gs.flatMap(g => Object.keys(g.who).map(uid => uid + "|" + g.st)));
  const cats = Object.keys(CATS);
  const cols = cats.flatMap(c => ui.bank.standardList.filter(s => s.cat === c));
  const list = studs.slice().sort((a, b) => a.label.localeCompare(b.label, undefined, { numeric: true }));
  let h = `<section class="section"><div class="section-head"><h2>Accuracy by standard</h2>
    <div class="legend"><span><i class="h1"></i>below 50%</span><span><i class="h2"></i>50–69%</span><span><i class="h3"></i>70–84%</span><span><i class="h4"></i>85%+</span><span><i class="h0"></i>fewer than 3 answered</span><span><i style="box-shadow:inset 0 0 0 2px var(--crit)"></i>flagged</span></div></div>
    <div class="scroll"><table class="heat"><thead><tr><th class="name" rowspan="2" style="vertical-align:bottom;padding-bottom:8px">Student</th>`;
  for (const c of cats) h += `<th class="cat" colspan="${cols.filter(s => s.cat === c).length}">${CATS[c]}</th>`;
  h += `</tr><tr>${cols.map(s => `<th class="std" title="${s.code}"><div>${esc(s.name)}</div></th>`).join("")}</tr></thead><tbody>`;
  for (const s of list) {
    const p = per[s.id] || { std: {} };
    h += `<tr><td class="name"><button type="button" data-student="${s.id}">${esc(s.label)}${s.active ? "" : " (off)"}</button></td>`;
    for (const c of cols) {
      const x = p.std[c.code];
      h += `<td class="cell ${x ? heatClass(x.c, x.n) : "h0"}${flagSet.has(s.id + "|" + c.code) ? " flag" : ""}" title="${esc(s.label)} · ${esc(c.name)}: ${x ? `${x.c} of ${x.n} correct` : "not practiced yet"}">${x && x.n >= 3 ? pct(x.c, x.n) : x ? "·" : ""}</td>`;
    }
    h += `</tr>`;
  }
  return h + `</tbody></table></div><p class="muted" style="margin:0;font-size:13px">Select a student to see their errors and recent practice.</p></section>`;
}
function studentPanel(uid, p) {
  const s = ui.t.users.find(u => u.id === uid);
  const head = `<div class="section-head"><div><div class="eyebrow">Student detail</div><h2>${esc(s.label)}</h2></div><button type="button" class="btn quiet" data-student="">Close</button></div>`;
  if (!p) return `<section class="section"><div class="panel" id="student-panel">${head}<p class="muted">No practice yet.</p></div></section>`;
  const stds = Object.entries(p.std).sort((a, b) => pct(a[1].c, a[1].n) - pct(b[1].c, b[1].n));
  const errs = Object.entries(p.err).sort((a, b) => b[1].n - a[1].n).slice(0, 5);
  const mine = rows().filter(a => a.uid === uid);
  const days = [...p.days].sort().slice(-6).reverse();
  return `<section class="section"><div class="panel" id="student-panel">${head}
    <div class="muted" style="font-size:13.5px">${p.n} questions · ${pct(p.c, p.n)}% correct · practiced on ${p.days.size} day${p.days.size === 1 ? "" : "s"}</div>
    <div><h3 style="margin-bottom:8px">By standard, weakest first</h3><div class="bars">${stds.slice(0, 10).map(([c, x]) => bar(stdName(c), x.c, x.n)).join("")}</div></div>
    ${errs.length ? `<div><h3 style="margin-bottom:8px">Repeated errors</h3><ul style="margin:0;padding-left:18px">${errs.map(([e, x]) => `<li>${errLabel(e)} <span class="muted">(${x.n}×)</span></li>`).join("")}</ul></div>` : ""}
    <div><h3 style="margin-bottom:8px">Recent practice</h3><table class="plain"><thead><tr><th>Day</th><th>Questions</th><th>Correct</th></tr></thead><tbody>${days.map(d => { const x = mine.filter(a => a.day === d); return `<tr><td>${fmtDay(d)}</td><td>${x.length}</td><td>${x.filter(a => a.ok).length}</td></tr>`; }).join("")}</tbody></table></div>
  </div></section>`;
}

// ---------- classes & codes
function viewClasses() {
  const t = ui.t;
  const me = t.users.find(u => u.me);
  const admins = t.users.filter(u => u.role === "admin");
  let h = `<div class="eyebrow">Teacher</div><h1>Classes & codes</h1>
    <p class="muted" style="max-width:70ch">Each student signs in with a code. Labels identify students in your reports; use a seat number or initials rather than a full name, and keep the matching roster yourself.</p>`;
  if (ui.made) {
    h += `<section class="section panel"><div class="section-head"><h2>New codes for ${esc(ui.made.className)}</h2><div class="row no-print"><button type="button" class="btn ghost small" data-print>Print these codes</button><button type="button" class="btn quiet small" data-hide-made>Done</button></div></div>
      <div class="cardsheet">${ui.made.codes.map(c => codeCard(c.label, c.code, ui.made.className)).join("")}</div></section>`;
  }
  h += `<section class="section"><div class="section-head"><h2>Add a class</h2></div>
    <form id="add-class" class="row"><label for="new-class">Class name</label><input type="text" id="new-class" class="field" placeholder="Period 2" maxlength="60" required><button class="btn" type="submit">Add class</button></form></section>`;
  for (const c of t.classes) {
    const studs = t.users.filter(u => u.role === "student" && u.classId === c.id);
    h += `<section class="section"><div class="section-head"><h2>${esc(c.name)} <span class="muted" style="font-size:14px;font-weight:500">${studs.length} code${studs.length === 1 ? "" : "s"}</span></h2>
      <div class="row no-print"><button type="button" class="btn quiet small" data-cards="${c.id}">Print all codes</button><button type="button" class="btn quiet small" data-rename-class="${c.id}">Rename</button></div></div>
      <form class="row make-codes" data-class="${c.id}"><label>Make <input type="number" name="count" min="1" max="60" value="${studs.length ? 1 : 25}"> codes labeled</label>
        <input type="text" class="field" name="prefix" value="${esc(defaultPrefix(c, studs))}" maxlength="20" aria-label="Label start" style="width:110px"><span class="hint">01, 02, …</span><button class="btn small" type="submit">Make codes</button></form>
      ${studs.length ? `<div class="scroll"><table class="plain"><thead><tr><th>Label</th><th>Code</th><th>Status</th><th></th></tr></thead><tbody>${studs.map(userRow).join("")}</tbody></table></div>` : ""}
      ${ui.cardsFor === c.id ? `<div class="cardsheet" style="margin-top:12px">${studs.filter(s => s.active).map(s => codeCard(s.label, s.code, c.name)).join("")}</div><div class="row no-print"><button type="button" class="btn ghost small" data-print>Print</button><button type="button" class="btn quiet small" data-cards="">Hide</button></div>` : ""}
    </section>`;
  }
  h += `<section class="section"><div class="section-head"><h2>Administrator codes</h2></div>
    <p class="muted" style="margin:0">Administrators see class results and the question bank, never student labels or answers.</p>
    <form id="add-admin" class="row"><label for="admin-label">Name or role</label><input type="text" id="admin-label" class="field" placeholder="Assistant principal" maxlength="60"><button class="btn small" type="submit">Make admin code</button></form>
    ${admins.length ? `<div class="scroll"><table class="plain"><thead><tr><th>Label</th><th>Code</th><th>Status</th><th></th></tr></thead><tbody>${admins.map(userRow).join("")}</tbody></table></div>` : ""}</section>
  <section class="section"><div class="section-head"><h2>Your teacher code</h2></div>
    <div class="row"><span class="code" style="font-size:18px">${esc(me?.code || "")}</span><button type="button" class="btn quiet small" data-new-code="${me?.id}">Replace my code</button></div>
    <p class="hint" style="margin:0">Replace it if anyone else may have seen it. You stay signed in on this device.</p></section>
  <section class="section"><div class="section-head"><h2>Delete student data</h2></div>
    <p class="muted" style="margin:0">Removes every student code, answer and intervention. Classes, admin codes and your code stay. Use this at the end of the pilot or if the school asks.</p>
    <form id="purge" class="row"><label for="purge-confirm">Type DELETE to confirm</label><input type="text" id="purge-confirm" class="field" autocomplete="off" style="width:120px"><button class="btn danger small" type="submit">Delete all student data</button></form></section>`;
  return h;
}
function defaultPrefix(c, studs) {
  if (studs.length) { const m = studs[0].label.match(/^(.*?)(\d+)$/); if (m) return m[1]; }
  const n = c.name.match(/\d+/); return n ? `P${n[0]}-` : "Student ";
}
function userRow(u) {
  return `<tr><td><input type="text" value="${esc(u.label)}" data-label="${u.id}" aria-label="Label" maxlength="60"></td>
    <td><span class="code">${esc(u.code)}</span></td>
    <td>${u.active ? `<span class="pill good">Active</span>` : `<span class="pill">Turned off</span>`}</td>
    <td><div class="actions-cell"><button type="button" class="btn quiet small" data-new-code="${u.id}">New code</button>
      <button type="button" class="btn quiet small" data-active="${u.id}" data-to="${u.active ? 0 : 1}">${u.active ? "Turn off" : "Turn on"}</button>
      <button type="button" class="btn danger small" data-delete-user="${u.id}">${ui.confirmDelete === u.id ? "Confirm delete" : "Delete"}</button></div></td></tr>`;
}
function codeCard(lbl, code, cls) {
  return `<div class="codecard"><div class="eyebrow">Algebra II Practice · ${esc(cls)}</div><div><b>${esc(lbl)}</b></div><div class="code">${esc(code)}</div><div class="hint">Sign in at ${esc(location.host)}</div></div>`;
}

// ---------- student
function viewStudent() {
  const s = ui.s;
  const mine = s.assignments;
  const stds = ui.bank.standardList.filter(x => ui.practice.cat === "ALL" || x.cat === ui.practice.cat);
  let h = `<div class="eyebrow">Student</div><h1>Hi, ${esc(ui.me.label)}</h1>
    <section class="section"><h2>Assigned to you</h2>`;
  h += mine.length ? `<div class="cards">${mine.map(a => { const fin = a.answered >= a.itemIds.length; return `<article class="card"><div class="eyebrow">From your teacher · ${fmtDay(a.day)}</div><h3>${esc(stdName(a.standard))}</h3>
      <div class="muted" style="font-size:13.5px">${a.itemIds.length} questions${a.answered && !fin ? ` · ${a.answered} done` : ""}</div>
      ${fin ? `<span class="pill good">Done · ${a.right} of ${a.itemIds.length}</span>` : `<button type="button" class="btn" data-start-assign="${a.id}">${a.answered ? "Continue" : "Start"}</button>`}</article>`; }).join("")}</div>`
    : `<div class="empty">Nothing assigned right now. Try a practice set below.</div>`;
  h += `</section><section class="section"><h2>Practice a set of 10</h2>
    <div class="tabs" role="group" aria-label="Category"><button type="button" data-pcat="ALL" aria-pressed="${ui.practice.cat === "ALL"}">All categories</button>${Object.entries(CATS).map(([k, v]) => `<button type="button" data-pcat="${k}" aria-pressed="${ui.practice.cat === k}">${v}</button>`).join("")}</div>
    <div class="row"><label for="pstd">Standard</label><select id="pstd"><option value="ALL">Any standard</option>${stds.map(x => `<option value="${x.code}"${x.code === ui.practice.std ? " selected" : ""}>${esc(x.name)} (${x.code})</option>`).join("")}</select>
    <button type="button" class="btn" data-start-practice>Start practice</button></div></section>
    <section class="section"><h2>My progress</h2>`;
  const per = {};
  for (const [qid, , ok] of s.answers) { const q = ui.ITEM[qid]; if (!q) continue; const st = base(q.standard); const x = per[st] ||= [0, 0]; x[1]++; if (ok) x[0]++; }
  const list = Object.entries(per).sort((a, b) => pct(a[1][0], a[1][1]) - pct(b[1][0], b[1][1]));
  const tot = s.answers.length, right = s.answers.filter(a => a[2]).length;
  h += list.length ? `<div class="panel"><div class="muted" style="font-size:13.5px">${tot} questions answered · ${pct(right, tot)}% correct · weakest standards first</div><div class="bars">${list.map(([c, [r, n]]) => bar(stdName(c), r, n)).join("")}</div></div>`
    : `<div class="empty">Your progress appears here after your first set.</div>`;
  return h + `</section>`;
}

// ---------- practice runner (students)
function startRun(ids, title, assignmentId) {
  ui.run = { ids, i: 0, sel: [], fb: null, right: 0, title, assignmentId, results: [], busy: false };
  ui.err = ""; render(); window.scrollTo({ top: 0 });
}
function viewRun() {
  const r = ui.run;
  if (r.i >= r.ids.length) {
    const by = {};
    for (const x of r.results) { const st = base(ui.ITEM[x.qid].standard); const v = by[st] ||= [0, 0]; v[1]++; if (x.ok) v[0]++; }
    return `<div class="eyebrow">${esc(r.title)}</div><h1>${r.right} of ${r.results.length} correct</h1>
      <div class="panel" style="margin-top:16px;max-width:860px"><div class="bars">${Object.entries(by).map(([st, [c, n]]) => bar(stdName(st), c, n)).join("")}</div>
      <div class="row"><button type="button" class="btn" data-end-run>Done</button></div></div>`;
  }
  const q = ui.ITEM[r.ids[r.i]], fb = r.fb;
  return `<div class="row" style="justify-content:space-between;max-width:860px"><div><div class="eyebrow">${esc(r.title)}</div><h1 style="font-size:20px">Question ${r.i + 1} of ${r.ids.length}</h1></div><button type="button" class="btn quiet" data-end-run>Exit</button></div>
    <div class="progress" style="margin:12px 0 16px"><span style="width:${100 * r.i / r.ids.length}%"></span></div>
    <article class="q"><div class="meta"><span class="pill">${CATS[q.category]}</span><span class="pill mono">${q.standard}</span><span class="pill">${q.calculator === "N" ? "No calculator" : "Calculator allowed"}</span>${q.type === "MS" ? '<span class="pill">Select all that apply</span>' : ""}</div>
    <div class="stem">${q.stem}</div>
    <div class="choices">${q.choices.map((c, i) => { const isA = fb && fb.answer.includes(i), isS = r.sel.includes(i); const cl = fb ? (isA ? " right" : isS ? " wrong" : "") : "";
      return `<button type="button" class="choice${cl}" data-pick="${i}" aria-pressed="${isS}"${fb ? " disabled" : ""}><b>${LETTERS[i]}.</b><span>${c}${fb && (isA || isS) ? `<span class="r">${fb.rationales[i]}</span>` : ""}</span></button>`; }).join("")}</div>
    ${fb ? `<div class="feedback"><b>${fb.correct ? "Correct." : "Not quite."}</b> ${fb.explanation}</div>` : ""}
    <div class="row">${fb ? `<button type="button" class="btn" data-next>${r.i + 1 < r.ids.length ? "Next question" : "See results"}</button>` : `<button type="button" class="btn" data-check${r.sel.length && !r.busy ? "" : " disabled"}>${r.busy ? "Checking…" : "Check answer"}</button>`}<span class="mono muted">${q.id}</span></div></article>`;
}

// ---------- admin and bank
function viewAdmin() {
  const a = ui.admin;
  let h = `<div class="eyebrow">Administrator</div><h1>Results by class</h1>
    <p class="muted" style="max-width:68ch">Class-level results only. Student labels and individual answers are visible to the class teacher.</p>`;
  if (!a.classes.length) return h + `<div class="empty">No classes yet.</div>`;
  h += `<section class="section"><div class="scroll"><table class="plain"><thead><tr><th>Class</th><th>Students</th><th>Active, last 7 days</th><th>Answers</th><th>Accuracy</th>${Object.values(CATS).map(c => `<th>${c}</th>`).join("")}<th>Interventions</th></tr></thead><tbody>
    ${a.classes.map(c => `<tr><td>${esc(c.name)}</td><td>${c.students}</td><td>${c.activeThisWeek}</td><td>${c.answers.toLocaleString()}</td><td>${c.answers ? pct(c.correct, c.answers) + "%" : "–"}</td>
      ${Object.keys(CATS).map(k => { const [r, n] = c.byCategory[k]; const p = pct(r, n); return `<td>${n ? `<span class="pill" style="background:var(--${p < 50 ? "crit" : p < 70 ? "warn" : "ok"}-bg);color:var(--ink)">${p}%</span>` : "–"}</td>`; }).join("")}
      <td>${c.interventions}</td></tr>`).join("")}</tbody></table></div></section>`;
  return h;
}
function viewBank() {
  const b = ui.bankf, items = ui.bank.items;
  const q = b.q.trim().toLowerCase();
  const list = items.filter(x => (b.cat === "ALL" || x.category === b.cat) && (b.std === "ALL" || base(x.standard) === b.std) && (b.type === "ALL" || x.type === b.type) &&
    (!q || x.id.toLowerCase().includes(q) || x.standard.toLowerCase().includes(q) || x.stem.replace(/<svg[\s\S]*?<\/svg>/g, "").replace(/<[^>]+>/g, " ").toLowerCase().includes(q)));
  const per = 20, pages = Math.max(1, Math.ceil(list.length / per));
  b.page = Math.min(b.page, pages - 1);
  const shown = list.slice(b.page * per, b.page * per + per);
  const stds = ui.bank.standardList.filter(s => b.cat === "ALL" || s.cat === b.cat);
  let h = `<div class="section-head"><div><div class="eyebrow">Question bank</div><h1>${items.length.toLocaleString()} questions</h1></div><span class="muted">${list.length.toLocaleString()} match</span></div>
    <div class="row" style="margin-top:16px">
      <select id="b-cat" aria-label="Category"><option value="ALL">All categories</option>${Object.entries(CATS).map(([k, v]) => `<option value="${k}"${b.cat === k ? " selected" : ""}>${v}</option>`).join("")}</select>
      <select id="b-std" aria-label="Standard"><option value="ALL">All standards</option>${stds.map(s => `<option value="${s.code}"${b.std === s.code ? " selected" : ""}>${s.code} · ${esc(s.name)}</option>`).join("")}</select>
      <select id="b-type" aria-label="Question type"><option value="ALL">All types</option><option value="MC"${b.type === "MC" ? " selected" : ""}>Multiple choice</option><option value="MS"${b.type === "MS" ? " selected" : ""}>Select all</option></select>
      <input type="search" id="b-q" placeholder="Search words or an ID like A2-0457" value="${esc(b.q)}" aria-label="Search questions" style="flex:1;min-width:200px">
    </div><div class="bank-list" style="margin-top:14px">`;
  h += shown.length ? shown.map(x => `<details class="item"><summary><span class="mono">${x.id}<br><span class="muted">${x.standard}</span></span><span class="preview">${x.stem.replace(/<svg[\s\S]*?<\/svg>/g, " [graph] ").replace(/<table[\s\S]*?<\/table>/g, " [table] ")}</span></summary>
      <div class="body"><div class="row" style="gap:6px"><span class="pill">${CATS[x.category]}</span><span class="pill">${x.type === "MS" ? "Select all" : "Multiple choice"}</span><span class="pill">DOK ${x.dok}</span><span class="pill">${x.calculator === "N" ? "No calculator" : "Calculator"}</span></div>
      <div class="stem">${x.stem}</div>${x.choices.map((c, i) => `<div class="opt${x.answer.includes(i) ? " key" : ""}"><b>${LETTERS[i]}.</b> ${c}<span class="r">${x.rationales[i]}</span></div>`).join("")}
      <div class="feedback"><b>Explanation.</b> ${x.explanation}</div></div></details>`).join("") : `<div class="empty">No questions match these filters.</div>`;
  h += `</div><div class="pager" style="margin-top:14px"><button type="button" class="btn quiet" data-page="-1"${b.page === 0 ? " disabled" : ""}>Previous</button><span class="muted">Page ${b.page + 1} of ${pages}</span><button type="button" class="btn quiet" data-page="1"${b.page >= pages - 1 ? " disabled" : ""}>Next</button></div>`;
  return h;
}

// ---------- events
document.addEventListener("submit", async e => {
  const f = e.target; e.preventDefault();
  if (f.id === "signin-form") {
    const code = document.getElementById("code").value;
    const btn = f.querySelector("button"); btn.disabled = true; btn.textContent = "Signing in…";
    const r = await act("/api/auth", { action: "login", code });
    if (r) { ui.me = await api("/api/auth"); ui.view = null; try { await enter(); } catch (x) { ui.err = x.message; } }
    render(); return;
  }
  if (f.id === "setup-form") {
    const r = await act("/api/auth", { action: "setup", key: document.getElementById("setup-key").value });
    if (r) ui.setupCode = r.code;
    render(); return;
  }
  if (f.id === "rules-form") {
    const fd = new FormData(f), rules = Object.fromEntries([...fd.entries()].map(([k, v]) => [k, +v]));
    if (await act("/api/teacher", { action: "rules", rules }, "Rules saved.")) await loadTeacher();
    render(); return;
  }
  if (f.id === "add-class") {
    const name = document.getElementById("new-class").value;
    const r = await act("/api/teacher", { action: "addClass", name }, `Added ${name}.`);
    if (r) await loadTeacher(ui.cls ?? r.id);
    render(); return;
  }
  if (f.classList.contains("make-codes")) {
    const classId = +f.dataset.class, fd = new FormData(f);
    const r = await act("/api/teacher", { action: "makeCodes", classId, count: +fd.get("count"), prefix: fd.get("prefix") });
    if (r) { ui.made = { className: ui.t.classes.find(c => c.id === classId).name, codes: r.made }; await loadTeacher(); window.scrollTo({ top: 0 }); }
    render(); return;
  }
  if (f.id === "add-admin") {
    const r = await act("/api/teacher", { action: "addAdmin", label: document.getElementById("admin-label").value });
    if (r) { ui.msg = `Admin code for ${r.label}: ${r.code}`; await loadTeacher(); }
    render(); return;
  }
  if (f.id === "purge") {
    const r = await act("/api/teacher", { action: "deleteAllStudentData", confirm: document.getElementById("purge-confirm").value }, "All student data was deleted.");
    if (r) { ui.made = null; await loadTeacher(); }
    render(); return;
  }
});

document.addEventListener("click", async e => {
  const t = e.target.closest("button");
  if (!t || t.type === "submit") return;
  const d = t.dataset;
  if (t.hasAttribute("data-signout")) { await act("/api/auth", { action: "logout" }); Object.assign(ui, { me: { signedIn: false }, bank: null, t: null, s: null, run: null, admin: null, made: null, msg: "", err: "", view: null, cls: null, student: null, cardsFor: null, practice: { cat: "ALL", std: "ALL" }, bankf: { cat: "ALL", std: "ALL", type: "ALL", q: "", page: 0 } }); ui.me = await api("/api/auth"); render(); return; }
  if (d.setup !== undefined) { ui.setup = d.setup === "1"; ui.err = ""; render(); return; }
  if (t.hasAttribute("data-continue")) { ui.setup = false; ui.setupCode = null; ui.me = await api("/api/auth"); await enter(); ui.view = "classes"; render(); return; }
  if (d.view) { ui.view = d.view; ui.msg = ""; ui.err = ""; if (d.view === "summary") ui.admin = await api("/api/admin"); render(); return; }
  if (d.cls) { ui.student = null; await loadTeacher(+d.cls); render(); return; }
  if (d.student !== undefined) { ui.student = d.student ? +d.student : null; render(); if (ui.student) document.getElementById("student-panel")?.scrollIntoView({ behavior: "smooth", block: "start" }); return; }
  if (d.approve) {
    const g = groups(analyze()).find(x => x.st === d.approve);
    if (g && await act("/api/teacher", { action: "assign", classId: ui.cls, standard: g.st, userIds: Object.keys(g.who).map(Number), itemIds: suggestSet(g), note: reteachNote(g) }, `Assigned ${stdName(g.st)} to ${Object.keys(g.who).length} student(s).`)) await loadTeacher();
    render(); return;
  }
  if (d.dismiss) { if (await act("/api/teacher", { action: "dismiss", classId: ui.cls, standard: d.dismiss })) await loadTeacher(); render(); return; }
  if (t.hasAttribute("data-restore")) { if (await act("/api/teacher", { action: "restoreDismissed", classId: ui.cls })) await loadTeacher(); render(); return; }
  if (d.closeAssignment) { if (await act("/api/teacher", { action: "closeAssignment", id: +d.closeAssignment })) await loadTeacher(); render(); return; }
  if (d.newCode) {
    const r = await act("/api/teacher", { action: "newCode", userId: +d.newCode });
    if (r) { ui.msg = `New code: ${r.code}. The old code no longer works.`; await loadTeacher(); }
    render(); return;
  }
  if (d.active) { if (await act("/api/teacher", { action: "setActive", userId: +d.active, active: d.to === "1" })) await loadTeacher(); render(); return; }
  if (d.deleteUser) {
    const id = +d.deleteUser;
    if (ui.confirmDelete !== id) { ui.confirmDelete = id; render(); return; }
    ui.confirmDelete = null;
    if (await act("/api/teacher", { action: "deleteUser", userId: id }, "Deleted the code and its answers.")) await loadTeacher();
    render(); return;
  }
  if (d.renameClass) {
    const c = ui.t.classes.find(x => x.id === +d.renameClass);
    const name = window.prompt("New class name", c.name);
    if (name && await act("/api/teacher", { action: "renameClass", classId: c.id, name })) await loadTeacher();
    render(); return;
  }
  if (d.cards !== undefined) { ui.cardsFor = d.cards ? +d.cards : null; render(); return; }
  if (t.hasAttribute("data-print")) { window.print(); return; }
  if (t.hasAttribute("data-hide-made")) { ui.made = null; render(); return; }
  if (d.pcat) { ui.practice.cat = d.pcat; ui.practice.std = "ALL"; render(); return; }
  if (t.hasAttribute("data-start-practice")) {
    const pool = ui.bank.items.filter(q => (ui.practice.cat === "ALL" || q.category === ui.practice.cat) && (ui.practice.std === "ALL" || base(q.standard) === ui.practice.std));
    const title = ui.practice.std !== "ALL" ? stdName(ui.practice.std) : ui.practice.cat !== "ALL" ? CATS[ui.practice.cat] : "Mixed practice";
    startRun(shuffle(pool).slice(0, 10).map(q => q.id), title, null); return;
  }
  if (d.startAssign) {
    const a = ui.s.assignments.find(x => x.id === +d.startAssign);
    const done = new Set(a.answeredIds || []);
    startRun(a.itemIds.filter(id => !done.has(id)), "Assigned: " + stdName(a.standard), a.id); return;
  }
  if (d.pick !== undefined && ui.run && !ui.run.fb) {
    const q = ui.ITEM[ui.run.ids[ui.run.i]], i = +d.pick;
    ui.run.sel = q.type === "MC" ? [i] : ui.run.sel.includes(i) ? ui.run.sel.filter(x => x !== i) : [...ui.run.sel, i];
    render(); return;
  }
  if (t.hasAttribute("data-check") && ui.run && !ui.run.busy) {
    const r = ui.run, qid = r.ids[r.i];
    r.busy = true; render();
    const fb = await act("/api/student", { action: "answer", itemId: qid, pick: r.sel, assignmentId: r.assignmentId });
    r.busy = false;
    if (fb) { r.fb = fb; if (fb.correct) r.right++; r.results.push({ qid, ok: fb.correct }); }
    render(); return;
  }
  if (t.hasAttribute("data-next") && ui.run) { const r = ui.run; r.i++; r.sel = []; r.fb = null; render(); window.scrollTo({ top: 0 }); return; }
  if (t.hasAttribute("data-end-run")) { ui.run = null; await loadStudent(); render(); return; }
  if (d.page) { ui.bankf.page += +d.page; render(); window.scrollTo({ top: 0 }); return; }
});

document.addEventListener("change", async e => {
  const t = e.target;
  if (t.id === "pstd") ui.practice.std = t.value;
  else if (t.id === "b-cat") { ui.bankf.cat = t.value; ui.bankf.std = "ALL"; ui.bankf.page = 0; render(); }
  else if (t.id === "b-std") { ui.bankf.std = t.value; ui.bankf.page = 0; render(); }
  else if (t.id === "b-type") { ui.bankf.type = t.value; ui.bankf.page = 0; render(); }
  else if (t.dataset.label) {
    if (await act("/api/teacher", { action: "setLabel", userId: +t.dataset.label, label: t.value }, "Label saved.")) await loadTeacher();
    render();
  }
});
let searchTimer;
document.addEventListener("input", e => {
  if (e.target.id !== "b-q") return;
  clearTimeout(searchTimer);
  searchTimer = setTimeout(() => {
    ui.bankf.q = e.target.value; ui.bankf.page = 0; render();
    const el = document.getElementById("b-q"); if (el) { el.focus(); el.setSelectionRange(el.value.length, el.value.length); }
  }, 250);
});

boot();
