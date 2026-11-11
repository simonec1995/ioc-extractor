# ioc-extractor

Piccolo strumento da riga di comando in Python che estrae gli **Indicatori di Compromissione (IoC)** da report di threat intelligence e da testi semplici.

Gestisce anche gli indicatori *defangati* (ad esempio `hxxp://evil[.]com`) e stampa un elenco pulito e senza doppioni.

## Cosa estrae

- URL
- Domini
- Indirizzi IPv4
- Hash di file (MD5, SHA1, SHA256)
- Indirizzi email

## Requisiti

Python 3.9 o successivo. Nessuna dipendenza esterna.

## Utilizzo

```
python3 ioc_extractor.py sample_report.txt
```

Esempio di output:

```
[URL]
  http://malware-example.net/payload.exe
[Dominio]
  evil-example.com
  malware-example.net
[IPv4]
  203.0.113.45
[SHA256]
  275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f
[Email]
  phisher@bad-example.org
```

## Come funziona

1. **Refang**: riporta il testo defangato alla forma normale (`[.]` diventa `.`, `hxxp` diventa `http`).
2. **Estrazione**: le espressioni regolari cercano ogni tipo di indicatore.
3. **Eliminazione dei doppioni**: i risultati vengono salvati in insiemi (set) e stampati in ordine alfabetico.

## Limiti noti

- I nomi di file come `payload.exe` vengono esclusi dall'elenco dei domini tramite un elenco fisso di estensioni, quindi estensioni insolite possono generare falsi positivi.
- Numeri di versione come `1.2.3.4` possono essere scambiati per indirizzi IPv4.
- Gli indirizzi IPv6 e i domini degli indirizzi email non vengono ancora estratti.
- L'output non è defangato: non cliccare né aprire gli indicatori estratti.

## Avvertenza

`sample_report.txt` contiene indicatori inventati a scopo di test. L'hash SHA256 è quello del file di test EICAR, innocuo, usato per provare gli antivirus.

## Autore

Simone Calogero Lauria, studente di cybersecurity e analista junior.

## Licenza

MIT
