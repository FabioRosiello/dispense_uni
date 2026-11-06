#!/usr/bin/env python3
"""Genera i nomi di metodi e tipi usati nei listati Java della dispensa e del cheat sheet.

VS Code colora di giallo i metodi e di verde acqua classi, interfacce e annotazioni; listings non conosce
la grammatica di Java e colora solo le parole che compaiono in un elenco. Lo script legge i listati Java e
produce due elenchi:
  - metodi: identificatori che iniziano con una minuscola e sono seguiti da "(";
  - tipi:   identificatori che iniziano con una maiuscola e contengono una minuscola (le costanti come
            TIMEOUT_MS restano variabili), più le annotazioni (@Test, @Override...).
Scrive due file:
  - preamble/listati-nomi.tex   linguaggio JavaVSCnomi, dai listati con style=java dei capitoli (la dispensa);
  - cheatsheet/listati-nomi.tex linguaggio JavaVSCnomiCS, dai listati con style=javacs del cheat sheet.
Va rilanciato dopo aver aggiunto esempi:  python3 preamble/nomi_listati.py  (dalla cartella IGSW).
"""
import glob
import os
import re

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(QUI)

PAROLE_JAVA = set("""abstract assert boolean break byte case catch char class const continue default do double else
enum extends final finally float for goto if implements import instanceof int interface long native new package
private protected public return short static strictfp super switch synchronized this throw throws transient try void
volatile while var record yield sealed permits true false null""".split())


def raccogli(file_tex, stile):
    """Metodi e tipi dei listati con style=<stile> nei file indicati."""
    metodi, tipi, variabili = set(), set(), set()
    listato = re.compile(r'\\begin\{lstlisting\}\[[^\]]*style=' + stile + r'(?=[,\]\s])[^\]]*\]\n(.*?)\\end\{lstlisting\}',
                         re.S)
    for f in file_tex:
        testo = open(f, encoding='utf-8').read()
        for m in listato.finditer(testo):
            codice = m.group(1)
            # niente stringhe e commenti: "Unità di calcolo(" non e' una chiamata
            codice = re.sub(r'"(?:\\.|[^"\\])*"', '""', codice)
            codice = re.sub(r'//[^\n]*', '', codice)
            codice = re.sub(r'/\*.*?\*/', '', codice, flags=re.S)
            # variabili, campi e parametri dichiarati: restano azzurri anche se altrove c'e' un metodo omonimo
            for nome in re.findall(r'\b(?:[A-Z][\w.]*(?:<[^;()]*?>)?(?:\[\])*|int|long|double|boolean|char|var|float|short|byte)'
                                   r'\s+([a-z][A-Za-z0-9_]*)\s*(?=[=;,):])', codice):
                variabili.add(nome)
            for nome in re.findall(r'\b([a-z][A-Za-z0-9_]*)\s*\(', codice):
                if nome not in PAROLE_JAVA:
                    metodi.add(nome)
            for nome in re.findall(r'(?<![@\w])([A-Z][A-Za-z0-9_]*)\b', codice):
                if re.search(r'[a-z]', nome):
                    tipi.add(nome)
            for nome in re.findall(r'@([A-Z][A-Za-z0-9_]*)', codice):
                tipi.add('@' + nome)
    metodi = {m for m in metodi - variabili if len(m) > 1}
    return metodi, tipi


def elenco(nomi):
    righe, riga = [], '    '
    # a parità di minuscole (timeoutErogazione, timeOutErogazione) decide il nome esatto: l'ordine non dipende
    # dall'ordine casuale degli insiemi di Python, e il file non cambia da un'esecuzione all'altra
    for n in sorted(nomi, key=lambda n: (n.lower(), n)):
        if len(riga) + len(n) + 1 > 100:
            righe.append(riga.rstrip())
            riga = '    '
        riga += n + ','
    righe.append(riga.rstrip().rstrip(','))
    return '\n'.join(righe)


def scrivi(percorso, lingua, descrizione, metodi, tipi):
    with open(percorso, 'w', encoding='utf-8') as out:
        out.write('% File generato da preamble/nomi_listati.py: non modificarlo a mano.\n')
        out.write('% Metodi (giallo) e tipi (verde acqua) che compaiono nei listati Java ' + descrizione + '.\n')
        out.write('\\lstdefinelanguage{' + lingua + '}[]{JavaVSC}{\n')
        out.write('  morekeywords=[3]{\n' + elenco(metodi) + '},\n')
        out.write('  morekeywords=[4]{\n' + elenco(tipi) + '},\n')
        out.write('}\n')
    print(os.path.relpath(percorso, RADICE) + ':', len(metodi), 'metodi,', len(tipi), 'tipi')


capitoli = sorted(glob.glob(os.path.join(RADICE, 'chapters', '*.tex')))
scrivi(os.path.join(QUI, 'listati-nomi.tex'), 'JavaVSCnomi', 'della dispensa', *raccogli(capitoli, 'java'))

cartella_cs = os.path.join(RADICE, 'cheatsheet')
if os.path.isdir(cartella_cs):
    file_cs = sorted(glob.glob(os.path.join(cartella_cs, '*.tex')))
    file_cs = [f for f in file_cs if os.path.basename(f) != 'listati-nomi.tex']
    scrivi(os.path.join(cartella_cs, 'listati-nomi.tex'), 'JavaVSCnomiCS', 'del cheat sheet', *raccogli(file_cs, 'javacs'))
