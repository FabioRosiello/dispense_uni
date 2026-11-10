"""Scelta delle domande di una prova.

Ogni prova è determinata dal suo ID: lo stesso ID (con la stessa banca e le
stesse opzioni) produce sempre la stessa prova. Gli ID sono raggruppati in
*serie* di dieci (1-10, 11-20, ...): dentro una serie le domande vengono
pescate da un mazzo senza reinserimento, quindi dieci prove consecutive non
ripetono una domanda finché la banca lo consente, e i capitoli ruotano in modo
che ogni prova tocchi più argomenti possibile.
"""

import random

from .modello import Famiglia

SERIE = 10

# Quanto spesso un capitolo compare fra le domande chiuse (peso relativo).
PESI = {1: 2, 2: 2, 3: 3, 4: 2, 5: 3, 6: 3, 7: 3, 8: 3, 9: 2, 10: 1, 11: 2, 12: 1, 13: 2,
        14: 2, 15: 3, 16: 1}

TITOLI = {
    1: "Introduzione al Web", 2: "HTML", 3: "CSS", 4: "Layout e Responsive Design",
    5: "JavaScript", 6: "JavaScript avanzato", 7: "JavaScript nel browser",
    8: "Asincronismo e richieste di rete", 9: "Il Web sotto il cofano",
    10: "Il lato server del Web", 11: "Node.js", 12: "Applicazioni web con Node.js",
    13: "Gestione delle sessioni", 14: "CSS moderno e adattivo", 15: "Express",
    16: "Una web app con Express",
}


class Prova:
    def __init__(self, numero, istanze, titolo, minuti):
        self.numero = numero
        self.id_testo = "%05d" % numero
        self.istanze = istanze          # chiuse (per capitolo), poi aperte
        self.titolo = titolo
        self.minuti = minuti


def _mazzo(domande, rng):
    """Le domande di un capitolo in ordine casuale, alternando gli argomenti."""
    per_tema = {}
    for domanda in domande:
        copie = domanda.varianti if isinstance(domanda, Famiglia) else 1
        for variante in range(copie):
            per_tema.setdefault(domanda.tema, []).append((domanda, variante))
    temi = sorted(per_tema)
    rng.shuffle(temi)
    for tema in temi:
        rng.shuffle(per_tema[tema])
    mazzo = []
    while any(per_tema[t] for t in temi):
        for tema in temi:
            if per_tema[tema]:
                mazzo.append(per_tema[tema].pop())
    return mazzo


class _Serie:
    """Lo stato di una serie di prove: mazzi, posizioni e crediti dei capitoli."""

    def __init__(self, banca, capitoli, numero_serie, n_chiuse, n_aperte):
        self.n_chiuse, self.n_aperte = n_chiuse, n_aperte
        self.numero_serie = numero_serie
        rng = random.Random("serie-%d-%s" % (numero_serie, ",".join(map(str, capitoli))))
        self.rng = rng
        self.chiuse = {c: _mazzo([d for d in banca if d.cap == c and not d.aperta], rng)
                       for c in capitoli}
        self.aperte = {c: _mazzo([d for d in banca if d.cap == c and d.aperta], rng)
                       for c in capitoli}
        self.chiuse = {c: m for c, m in self.chiuse.items() if m}
        self.aperte = {c: m for c, m in self.aperte.items() if m}
        self.pos_chiuse = dict.fromkeys(self.chiuse, 0)
        self.pos_aperte = dict.fromkeys(self.aperte, 0)
        # un piccolo credito iniziale casuale decide da quali capitoli si parte
        self.credito_chiuse = {c: rng.random() for c in self.chiuse}
        self.credito_aperte = {c: rng.random() for c in self.aperte}

    def _pesca(self, mazzi, posizioni, crediti, quante, da_evitare, pesi):
        if not mazzi or quante <= 0:
            return []
        totale = float(sum(pesi[c] for c in mazzi))
        for c in mazzi:
            crediti[c] += pesi[c] * quante / totale
        usati = dict.fromkeys(mazzi, 0)
        pescate = []
        for _ in range(quante):
            # prima i capitoli non ancora usati in questa prova, poi il credito
            # (un capitolo già coperto dalle domande chiuse parte svantaggiato)
            c = min(mazzi, key=lambda k: (usati[k],
                                          -(crediti[k] - (0.75 if k in da_evitare else 0)), k))
            usati[c] += 1
            crediti[c] -= 1
            mazzo = mazzi[c]
            giro, indice = divmod(posizioni[c], len(mazzo))
            posizioni[c] += 1
            domanda, variante = mazzo[indice]
            pescate.append((domanda, variante, giro))
        return pescate

    def prossima(self):
        pesi_aperte = dict.fromkeys(PESI, 1)
        chiuse = self._pesca(self.chiuse, self.pos_chiuse, self.credito_chiuse,
                             self.n_chiuse, set(), PESI)
        coperti = {d.cap for d, _, _ in chiuse}
        aperte = self._pesca(self.aperte, self.pos_aperte, self.credito_aperte,
                             self.n_aperte, coperti, pesi_aperte)
        return chiuse, aperte


def componi(numero, banca, n_chiuse=8, n_aperte=3, capitoli=None, titolo=None, minuti=45):
    """Costruisce la prova con l'ID dato."""
    if numero < 1:
        raise ValueError("l'ID della prova parte da 1")
    capitoli = sorted(capitoli or [c for c in sorted({d.cap for d in banca}) if c <= 16])
    numero_serie, posto = divmod(numero - 1, SERIE)
    serie = _Serie(banca, capitoli, numero_serie, n_chiuse, n_aperte)
    for _ in range(posto + 1):
        chiuse, aperte = serie.prossima()
    if len(chiuse) < n_chiuse or len(aperte) < n_aperte:
        raise ValueError("la banca non ha abbastanza domande per i capitoli scelti")

    istanze = []
    for domanda, variante, giro in chiuse + aperte:
        if isinstance(domanda, Famiglia):
            # la variante dipende dalla serie, non dalla singola prova: così
            # due prove della stessa serie non ricevono gli stessi dati
            rng = random.Random("%s:%d:%d:%d" % (domanda.id, numero_serie, variante, giro))
        else:
            rng = random.Random("%s:%d" % (domanda.id, numero))
        istanze.append(domanda.istanza(rng))
    ordine = {id(i): n for n, i in enumerate(istanze)}
    istanze.sort(key=lambda i: (i.aperta, i.cap, ordine[id(i)]))
    return Prova(numero, istanze, titolo or "Prova Scritta di Tecnologie Web", minuti)
