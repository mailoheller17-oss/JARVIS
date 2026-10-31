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
  $("#panel-konnektoren").hidden = t !== "konnektoren";
  $("#panel-settings").hidden = t !== "settings";
  if (t === "konnektoren") loadKonnektoren();
  if (t === "money") renderMoney();
  if (t === "status") loadStatus();
  if (MODE_INFO[t]) { mode = t; $("#msg").placeholder = MODE_INFO[t].ph; renderChat(); renderChips(); }
}

// ---------- Quick-Chips ----------
const CHIPS = {
  chat: ["Wie wird das Wetter morgen?", "Was trendet gerade?", "/bild Gaming-Setup mit Neonlicht"],
  edit: ["Skate-Montage im Herbst", "Fortnite-Highlights mit Bass-Drops", "/bild YouTube-Thumbnail, schockiertes Gesicht, Explosion"],
  learn: ["Erklär mir Zinseszins", "Was ist ein ETF?", "Erklär mir, wie Algorithmen auf TikTok funktionieren"],
};
function renderChips() {
  const box = $("#chips"); box.innerHTML = "";
  (CHIPS[mode] || []).forEach((c) => {
    const b = document.createElement("button"); b.type = "button"; b.textContent = c;
    b.onclick = () => { $("#msg").value = c; $("#chatForm").requestSubmit(); };
    box.appendChild(b);
  });
}

// ---------- Design ----------
function setSkin(s) { document.documentElement.dataset.skin = s; store.set("jarvisSkin", s); $("#skinSelect").value = s; }
$("#skinSelect").onchange = (e) => setSkin(e.target.value);
setSkin(store.get("jarvisSkin", "ironman"));
// ?skin=neon&tile=edit – für Screenshots/Direktlinks
const qs = new URLSearchParams(location.search);
if (qs.get("skin")) setSkin(qs.get("skin"));

// ---------- Konnektoren ----------
const KOSTEN = { "gratis": ["ok", "gratis"], "gratis-kontingent": ["ok", "Gratis-Kontingent"], "kostenpflichtig": ["paid", "kostenpflichtig"] };
const STATUS = { verbunden: ["ok", "verbunden"], schluessel_fehlt: ["miss", "Schlüssel fehlt"], aus: ["off", "aus"] };
const esc = (t) => String(t).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
async function loadKonnektoren() {
  const box = $("#konList"); box.textContent = "Lade…";
  try {
    const d = await api("/api/konnektoren");
    $("#brainInfo").textContent = d.gehirn.length ? "Gehirn-Reihenfolge: " + d.gehirn.join(" → ") : "Noch kein KI-Gehirn verbunden – trag z. B. GEMINI_API_KEY ein.";
    box.innerHTML = d.kategorien.map((k) => {
      const list = d.konnektoren.filter((c) => c.kategorie === k);
      if (!list.length) return "";
      return `<h2 style="margin-top:14px">${esc(k)}</h2><div class="cards">` + list.map((c) => {
        const [sc, st] = c.status === "schluessel_fehlt" && !c.env.length ? ["miss", "nicht bereit"] : STATUS[c.status];
        const [kc, kt] = KOSTEN[c.kosten];
        return `<div class="card" data-name="${esc(c.name)}">
          <h3><span>${esc(c.titel)}</span><span class="badge ${sc}">${st}</span></h3>
          <p>${esc(c.beschreibung)}</p>
          <p><span class="badge ${kc}">${kt}</span> ${c.env.map((e) => `<code>${esc(e)}</code>`).join(" ")}</p>
          ${c.kosten === "kostenpflichtig" ? `<p class="warn">⚠️ ${esc(c.hinweis || "Kostet Geld.")} Standardmäßig aus.</p>` : ""}
          <div class="actions">
            <button class="ghost" data-act="test">Testen</button>
            <button class="ghost" data-act="toggle">${c.aktiv ? "Ausschalten" : "Einschalten"}</button>
            <a href="${esc(c.key_url)}" target="_blank" rel="noopener">Schlüssel holen ↗</a>
          </div>
          <p class="hint res"></p>
        </div>`;
      }).join("") + "</div>";
    }).join("");
    box.querySelectorAll(".card button").forEach((b) => b.onclick = () => konAction(b, d.konnektoren.find((c) => c.name === b.closest(".card").dataset.name)));
  } catch (e) { box.textContent = "Fehler: " + e.message; }
}
const pendingPaid = new Set();
async function konAction(btn, c) {
  const res = btn.closest(".card").querySelector(".res");
  if (btn.dataset.act === "test") {
    res.textContent = "Teste…";
    const r = await api(`/api/konnektoren/${c.name}/test`, {});
    res.textContent = (r.ok ? "✅ " : "❌ ") + r.meldung;
    return;
  }
  if (!c.aktiv && c.kosten === "kostenpflichtig" && !pendingPaid.has(c.name)) {
    pendingPaid.add(c.name);
    res.textContent = "⚠️ Kostet echtes Geld/Credits. Nochmal „Einschalten“ drücken zum Bestätigen.";
    return;
  }
  pendingPaid.delete(c.name);
  await api(`/api/konnektoren/${c.name}/aktiv`, { aktiv: !c.aktiv });
  loadKonnektoren();
}

// ---------- Chat ----------
function addBubble(role, text, image) {
  const d = document.createElement("div");
  d.className = "m " + role; d.textContent = text;
  if (image) { const i = document.createElement("img"); i.src = image; i.alt = text; i.onload = () => { $("#chat").scrollTop = $("#chat").scrollHeight; }; d.appendChild(i); }
  $("#chat").appendChild(d); $("#chat").scrollTop = $("#chat").scrollHeight;
}
function renderChat() {
  $("#chat").innerHTML = "";
  const h = histories[mode];
  if (!h.length) addBubble("assistant", MODE_INFO[mode].hello);
  h.forEach((m) => addBubble(m.role, m.content, m.image));
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
    const r = await api("/api/chat", { messages: h.slice(-20).map(({ role, content }) => ({ role, content })), mode });
    h.push({ role: "assistant", content: r.reply, ...(r.image ? { image: r.image } : {}) }); addBubble("assistant", r.reply, r.image);
    $("#provider").textContent = r.provider;
    store.set("jarvisHist", histories);
    speak(r.reply);
  } catch (err) {
    h.pop();
    if (err.message !== "401") addBubble("sys", "Fehler: " + err.message);
  } finally { if (!speechSynthesis?.speaking && (!audio || audio.paused)) orb(); }
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
  speechSynthesis?.cancel(); audio?.pause();
  rec.start(); $("#mic").classList.add("on"); orb("listening");
};

// ---------- Speech out ----------
let ttsOn = store.get("jarvisTts", true);
const ttsBtn = $("#ttsToggle");
const syncTts = () => { ttsBtn.textContent = ttsOn ? "🔊" : "🔇"; ttsBtn.classList.toggle("off", !ttsOn); };
syncTts();
ttsBtn.onclick = () => { ttsOn = !ttsOn; store.set("jarvisTts", ttsOn); syncTts(); if (!ttsOn) { speechSynthesis?.cancel(); audio?.pause(); } };
function germanVoice() {
  const v = speechSynthesis.getVoices().filter((v) => v.lang?.toLowerCase().startsWith("de"));
  return v.find((x) => /google|natural|neural|anna|helena|markus/i.test(x.name)) || v[0];
}
let audio = null;
async function speak(text) {
  if (!ttsOn) return orb();
  audio?.pause(); speechSynthesis?.cancel();
  try {
    const r = await fetch("/api/tts", { method: "POST", headers: { Authorization: "Bearer " + token, "Content-Type": "application/json" }, body: JSON.stringify({ text }) });
    if (r.ok) {
      audio = new Audio(URL.createObjectURL(await r.blob()));
      audio.onplay = () => orb("speaking"); audio.onended = audio.onerror = () => orb();
      await audio.play(); return;
    }
  } catch {}
  browserSpeak(text);
}
function browserSpeak(text) {
  if (!window.speechSynthesis) return orb();
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
      row("Browser: Spracherkennung", !!SR) + row("Browser: Vorlesen", !!window.speechSynthesis) +
      `<li><span>Gehirn</span><span>${s.gehirn.length ? s.gehirn.join(" → ") : "Demo"}</span></li>`;
  } catch (e) { ul.innerHTML = `<li>Fehler: ${e.message}</li>`; }
}

// ---------- Start ----------
function startApp() {
  $("#login").hidden = true; $("#app").hidden = false;
  selectTile(qs.get("tile") || "chat");
  api("/api/status").then((s) => {
    $("#provider").textContent = s.gehirn[0] || "demo";
  }).catch(() => {});
}
(async () => { if (token && await tryLogin(token)) startApp(); else showLogin(); })();
