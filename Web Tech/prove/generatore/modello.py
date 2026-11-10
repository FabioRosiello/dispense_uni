"""Il modello delle domande: chiuse, aperte e famiglie parametriche.

Una domanda della banca è una *ricetta*: dalla stessa domanda escono prove
diverse, perché ogni volta si estraggono i distrattori, si mescolano le opzioni
e, per le famiglie, si rigenerano i dati. L'oggetto pronto per la stampa è
l'`Istanza`.
"""

import random
import textwrap

from .markup import a_latex, larghezza_stimata, testo_semplice, AMMESSI_CODICE

LINGUE = ("js", "html", "css", "http", "pug", "php", "json", "sh", "sql", "testo")

# Larghezze utili (in caratteri) dei listati in corpo \footnotesize: una
# colonna di listings è larga 5,1 pt.
CARATTERI_RIGA = 100       # listato a tutta larghezza
CARATTERI_SINISTRA = 50    # listato di sinistra, quando sono affiancati
CARATTERI_DESTRA = 45      # listato di destra

NESSUNA = "Nessuna delle altre"


class ErroreBanca(ValueError):
    pass


class Listato:
    """Un frammento di codice da mostrare in un riquadro numerato."""

    def __init__(self, lingua, sorgente, primo=1):
        if lingua not in LINGUE:
            raise ErroreBanca("lingua del listato sconosciuta: %r" % lingua)
        sorgente = textwrap.dedent(sorgente).strip("\n")
        righe = [r.rstrip() for r in sorgente.split("\n")]
        for r in righe:
            for c in r:
                if c == "\t" or (ord(c) > 126 and c not in AMMESSI_CODICE):
                    raise ErroreBanca("carattere %r non previsto nel listato: %r" % (c, r))
        self.lingua = lingua
        self.righe = righe
        self.primo = primo

    @property
    def sorgente(self):
        return "\n".join(self.righe)

    @property
    def larghezza(self):
        return max(len(r) for r in self.righe)


def L(lingua, sorgente, primo=1):
    """Scorciatoia per scrivere un listato nella banca."""
    return Listato(lingua, sorgente, primo)


def _listati(codice):
    if codice is None:
        return []
    if isinstance(codice, Listato):
        return [codice]
    codice = list(codice)
    if len(codice) > 2:
        raise ErroreBanca("al massimo due listati per domanda")
    for c in codice:
        if not isinstance(c, Listato):
            raise ErroreBanca("i listati vanno scritti con L(lingua, sorgente)")
    return codice


class Istanza:
    """Una domanda pronta per la stampa (testi ancora nel mini-markup)."""

    def __init__(self, domanda, testo, codice, dopo, opzioni, spiegazione, rif, righe=None,
                 traccia=None):
        self.domanda = domanda          # la ricetta da cui viene
        self.id = domanda.id
        self.cap = domanda.cap
        self.tema = domanda.tema
        self.punti = domanda.punti
        self.aperta = domanda.aperta
        self.testo = testo
        self.codice = codice            # lista di Listato (0, 1 o 2)
        self.dopo = dopo                # testo dopo il codice, o None
        self.opzioni = opzioni          # lista di (testo, corretta); [] per le aperte
        self.spiegazione = spiegazione
        self.rif = rif
        self.righe = righe              # righe per la risposta (aperte)
        self.traccia = traccia or []    # punti della risposta attesa (aperte)

    @property
    def lettere_giuste(self):
        return [chr(65 + i) for i, (_, ok) in enumerate(self.opzioni) if ok]

    def due_colonne(self):
        """Le opzioni stanno affiancate su due colonne?"""
        # una colonna è larga 227,7 pt, tolti la casella e il suo margine
        return all(larghezza_stimata(t) <= 228.5 for t, _ in self.opzioni)


class Chiusa:
    """Domanda a risposta chiusa (2 punti).

    giuste, sbagliate   testi delle opzioni corrette e dei distrattori. Se le
                        giuste sono più d'una la domanda è a risposta multipla
                        (salvo multi=False: allora sono formulazioni
                        alternative dell'unica risposta giusta).
    multi               True per le domande del tipo «Quali delle seguenti…»,
                        in cui chi risponde non sa quante siano le giuste.
    n                   numero di opzioni da mostrare (di norma 4 o 6).
    quante_giuste       (min, max) opzioni corrette da mostrare nelle multiple.
    nessuna             True se ha senso aggiungere «Nessuna delle altre».
    fisse               True per mostrare tutte le opzioni, senza estrazione.
    """

    aperta = False

    def __init__(self, id, cap, tema, testo, giuste, sbagliate, codice=None, dopo=None,
                 spiegazione="", rif=None, multi=None, n=None, quante_giuste=None,
                 nessuna=False, fisse=False, verifica=None, punti=2, fonte=None):
        self.id = id
        self.cap = cap
        self.tema = tema
        self.testo = testo
        self.giuste = [giuste] if isinstance(giuste, str) else list(giuste)
        self.sbagliate = [sbagliate] if isinstance(sbagliate, str) else list(sbagliate)
        self.codice = _listati(codice)
        self.dopo = dopo
        self.spiegazione = spiegazione
        self.rif = rif
        self.multi = (len(self.giuste) > 1) if multi is None else multi
        self.n = n
        self.quante_giuste = quante_giuste
        self.nessuna = nessuna
        self.fisse = fisse
        self.verifica = verifica
        self.punti = punti
        self.fonte = fonte
        self._controlla()

    # ------------------------------------------------------------------
    def _controlla(self):
        dove = "domanda %r" % self.id
        if not self.giuste:
            raise ErroreBanca("%s: nessuna risposta giusta" % dove)
        if len(self.sbagliate) < (1 if self.fisse else 3):
            raise ErroreBanca("%s: servono almeno 3 distrattori" % dove)
        # maiuscole e minuscole contano solo nel codice (H1 e h1 sono opzioni diverse)
        tutte = [testo_semplice(t).strip() if t.lstrip().startswith("`")
                 else testo_semplice(t).strip().lower() for t in self.giuste + self.sbagliate]
        if len(set(tutte)) != len(tutte):
            doppie = sorted({t for t in tutte if tutte.count(t) > 1})
            raise ErroreBanca("%s: opzioni ripetute: %s" % (dove, doppie))
        if not self.spiegazione:
            raise ErroreBanca("%s: manca la spiegazione" % dove)
        for testo in [self.testo, self.dopo, self.spiegazione] + self.giuste + self.sbagliate:
            a_latex(testo)      # solleva ErroreMarkup se il testo non è valido
        _controlla_listati(self.codice, dove)

    # ------------------------------------------------------------------
    def istanza(self, rng):
        """Estrae le opzioni e le mescola."""
        giuste, sbagliate = list(self.giuste), list(self.sbagliate)
        rng.shuffle(giuste)
        rng.shuffle(sbagliate)
        if self.fisse:
            scelte = [(t, True) for t in self.giuste] + [(t, False) for t in self.sbagliate]
        elif self.multi:
            scelte = self._estrai_multipla(rng, giuste, sbagliate)
        else:
            scelte = self._estrai_singola(rng, giuste, sbagliate)
        rng.shuffle(scelte)
        return Istanza(self, self.testo, self.codice, self.dopo, scelte, self.spiegazione,
                       self.rif)

    def _estrai_singola(self, rng, giuste, sbagliate):
        n = self.n or (6 if len(sbagliate) >= 5 else 4)
        n = min(n, len(sbagliate) + 1)
        sorte = rng.random()
        if self.nessuna and sorte < 0.10 and len(sbagliate) >= n - 1:
            # la risposta giusta non c'è: vale «Nessuna delle altre»
            return [(t, False) for t in sbagliate[:n - 1]] + [(NESSUNA, True)]
        if self.nessuna and sorte < 0.35:
            return ([(giuste[0], True)] + [(t, False) for t in sbagliate[:n - 2]]
                    + [(NESSUNA, False)])
        return [(giuste[0], True)] + [(t, False) for t in sbagliate[:n - 1]]

    def _estrai_multipla(self, rng, giuste, sbagliate):
        n = self.n or 6
        n = min(n, len(giuste) + len(sbagliate))
        minimo, massimo = self.quante_giuste or (1, 3)
        massimo = min(massimo, len(giuste), n - 1)
        minimo = max(min(minimo, massimo), n - len(sbagliate))
        massimo = max(minimo, massimo)
        # chi risponde non sa quante siano le giuste: di solito due, a volte
        # una sola o tre
        possibili = list(range(minimo, massimo + 1))
        pesi = [{1: 2, 2: 5, 3: 3}.get(k, 1) for k in possibili]
        k = rng.choices(possibili, weights=pesi)[0]
        scelte = [(t, True) for t in giuste[:k]] + [(t, False) for t in sbagliate[:n - k]]
        if self.nessuna and rng.random() < 0.3:
            # prende il posto di un distrattore
            for i in range(len(scelte) - 1, -1, -1):
                if not scelte[i][1]:
                    scelte[i] = (NESSUNA, False)
                    break
        return scelte

    # ------------------------------------------------------------------
    def istanza_completa(self):
        """Tutte le opzioni, nell'ordine della banca (per la raccolta)."""
        scelte = [(t, True) for t in self.giuste] + [(t, False) for t in self.sbagliate]
        return Istanza(self, self.testo, self.codice, self.dopo, scelte, self.spiegazione,
                       self.rif)


class Aperta:
    """Domanda a risposta aperta (5 punti), con la traccia della risposta."""

    aperta = True

    def __init__(self, id, cap, tema, testo, traccia, codice=None, rif=None, punti=5,
                 righe=6, fonte=None):
        self.id = id
        self.cap = cap
        self.tema = tema
        self.testo = testo
        self.traccia = [traccia] if isinstance(traccia, str) else list(traccia)
        self.codice = _listati(codice)
        self.rif = rif
        self.punti = punti
        self.righe = righe
        self.fonte = fonte
        self.verifica = None
        dove = "domanda aperta %r" % self.id
        if not self.traccia:
            raise ErroreBanca("%s: manca la traccia della risposta" % dove)
        for testo in [self.testo] + self.traccia:
            a_latex(testo)
        _controlla_listati(self.codice, dove)

    def istanza(self, rng=None):
        return Istanza(self, self.testo, self.codice, None, [], "", self.rif,
                       righe=self.righe, traccia=self.traccia)

    istanza_completa = istanza


class Famiglia:
    """Domanda parametrica: una funzione che, dato un generatore casuale,
    costruisce ogni volta una Chiusa diversa (con la risposta calcolata)."""

    aperta = False

    def __init__(self, id, cap, tema, funzione, varianti=3, punti=2):
        self.id = id
        self.cap = cap
        self.tema = tema
        self.funzione = funzione
        self.varianti = varianti      # quante volte compare nel mazzo di una serie
        self.punti = punti
        self.fonte = None

    def genera(self, rng):
        """La Chiusa di una variante."""
        domanda = self.funzione(rng)
        if not isinstance(domanda, Chiusa):
            raise ErroreBanca("la famiglia %r deve restituire una Chiusa" % self.id)
        return domanda

    def istanza(self, rng):
        domanda = self.genera(rng)
        istanza = domanda.istanza(rng)
        istanza.id = self.id
        return istanza

    def istanza_completa(self):
        domanda = self.genera(random.Random(self.id))
        istanza = domanda.istanza_completa()
        istanza.id = self.id
        return istanza


def _controlla_listati(listati, dove):
    if len(listati) == 1 and listati[0].larghezza > CARATTERI_RIGA:
        raise ErroreBanca("%s: riga di codice troppo lunga (%d caratteri)"
                          % (dove, listati[0].larghezza))
    if len(listati) == 2:
        for listato in listati:
            if listato.larghezza > CARATTERI_RIGA:
                raise ErroreBanca("%s: riga di codice troppo lunga" % dove)


def disposizione(listati):
    """Come affiancare due listati: (frazione sinistra, frazione destra) della
    riga, oppure None se vanno uno sotto l'altro.

    Le prove del corso usano 0,50 e 0,45; quando una riga non ci sta, le due
    colonne si dividono lo spazio in proporzione alle righe più lunghe.
    """
    if len(listati) != 2:
        return None
    a, b = listati[0].larghezza, listati[1].larghezza
    if a <= CARATTERI_SINISTRA and b <= CARATTERI_DESTRA:
        return (0.5, 0.45)
    if a + b <= 92:
        # 5,1 pt per carattere, più i margini interni del riquadro
        sinistra, destra = a * 5.1 + 10, b * 5.1 + 10
        frazione = 0.95 * sinistra / (sinistra + destra)
        return (round(frazione, 3), round(0.95 - frazione, 3))
    return None


def affiancabili(listati):
    """Due listati stanno uno accanto all'altro?"""
    return disposizione(listati) is not None
