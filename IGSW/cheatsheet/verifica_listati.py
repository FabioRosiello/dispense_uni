#!/usr/bin/env python3
"""Compila ed esegue il codice Java del cheat sheet e confronta gli output con quelli stampati.

- Ogni ambiente caso (o struttura) che contiene un listato con style=javacs viene compilato da solo, come un unico
  file: le classi sono tutte senza public tranne al più una, e gli import di java.util e java.time sono sottintesi
  (lo script li aggiunge in testa).
- Ogni ambiente programma è un esempio completo: i suoi listati Java (un file ciascuno, con name=Nome.java oppure
  con il nome della classe public) si compilano insieme, poi si eseguono i comandi del listato «Terminale» (righe che
  iniziano con «$ ») e si confronta l'output con le righe stampate sotto ogni comando. Una riga «...» vale per
  qualunque numero di righe.
- Le righe del codice non devono superare i 52 caratteri: nella colonna del codice (96 mm) non ne stanno di più.
Uso, dalla cartella IGSW:  python3 cheatsheet/verifica_listati.py   (serve un JDK 21: javac e java)
"""
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile

QUI = os.path.dirname(os.path.abspath(__file__))
IMPORT = 'import java.util.*;\nimport java.time.*;\n'
LISTATO = re.compile(r'\\begin\{lstlisting\}\[([^\]]*)\]\n(.*?)\\end\{lstlisting\}', re.S)
AMBIENTE = re.compile(r'\\begin\{(caso|struttura|programma)\}(?:\[[^\]]*\])?\{([^}]*)\}(.*?)\\end\{\1\}', re.S)
MAX_RIGA = 52


def opzione(opzioni, chiave):
    m = re.search(r'(?:^|,)\s*' + chiave + r'=([^,]*)', opzioni)
    return m.group(1).strip() if m else None


def file_di(codice, nome_predefinito):
    """Il nome del file .java: quello della classe public, se c'è."""
    m = re.search(r'^public\s+(?:final\s+|abstract\s+)?(?:class|interface|enum|record)\s+(\w+)', codice, re.M)
    return (m.group(1) if m else nome_predefinito) + '.java'


def compila(cartella, nomi_file):
    esito = subprocess.run(['javac', '-encoding', 'UTF-8', '-Xlint:none', '-nowarn', '-d', cartella] + nomi_file,
                           cwd=cartella, capture_output=True, text=True)
    errori = [r for r in esito.stderr.split('\n') if not r.startswith('Picked up JAVA_TOOL_OPTIONS')]
    return esito.returncode == 0, '\n'.join(errori)


def confronta(atteso, ottenuto):
    """Confronto riga per riga; «...» assorbe un numero qualsiasi di righe."""
    i = j = 0
    while i < len(atteso):
        if atteso[i].strip() == '...':
            if i + 1 == len(atteso):
                return True
            while j < len(ottenuto) and ottenuto[j] != atteso[i + 1]:
                j += 1
            i += 1
            continue
        if j >= len(ottenuto) or atteso[i] != ottenuto[j]:
            return False
        i += 1
        j += 1
    return j == len(ottenuto)


def esegui_terminale(cartella, terminale):
    """Esegue i comandi «$ ...» di un listato Terminale; restituisce l'elenco delle differenze."""
    differenze = []
    righe = terminale.rstrip('\n').split('\n')
    k = 0
    while k < len(righe):
        if not righe[k].startswith('$ '):
            k += 1
            continue
        comando = righe[k][2:]
        atteso = []
        k += 1
        while k < len(righe) and not righe[k].startswith('$ '):
            atteso.append(righe[k])
            k += 1
        if comando.startswith('javac'):
            continue                      # già compilato
        esito = subprocess.run(comando, shell=True, cwd=cartella, capture_output=True, text=True)
        # la JVM può annunciare su stderr le opzioni prese da JAVA_TOOL_OPTIONS: non fa parte dell'output
        ottenuto = [r for r in (esito.stdout + esito.stderr).rstrip('\n').split('\n')
                    if not r.startswith('Picked up JAVA_TOOL_OPTIONS')]
        if not confronta(atteso, ottenuto):
            differenze.append(f'«{comando}»:\n  atteso:   {atteso}\n  ottenuto: {ottenuto}')
    return differenze


errori = 0
casi = 0
programmi = 0
for tex in sorted(glob.glob(os.path.join(QUI, '*.tex'))):
    testo = open(tex, encoding='utf-8').read()
    breve = os.path.basename(tex)
    for m in AMBIENTE.finditer(testo):
        tipo, etichetta, corpo = m.group(1), m.group(2), m.group(3)
        sorgenti, terminali = [], []
        for opz, codice in LISTATO.findall(corpo):
            if opzione(opz, 'style') == 'javacs':
                for riga in codice.split('\n'):
                    if len(riga) > MAX_RIGA:
                        errori += 1
                        print(f'RIGA LUNGA {breve}, {etichetta}: [{len(riga)}] {riga}')
                nome = opzione(opz, 'name') or file_di(codice, 'Caso')
                sorgenti.append((nome, codice))
            elif opzione(opz, 'name') == 'Terminale':
                terminali.append(codice)
        if not sorgenti:
            continue
        if tipo == 'programma':
            programmi += 1
        else:
            casi += 1
        tmp = tempfile.mkdtemp()
        try:
            for nome, codice in sorgenti:
                open(os.path.join(tmp, nome), 'w', encoding='utf-8').write(IMPORT + codice)
            ok, err = compila(tmp, [n for n, _ in sorgenti])
            if not ok:
                errori += 1
                print(f'ERRORE di compilazione {breve}, {etichetta}:\n{err}')
                continue
            if tipo == 'programma':
                if not terminali:
                    errori += 1
                    print(f'MANCA IL TERMINALE {breve}, {etichetta}')
                for terminale in terminali:
                    for d in esegui_terminale(tmp, terminale):
                        errori += 1
                        print(f'OUTPUT DIVERSO {breve}, {etichetta}, {d}')
        finally:
            shutil.rmtree(tmp)

print(f'{casi} casi compilati, {programmi} programmi compilati ed eseguiti, {errori} errori')
sys.exit(1 if errori else 0)
