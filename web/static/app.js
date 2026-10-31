const $ = (s) => document.querySelector(s);
const store = {
  get: (k, d) => { try { const v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch { return d; } },
  set: (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch {} },
};

// ---------- Dev auto-reload (page reloads when the server restarts) ----------
let bootId = null;
setInterval(async () => {
  try {
    const j = await (await fetch("/api/version", { cache: "no-store" })).json();
    if (bootId && j.boot !== bootId) location.reload();
    bootId = j.boot;
  } catch {}
}, 1500);

if ("serviceWorker" in navigator) navigator.serviceWorker.register("/sw.js").catch(() => {});

// ---------- Auth ----------
let token = store.get("jarvisToken", "");
const api = async (path, body) => {
  const r = await fetch(path, {
    method: body === undefined ? "GET" : "POST",
    headers: { Authorization: "Bearer " + token, "Content-Type": "application/json" },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  if (r.status === 401) { showLogin("Token ungültig."); throw new Error("401"); }
  if (!r.ok) throw new Error("HTTP " + r.status);
  return r.json();
};

function showLogin(msg) {
  $("#app").hidden = true; $("#login").hidden = false;
  if (msg) $("#loginHint").textContent = msg;
  $("#tokenInput").focus();
}
async function tryLogin(t) {
  const r = await fetch("/api/login", { method: "POST", headers: { Authorization: "Bearer " + t } });
  return r.ok;
}
$("#loginForm").onsubmit = async (e) => {
  e.preventDefault();
  const t = $("#tokenInput").value.trim();
  if (await tryLogin(t)) { token = t; store.set("jarvisToken", t); startApp(); }
  else $("#loginHint").textContent = "Nope, falscher Token.";
};
$("#logout").onclick = () => { store.set("jarvisToken", ""); token = ""; showLogin("Abgemeldet."); };

// ---------- Modes / tiles ----------
const MODE_INFO = {
  chat:  { ph: "Sag was, Mailo…", hello: "Hey Mailo, was geht?" },
  edit:  { ph: "Thema für den Edit (z.B. Skate-Montage im Herbst)", hello: "Gib mir ein Thema – ich plan Hook, Clips, Musik und Schnitte." },
  learn: { ph: "Erklär mir … (z.B. Zinseszins)", hello: "Was willst du lernen? Ich erklär's kurz und stell dir 'ne Quizfrage." },
};
let mode = "chat";
const histories = store.get("jarvisHist", { chat: [], edit: [], learn: [] });

document.querySelectorAll(".tiles button").forEach((b) => b.onclick = () => selectTile(b.dataset.tile));
function selectTile(t) {
  document.querySelectorAll(".tiles button").forEach((b) => b.classList.toggle("active", b.dataset.tile === t));
  $("#panel-money").hidden = t !== "money";
  $("#panel-status").hidden = t !== "status";
  if (t === "money") renderMoney();
  if (t === "status") loadStatus();
  if (MODE_INFO[t]) { mode = t; $("#msg").placeholder = MODE_INFO[t].ph; renderChat(); }
}

// ---------- Chat ----------
function addBubble(role, text) {
  const d = document.createElement("div");
  d.className = "m " + role; d.textContent = text;
  $("#chat").appendChild(d); $("#chat").scrollTop = $("#chat").scrollHeight;
}
function renderChat() {
  $("#chat").innerHTML = "";
  const h = histories[mode];
  if (!h.length) addBubble("assistant", MODE_INFO[mode].hello);
  h.forEach((m) => addBubble(m.role, m.content));
}
function orb(state) { $("#orb").className = "orb " + (state || ""); }

$("#chatForm").onsubmit = async (e) => {
  e.preventDefault();
  const text = $("#msg").value.trim();
  if (!text) return;
  $("#msg").value = "";
  const h = histories[mode];
  h.push({ role: "user", content: text }); addBubble("user", text);
  orb("thinking");
  try {
    const r = await api("/api/chat", { messages: h.slice(-20), mode });
    h.push({ role: "assistant", content: r.reply }); addBubble("assistant", r.reply);
    $("#provider").textContent = r.provider;
    store.set("jarvisHist", histories);
    speak(r.reply);
  } catch (err) {
    h.pop();
    if (err.message !== "401") addBubble("sys", "Fehler: " + err.message);
  } finally { if (!speechSynthesis?.speaking) orb(); }
};

// ---------- Speech in (Web Speech API) ----------
const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
let rec = null;
if (!SR) $("#mic").classList.add("off");
$("#mic").onclick = () => {
  if (!SR) return addBubble("sys", "Spracherkennung geht in diesem Browser nicht (nimm Chrome/Edge/Safari).");
  if (rec) { rec.stop(); return; }
  rec = new SR(); rec.lang = "de-DE"; rec.interimResults = true;
  rec.onresult = (e) => {
    const t = Array.from(e.results).map((r) => r[0].transcript).join("");
    $("#msg").value = t;
    if (e.results[e.results.length - 1].isFinal) $("#chatForm").requestSubmit();
  };
  rec.onerror = (e) => addBubble("sys", "Mikro: " + e.error);
  rec.onend = () => { rec = null; $("#mic").classList.remove("on"); orb(); };
  speechSynthesis?.cancel();
  rec.start(); $("#mic").classList.add("on"); orb("listening");
};

// ---------- Speech out ----------
let ttsOn = store.get("jarvisTts", true);
const ttsBtn = $("#ttsToggle");
const syncTts = () => { ttsBtn.textContent = ttsOn ? "🔊" : "🔇"; ttsBtn.classList.toggle("off", !ttsOn); };
syncTts();
ttsBtn.onclick = () => { ttsOn = !ttsOn; store.set("jarvisTts", ttsOn); syncTts(); if (!ttsOn) speechSynthesis?.cancel(); };
function germanVoice() {
  const v = speechSynthesis.getVoices().filter((v) => v.lang?.toLowerCase().startsWith("de"));
  return v.find((x) => /google|natural|neural|anna|helena|markus/i.test(x.name)) || v[0];
}
function speak(text) {
  if (!ttsOn || !window.speechSynthesis) return orb();
  speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text.replace(/[*#_`>]/g, ""));
  u.lang = "de-DE"; const v = germanVoice(); if (v) u.voice = v;
  u.onstart = () => orb("speaking"); u.onend = u.onerror = () => orb();
  speechSynthesis.speak(u);
}
if (window.speechSynthesis) speechSynthesis.onvoiceschanged = () => {};

// ---------- Money (local) ----------
const money = store.get("jarvisMoney", { name: "", goal: 0, saved: 0 });
$("#goalName").value = money.name; $("#goalAmount").value = money.goal || "";
$("#goalName").oninput = () => { money.name = $("#goalName").value; saveMoney(); };
$("#goalAmount").oninput = () => { money.goal = parseFloat($("#goalAmount").value) || 0; saveMoney(); };
const delta = (sign) => {
  const v = parseFloat($("#moneyDelta").value); if (!v) return;
  money.saved = Math.max(0, Math.round((money.saved + sign * v) * 100) / 100);
  $("#moneyDelta").value = ""; saveMoney();
};
$("#moneyAdd").onclick = () => delta(1);
$("#moneySub").onclick = () => delta(-1);
function saveMoney() { store.set("jarvisMoney", money); renderMoney(); }
function renderMoney() {
  const pct = money.goal ? Math.min(100, (money.saved / money.goal) * 100) : 0;
  $("#goalBar").style.width = pct + "%";
  const eur = (n) => n.toLocaleString("de-DE", { style: "currency", currency: "EUR" });
  $("#goalText").textContent = money.goal
    ? `${eur(money.saved)} von ${eur(money.goal)}${money.name ? " für " + money.name : ""} – ${pct.toFixed(0)} %` +
      (pct >= 100 ? " 🎉 Geschafft!" : `, noch ${eur(Math.max(0, money.goal - money.saved))}`)
    : "Setz ein Ziel, dann zähl ich mit.";
}

// ---------- Status ----------
async function loadStatus() {
  const ul = $("#statusList"); ul.innerHTML = "<li>Lade…</li>";
  try {
    const s = await api("/api/status");
    const row = (k, ok, extra = "") => `<li><span>${k}</span><span>${ok ? "✅" : "❌"} ${extra}</span></li>`;
    ul.innerHTML =
      Object.entries(s.keys).map(([k, v]) => row(k, v)).join("") +
      Object.entries(s.tools).map(([k, v]) => row("Werkzeug: " + k, v)).join("") +
      row("Browser: Spracherkennung", !!SR) + row("Browser: Vorlesen", !!window.speechSynthesis);
  } catch (e) { ul.innerHTML = `<li>Fehler: ${e.message}</li>`; }
}

// ---------- Start ----------
function startApp() {
  $("#login").hidden = true; $("#app").hidden = false;
  selectTile("chat");
  api("/api/status").then((s) => {
    const any = s.keys.GEMINI_API_KEY || s.keys.GROQ_API_KEY;
    $("#provider").textContent = any ? (s.keys.GEMINI_API_KEY ? "Gemini" : "Groq") : "demo";
  }).catch(() => {});
}
(async () => { if (token && await tryLogin(token)) startApp(); else showLogin(); })();
