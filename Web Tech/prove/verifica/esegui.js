// Esegue i casi di verifica della banca e ne restituisce l'esito reale.
//
//   node esegui.js casi.json risultati.json
//
// Tipi di caso:
//   node      un frammento JavaScript eseguito con Node (righe stampate ed
//             eventuale eccezione non gestita)
//   browser   un documento HTML aperto in Chromium (console ed errori della
//             pagina), con eventuali clic e attese dopo il caricamento
//   css       il valore calcolato di una proprietà di un elemento
//   dom       il valore di un'espressione valutata nella pagina caricata
//   pug       un template Pug trasformato in HTML con i locals dati
//   express   un'applicazione (Express o il modulo http di Node) avviata
//             davvero e interrogata con fetch
//
// Chromium arriva da Playwright (require('playwright')); Pug ed Express dai
// pacchetti installati in questa cartella (npm install).

"use strict";

const fs = require("fs");
const os = require("os");
const path = require("path");
const net = require("net");
const { spawn, spawnSync } = require("child_process");

const QUI = __dirname;

function nomeErrore(stderr) {
  for (const riga of stderr.split("\n")) {
    const m = riga.match(/^(?:Uncaught )?([A-Za-z_$][\w$]*(?:Error|Exception))\b/);
    if (m) return m[1];
  }
  return stderr.trim() ? "ErroreSconosciuto" : null;
}

function righe(testo) {
  const r = testo.replace(/\r/g, "").split("\n");
  if (r.length && r[r.length - 1] === "") r.pop();
  return r;
}

function scriviFile(caso, cartella) {
  for (const [nome, contenuto] of Object.entries(caso.file || {})) {
    fs.writeFileSync(path.join(cartella, nome), contenuto);
  }
}

function eseguiNode(caso, cartella) {
  scriviFile(caso, cartella);
  const estensione = caso.modulo ? ".mjs" : ".js";
  const file = path.join(cartella, "caso" + estensione);
  const testa = caso.strict && !caso.modulo ? '"use strict";\n' : "";
  fs.writeFileSync(file, testa + caso.codice + "\n");
  const esito = spawnSync(process.execPath, [file], {
    cwd: cartella, encoding: "utf8", timeout: 15000,
    env: Object.assign({}, process.env, { NODE_OPTIONS: "", JAVA_TOOL_OPTIONS: "" }),
  });
  return { righe: righe(esito.stdout || ""),
           errore: esito.status === 0 ? null : nomeErrore(esito.stderr || "") };
}

let browser = null;
async function apriBrowser() {
  if (!browser) {
    const { chromium } = require("playwright");
    browser = await chromium.launch();
  }
  return browser;
}

async function apriPagina(caso, cartella, html) {
  const b = await apriBrowser();
  const contesto = await b.newContext({
    viewport: { width: (caso.viewport || [1000, 700])[0], height: (caso.viewport || [1000, 700])[1] },
  });
  const pagina = await contesto.newPage();
  const console_ = [];
  const errori = [];
  pagina.on("console", (m) => console_.push(m.text()));
  // gli errori degli script esterni arrivano come "Uncaught TypeError"
  pagina.on("pageerror", (e) => errori.push((e.name || "Error").replace(/^Uncaught /, "")));
  const file = path.join(cartella, "pagina.html");
  fs.writeFileSync(file, html);
  scriviFile(caso, cartella);
  await pagina.goto("file://" + file, { waitUntil: "load" });
  return { pagina, contesto, console_, errori };
}

async function eseguiBrowser(caso, cartella) {
  const { pagina, contesto, console_, errori } = await apriPagina(caso, cartella, caso.html);
  await pagina.waitForTimeout(200);
  for (const azione of caso.azioni || []) {
    if (azione.click) await pagina.click(azione.click);
    if (azione.attendi) await pagina.waitForTimeout(azione.attendi);
  }
  await pagina.waitForTimeout(caso.attesa || 300);
  await contesto.close();
  return { righe: console_, errore: errori.length ? errori[0] : null };
}

async function eseguiCss(caso, cartella) {
  const html = "<!DOCTYPE html>\n<html><head><meta charset=\"utf-8\"><style>\n" + caso.css +
    "\n</style></head>\n" + caso.html + "\n</html>\n";
  const { pagina, contesto } = await apriPagina(caso, cartella, html);
  const risultato = await pagina.evaluate(({ selettore, proprieta, candidati }) => {
    const el = document.querySelector(selettore);
    const reale = getComputedStyle(el)[proprieta];
    // il valore calcolato di ogni opzione, misurato su un elemento sonda
    const sonda = document.createElement("span");
    document.documentElement.appendChild(sonda);
    const corrispondenti = [];
    for (const c of candidati) {
      sonda.style[proprieta] = "";
      sonda.style[proprieta] = c;
      if (sonda.style[proprieta] !== "" && getComputedStyle(sonda)[proprieta] === reale) {
        corrispondenti.push(c);
      }
    }
    sonda.remove();
    return { reale, corrispondenti };
  }, { selettore: caso.selettore, proprieta: caso.proprieta, candidati: caso.candidati || [] });
  await contesto.close();
  return risultato;
}

async function eseguiDom(caso, cartella) {
  const { pagina, contesto, errori } = await apriPagina(caso, cartella, caso.html);
  await pagina.waitForTimeout(caso.attesa || 50);
  const valore = await pagina.evaluate(caso.espressione);
  await contesto.close();
  return { valore: typeof valore === "string" ? valore : JSON.stringify(valore),
           errore: errori.length ? errori[0] : null };
}

function eseguiPug(caso, cartella) {
  // i template inclusi o estesi stanno nella stessa cartella del principale
  const pug = require(path.join(QUI, "node_modules", "pug"));
  scriviFile(caso, cartella);
  const principale = path.join(cartella, caso.principale);
  fs.writeFileSync(principale, caso.sorgente);
  return { html: pug.renderFile(principale, caso.locals || {}) };
}

function portaLibera(porta) {
  return new Promise((risolvi) => {
    const s = net.connect(porta, "127.0.0.1");
    s.on("connect", () => { s.destroy(); risolvi(false); });
    s.on("error", () => risolvi(true));
  });
}

async function attendiPorta(porta, figlio) {
  for (let i = 0; i < 100; i++) {
    if (figlio.exitCode !== null) return false;
    if (!(await portaLibera(porta))) return true;
    await new Promise((r) => setTimeout(r, 100));
  }
  return false;
}

async function eseguiExpress(caso) {
  const porta = 3000;
  if (!(await portaLibera(porta))) throw new Error("la porta 3000 è occupata");
  const file = path.join(QUI, ".caso-express.mjs");
  fs.writeFileSync(file, caso.codice + "\n");
  const figlio = spawn(process.execPath, [file], { cwd: QUI, stdio: ["ignore", "pipe", "pipe"] });
  let uscita = "", errore = "";
  figlio.stdout.on("data", (d) => { uscita += d; });
  figlio.stderr.on("data", (d) => { errore += d; });
  const pronto = await attendiPorta(porta, figlio);
  const risposte = [];
  if (pronto) {
    for (const r of caso.richieste) {
      const opzioni = { method: r.metodo || "GET", redirect: "manual", headers: r.intestazioni || {} };
      if (r.corpo !== undefined) opzioni.body = r.corpo;
      try {
        const risposta = await fetch("http://127.0.0.1:" + porta + r.percorso, opzioni);
        let corpo = (await risposta.text()).trim();
        if (risposta.status >= 300 && risposta.status < 400) {
          corpo = "-> " + risposta.headers.get("location");
        } else if (/<pre>(.*)<\/pre>/s.test(corpo)) {
          // la pagina d'errore predefinita di Express: basta il messaggio
          corpo = corpo.match(/<pre>(.*)<\/pre>/s)[1].split("<br>")[0].trim();
        }
        risposte.push(risposta.status + " " + corpo);
      } catch (e) {
        risposte.push("ERRORE " + e.message);
      }
      await new Promise((ok) => setTimeout(ok, 30));
    }
  }
  figlio.kill();
  await new Promise((ok) => figlio.on("exit", ok));
  fs.rmSync(file, { force: true });
  return { risposte, log: righe(uscita), stderr: pronto ? null : errore.slice(0, 800) };
}

async function main() {
  const casi = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
  const risultati = {};
  for (const caso of casi) {
    const cartella = fs.mkdtempSync(path.join(os.tmpdir(), "verifica-"));
    try {
      if (caso.tipo === "node") risultati[caso.chiave] = eseguiNode(caso, cartella);
      else if (caso.tipo === "browser") risultati[caso.chiave] = await eseguiBrowser(caso, cartella);
      else if (caso.tipo === "css") risultati[caso.chiave] = await eseguiCss(caso, cartella);
      else if (caso.tipo === "dom") risultati[caso.chiave] = await eseguiDom(caso, cartella);
      else if (caso.tipo === "pug") risultati[caso.chiave] = eseguiPug(caso, cartella);
      else if (caso.tipo === "express") risultati[caso.chiave] = await eseguiExpress(caso);
      else risultati[caso.chiave] = { eccezione: "tipo sconosciuto: " + caso.tipo };
    } catch (e) {
      risultati[caso.chiave] = { eccezione: String(e && e.stack || e).slice(0, 600) };
    } finally {
      fs.rmSync(cartella, { recursive: true, force: true });
    }
  }
  if (browser) await browser.close();
  fs.writeFileSync(process.argv[3], JSON.stringify(risultati, null, 1));
}

main().catch((e) => { console.error(e); process.exit(1); });
