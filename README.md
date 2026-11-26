# Canali ETRTO per misura di pneumatico

La prima web app di Stefano, fatta con Claude (app desktop) il 27 aprile 2026: inserisci la misura dello pneumatico (battistrada, spalla, diametro) e ti dice su quali canali può essere montato secondo le tabelle ETRTO.

## Provenienza

- Chat claude.ai «App per compatibilità pneumatici e cerchi» del 2026-04-27, nell'archivio: `_archivio-chat-claude/chat/13-2026-04-27-app-per-compatibilita-pneumatici-e-cerchi.md`.
- `index.html` è il file `etrto_canali.html` generato in quella chat, estratto il 2026-10-24 dall'export grezzo (`_archivio-chat-claude/_raw/conversations-000/conversations.json`), senza modifiche.

## Come funziona

- Tre tendine: battistrada, poi spalla, poi diametro. Il diametro mostra solo i valori che esistono per quella combinazione.
- «Cerca canali» (o Invio) mostra i canali ammessi, con la lettera del bordo (J, B) e il simbolo ½ come nel file originale.
- Scheda «Da ruota a gomma» (dal 2026-11-26): ricerca inversa. Si sceglie il diametro e poi il canale (solo quelli che esistono per quel diametro) e compaiono le misure di pneumatico ammesse, raggruppate per serie (/75 … /30). Gli stessi dati letti al contrario, calcolati nel browser. Avviso fisso: ammessa ETRTO non vuol dire omologata a libretto.

## Dati

- 684 misure incorporate nello script (`const DATA`), ricavate da `Mak/Canali XLS.xlsx`.
- Controllo del 2026-10-24: le 684 misure e i canali coincidono con l'Excel. Uniche differenze sono due spazi in fondo («3½J ») nelle righe 135/80 R15 e 145/80 R12, che l'app aveva già tolto.

## Com'è fatto

- `index.template.html`: l'app, da modificare a mano. Al posto dei dati ha il segnaposto `/*ETRTO_DATA*/`, al posto della data di build `/*BUILD*/`.
- `data/build.py`: legge `Mak/Canali XLS.xlsx` (o il file passato come argomento) senza librerie esterne e scrive `index.html`. **`index.html` non si modifica a mano.**
- Nel build «3½ J» e «3½J» diventano tutti «3½J» (nell'Excel compaiono entrambe le forme).
- Nessuna CDN, funziona offline. Icona Home: `assets/mak.png`.

Per aggiornare i dati (per esempio con una nuova edizione ETRTO nello stesso formato):

    python3 data/build.py ["percorso/del/file.xlsx"]

poi commit e push: GitHub Pages ripubblica da `main`.

## Stato

LIVE dal 2026-10-25: https://stefanoserafin.github.io/mak-etrto-canali/ — in chiaro (tabelle ETRTO, nessun dato riservato). Repo `StefanoSerafin/mak-etrto-canali`, annidato nel workspace.
