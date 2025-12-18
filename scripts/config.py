#!/usr/bin/env python3
"""
PSM-Desk-DB Konfiguration
=========================
Alle 25 BVL-Endpunkte (Kern + Wichtig)
"""

# BVL API Basis-URL
BVL_BASE_URL = "https://psm-api.bvl.bund.de/ords/psm/api-v1"

# Pagination
DEFAULT_LIMIT = 1000
MAX_RETRIES = 3
RETRY_DELAY = 2  # Sekunden

# Output-Verzeichnis
DATA_DIR = "data"

# ============================================================================
# 25 ENDPUNKTE (Variante B: Kern + Wichtig)
# ============================================================================

# Sync-Reihenfolge ist WICHTIG wegen Abhängigkeiten!
# 1. Lookup-Tabellen zuerst (keine Abhängigkeiten)
# 2. Haupttabellen (referenzieren Lookups)
# 3. Verknüpfungstabellen (referenzieren Haupttabellen)

ENDPOINTS = {
    # ========================================
    # GRUPPE 1: Lookup-Tabellen (keine Abhängigkeiten)
    # ========================================
    "kode": {
        "path": "/kode/",
        "description": "Kodelisten-Dekodierung",
        "priority": 1,
        "group": "lookup"
    },
    "kodeliste": {
        "path": "/kodeliste/",
        "description": "Kodelisten-Beschreibung",
        "priority": 1,
        "group": "lookup"
    },
    "kultur_gruppe": {
        "path": "/kultur_gruppe/",
        "description": "Kultur-Namen",
        "priority": 1,
        "group": "lookup"
    },
    "schadorg_gruppe": {
        "path": "/schadorg_gruppe/",
        "description": "Schadorganismen-Namen",
        "priority": 1,
        "group": "lookup"
    },
    "ghs_gefahrenhinweise": {
        "path": "/ghs_gefahrenhinweise/",
        "description": "H-Sätze (Hazard Statements)",
        "priority": 1,
        "group": "lookup"
    },
    "ghs_sicherheitshinweise": {
        "path": "/ghs_sicherheitshinweise/",
        "description": "P-Sätze (Precautionary Statements)",
        "priority": 1,
        "group": "lookup"
    },
    "ghs_gefahrensymbole": {
        "path": "/ghs_gefahrensymbole/",
        "description": "GHS-Piktogramme",
        "priority": 1,
        "group": "lookup"
    },
    "hinweis": {
        "path": "/hinweis/",
        "description": "Zusätzliche Hinweise",
        "priority": 1,
        "group": "lookup"
    },
    "stand": {
        "path": "/stand/",
        "description": "Datenstand der BVL-Datenbank",
        "priority": 1,
        "group": "lookup"
    },
    
    # ========================================
    # GRUPPE 2: Stammdaten (referenzieren Lookups)
    # ========================================
    "wirkstoff": {
        "path": "/wirkstoff/",
        "description": "Wirkstoffe",
        "priority": 2,
        "group": "stamm"
    },
    "adresse": {
        "path": "/adresse/",
        "description": "Firmen-Adressen",
        "priority": 2,
        "group": "stamm"
    },
    "auflagen": {
        "path": "/auflagen/",
        "description": "Gesetzliche Auflagen",
        "priority": 2,
        "group": "stamm"
    },
    
    # ========================================
    # GRUPPE 3: Haupttabellen (Mittel)
    # ========================================
    "mittel": {
        "path": "/mittel/",
        "description": "Zugelassene Pflanzenschutzmittel",
        "priority": 3,
        "group": "mittel"
    },
    "mittel_abgelaufen": {
        "path": "/mittel_abgelaufen/",
        "description": "Abgelaufene Mittel mit Aufbrauchfrist",
        "priority": 3,
        "group": "mittel"
    },
    "staerkung": {
        "path": "/staerkung/",
        "description": "Pflanzenstärkungsmittel",
        "priority": 3,
        "group": "mittel"
    },
    "zusatzstoff": {
        "path": "/zusatzstoff/",
        "description": "Zusatzstoffe",
        "priority": 3,
        "group": "mittel"
    },
    
    # ========================================
    # GRUPPE 4: Mittel-Verknüpfungen
    # ========================================
    "wirkstoff_gehalt": {
        "path": "/wirkstoff_gehalt/",
        "description": "Wirkstoffgehalt pro Mittel",
        "priority": 4,
        "group": "mittel_rel"
    },
    "mittel_vertrieb": {
        "path": "/mittel_vertrieb/",
        "description": "Vertriebsfirmen pro Mittel",
        "priority": 4,
        "group": "mittel_rel"
    },
    "mittel_gefahren_symbol": {
        "path": "/mittel_gefahren_symbol/",
        "description": "GHS-Symbole pro Mittel",
        "priority": 4,
        "group": "mittel_rel"
    },
    
    # ========================================
    # GRUPPE 5: Anwendungsgebiete (AWG)
    # ========================================
    "awg": {
        "path": "/awg/",
        "description": "Anwendungsgebiete",
        "priority": 5,
        "group": "awg"
    },
    "awg_zulassung": {
        "path": "/awg_zulassung/",
        "description": "Zulassungszeiträume pro AWG",
        "priority": 5,
        "group": "awg"
    },
    
    # ========================================
    # GRUPPE 6: AWG-Verknüpfungen
    # ========================================
    "awg_kultur": {
        "path": "/awg_kultur/",
        "description": "Kulturen pro Anwendungsgebiet",
        "priority": 6,
        "group": "awg_rel"
    },
    "awg_schadorg": {
        "path": "/awg_schadorg/",
        "description": "Schadorganismen pro Anwendungsgebiet",
        "priority": 6,
        "group": "awg_rel"
    },
    "awg_aufwand": {
        "path": "/awg_aufwand/",
        "description": "Aufwandmengen pro Anwendungsgebiet",
        "priority": 6,
        "group": "awg_rel"
    },
    "awg_wartezeit": {
        "path": "/awg_wartezeit/",
        "description": "Wartezeiten pro Anwendungsgebiet",
        "priority": 6,
        "group": "awg_rel"
    },
}

def get_endpoints_by_priority():
    """Gibt Endpunkte sortiert nach Priorität zurück"""
    sorted_endpoints = sorted(
        ENDPOINTS.items(),
        key=lambda x: (x[1]["priority"], x[0])
    )
    return [(name, cfg) for name, cfg in sorted_endpoints]

def get_endpoint_count():
    """Gibt die Anzahl der Endpunkte zurück"""
    return len(ENDPOINTS)

if __name__ == "__main__":
    print(f"PSM-Desk-DB: {get_endpoint_count()} BVL-Endpunkte konfiguriert")
    print("\nEndpunkte nach Priorität:")
    for name, cfg in get_endpoints_by_priority():
        print(f"  {cfg['priority']}. {name:25} - {cfg['description']}")
