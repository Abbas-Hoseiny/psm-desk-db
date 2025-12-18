# 🌱 PSM-Desk-DB

> BVL Pflanzenschutzmittel-Datenbank für [PSM-Desk](https://github.com/Abbas-Hoseiny/psm-desk)

## 📋 Übersicht

Dieses Repository enthält die aufbereiteten Daten der BVL (Bundesamt für Verbraucherschutz und Lebensmittelsicherheit) Pflanzenschutzmittel-API.

- **25 BVL-Endpunkte** (Kern + Wichtig)
- **Automatische Aktualisierung** alle 2 Tage via GitHub Actions
- **GZIP-komprimierte** JSON-Dateien für effiziente Übertragung
- **GitHub Pages** für einfachen Zugriff

## 🌐 API-Endpunkt

```
https://abbas-hoseiny.github.io/psm-desk-db/manifest.json
```

## 📁 Dateistruktur

```
psm-desk-db/
├── data/
│   ├── manifest.json          # Metadaten & Checksummen
│   ├── mittel.json.gz         # Zugelassene PSM (~3.000)
│   ├── mittel_abgelaufen.json.gz
│   ├── wirkstoff.json.gz
│   ├── awg.json.gz            # Anwendungsgebiete
│   └── ... (25 Dateien)
├── scripts/
│   ├── config.py              # Konfiguration (25 Endpunkte)
│   ├── fetch_bvl.py           # BVL API Abruf
│   ├── transform.py           # Daten transformieren
│   ├── compress.py            # GZIP Komprimierung
│   └── manifest.py            # Manifest generieren
└── .github/
    └── workflows/
        └── update-db.yml      # Automatischer Update (alle 2 Tage)
```

## 📊 Enthaltene Endpunkte (25)

### ⭐⭐⭐ KERN (15 Endpunkte)

| Endpunkt              | Beschreibung               |
| --------------------- | -------------------------- |
| `/mittel/`            | Zugelassene PSM            |
| `/mittel_abgelaufen/` | Abgelaufene PSM            |
| `/wirkstoff/`         | Wirkstoffe                 |
| `/wirkstoff_gehalt/`  | Wirkstoffgehalt pro Mittel |
| `/awg/`               | Anwendungsgebiete          |
| `/awg_kultur/`        | Kulturen pro AWG           |
| `/awg_schadorg/`      | Schadorganismen pro AWG    |
| `/awg_aufwand/`       | Aufwandmengen              |
| `/awg_wartezeit/`     | Wartezeiten                |
| `/auflagen/`          | Gesetzliche Auflagen       |
| `/kode/`              | Kodelisten-Dekodierung     |
| `/kultur_gruppe/`     | Kultur-Namen               |
| `/schadorg_gruppe/`   | Schadorg-Namen             |
| `/mittel_vertrieb/`   | Vertriebsfirmen            |
| `/adresse/`           | Firmen-Adressen            |

### ⭐⭐ WICHTIG (10 Endpunkte)

| Endpunkt                    | Beschreibung            |
| --------------------------- | ----------------------- |
| `/ghs_gefahrenhinweise/`    | H-Sätze                 |
| `/ghs_sicherheitshinweise/` | P-Sätze                 |
| `/ghs_gefahrensymbole/`     | GHS-Piktogramme         |
| `/mittel_gefahren_symbol/`  | GHS pro Mittel          |
| `/awg_zulassung/`           | Zulassungszeiträume     |
| `/staerkung/`               | Pflanzenstärkungsmittel |
| `/zusatzstoff/`             | Zusatzstoffe            |
| `/hinweis/`                 | Zusätzliche Hinweise    |
| `/kodeliste/`               | Kodelisten-Beschreibung |
| `/stand/`                   | Datenstand              |

## 🔧 Lokale Entwicklung

```bash
# In das Verzeichnis wechseln
cd scripts

# Daten abrufen (Test-Modus: nur 1 Datensatz pro Endpunkt)
python fetch_bvl.py --test

# Vollständiger Abruf (ca. 5-10 Minuten)
python fetch_bvl.py

# Transformieren
python transform.py

# Komprimieren
python compress.py

# Manifest generieren
python manifest.py
```

## 📜 Lizenz

Die Daten stammen von der [BVL PSM-API](https://psm-api.bvl.bund.de) und unterliegen den Nutzungsbedingungen des BVL.

## 🔗 Links

- [PSM-Desk App](https://github.com/Abbas-Hoseiny/psm-desk)
- [BVL PSM-API](https://psm-api.bvl.bund.de)
- [BVL Pflanzenschutzmittel-Verzeichnis](https://www.bvl.bund.de/DE/Arbeitsbereiche/04_Pflanzenschutzmittel/01_Aufgaben/02_ZulssePflszMittel/01_ZugPflSchMittlDt/psm_zugelassen.html)
