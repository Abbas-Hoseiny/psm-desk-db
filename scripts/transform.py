#!/usr/bin/env python3
"""
BVL Daten Transformer
=====================
Transformiert Rohdaten in normalisierte Struktur für die App.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

from config import DATA_DIR, get_endpoint_count


def load_raw_data(input_dir: str = DATA_DIR) -> dict:
    """Lädt alle Rohdaten"""
    raw_dir = Path(input_dir) / "raw"
    data = {}
    
    for file_path in raw_dir.glob("*.json"):
        name = file_path.stem
        with open(file_path, "r", encoding="utf-8") as f:
            data[name] = json.load(f)
        print(f"  📂 {name}: {len(data[name]):,} Datensätze")
    
    return data


def transform_mittel(raw_data: dict) -> list:
    """Transformiert Mittel-Daten"""
    mittel = raw_data.get("mittel", [])
    
    transformed = []
    for m in mittel:
        transformed.append({
            "kennr": m.get("KENNR", ""),
            "mittelname": m.get("MITTELNAME", ""),
            "formulierung_art": m.get("FORMULIERUNG_ART"),
            "zul_erstmalig_am": m.get("ZUL_ERSTMALIG_AM"),
            "zul_ende": m.get("ZUL_ENDE"),
            "wirkungsbereich": m.get("WIRKUNGSBEREICH"),
            "kennr_zul": m.get("KENNR_ZUL"),
            "is_active": True
        })
    
    return transformed


def transform_mittel_abgelaufen(raw_data: dict) -> list:
    """Transformiert abgelaufene Mittel"""
    mittel = raw_data.get("mittel_abgelaufen", [])
    
    transformed = []
    for m in mittel:
        transformed.append({
            "kennr": m.get("KENNR", ""),
            "mittelname": m.get("MITTELNAME", ""),
            "formulierung_art": m.get("FORMULIERUNG_ART"),
            "zul_erstmalig_am": m.get("ZUL_ERSTMALIG_AM"),
            "zul_ende": m.get("ZUL_ENDE"),
            "aufbrauchfrist": m.get("AUFBRAUCHFRIST"),
            "status": m.get("STATUS"),
            "is_active": False
        })
    
    return transformed


def transform_wirkstoffe(raw_data: dict) -> list:
    """Transformiert Wirkstoffe"""
    wirkstoffe = raw_data.get("wirkstoff", [])
    
    transformed = []
    for w in wirkstoffe:
        transformed.append({
            "wirknr": w.get("WIRKNR", ""),
            "wirkstoffname": w.get("WIRKSTOFFNAME", ""),
            "wirkstoffname_en": w.get("WIRKSTOFFNAME_EN"),
            "cas_nr": w.get("CAS_NR"),
            "kategorie": w.get("KATEGORIE")
        })
    
    return transformed


def transform_wirkstoff_gehalt(raw_data: dict) -> list:
    """Transformiert Wirkstoffgehalt"""
    gehalt = raw_data.get("wirkstoff_gehalt", [])
    
    transformed = []
    for g in gehalt:
        transformed.append({
            "kennr": g.get("KENNR", ""),
            "wirknr": g.get("WIRKNR", ""),
            "gehalt": g.get("GEHALT"),
            "gehalt_einheit": g.get("GEHALT_EINHEIT"),
            "gehalt_art": g.get("GEHALT_ART")
        })
    
    return transformed


def transform_awg(raw_data: dict) -> list:
    """Transformiert Anwendungsgebiete"""
    awg = raw_data.get("awg", [])
    
    transformed = []
    for a in awg:
        transformed.append({
            "awg_id": a.get("AWG_ID"),
            "kennr": a.get("KENNR", ""),
            "awg_auflagen": a.get("AWG_AUFLAGEN"),
            "awg_anwendungsbereich": a.get("AWG_ANWENDUNGSBEREICH"),
            "awg_bis": a.get("AWG_BIS"),
            "awg_von": a.get("AWG_VON"),
            "antragsteller": a.get("ANTRAGSTELLER"),
            "datum": a.get("DATUM")
        })
    
    return transformed


def transform_awg_kultur(raw_data: dict) -> list:
    """Transformiert AWG-Kulturen"""
    kulturen = raw_data.get("awg_kultur", [])
    
    transformed = []
    for k in kulturen:
        transformed.append({
            "awg_id": k.get("AWG_ID"),
            "kultur": k.get("KULTUR", ""),
            "kultur_gruppe": k.get("KULTUR_GRUPPE"),
            "schadorg": k.get("SCHADORG")  # Manchmal enthalten
        })
    
    return transformed


def transform_awg_schadorg(raw_data: dict) -> list:
    """Transformiert AWG-Schadorganismen"""
    schadorg = raw_data.get("awg_schadorg", [])
    
    transformed = []
    for s in schadorg:
        transformed.append({
            "awg_id": s.get("AWG_ID"),
            "schadorg": s.get("SCHADORG", ""),
            "schadorg_gruppe": s.get("SCHADORG_GRUPPE")
        })
    
    return transformed


def transform_awg_aufwand(raw_data: dict) -> list:
    """Transformiert Aufwandmengen"""
    aufwand = raw_data.get("awg_aufwand", [])
    
    transformed = []
    for a in aufwand:
        transformed.append({
            "awg_id": a.get("AWG_ID"),
            "aufwand": a.get("AUFWAND"),
            "aufwand_einheit": a.get("AUFWAND_EINHEIT"),
            "aufwand_text": a.get("AUFWAND_TEXT"),
            "stadium_von": a.get("STADIUM_VON"),
            "stadium_bis": a.get("STADIUM_BIS")
        })
    
    return transformed


def transform_awg_wartezeit(raw_data: dict) -> list:
    """Transformiert Wartezeiten"""
    wartezeit = raw_data.get("awg_wartezeit", [])
    
    transformed = []
    for w in wartezeit:
        transformed.append({
            "awg_id": w.get("AWG_ID"),
            "wartezeit_tage": w.get("WARTEZEIT_TAGE"),
            "wartezeit_text": w.get("WARTEZEIT_TEXT"),
            "kultur": w.get("KULTUR"),
            "ernte_nutzung": w.get("ERNTE_NUTZUNG")
        })
    
    return transformed


def transform_awg_zulassung(raw_data: dict) -> list:
    """Transformiert AWG-Zulassungszeiträume"""
    zulassung = raw_data.get("awg_zulassung", [])
    
    transformed = []
    for z in zulassung:
        transformed.append({
            "awg_id": z.get("AWG_ID"),
            "zulassungsnr": z.get("ZULASSUNGSNR"),
            "zul_von": z.get("ZUL_VON"),
            "zul_bis": z.get("ZUL_BIS"),
            "status": z.get("STATUS")
        })
    
    return transformed


def transform_auflagen(raw_data: dict) -> list:
    """Transformiert Auflagen"""
    auflagen = raw_data.get("auflagen", [])
    
    transformed = []
    for a in auflagen:
        transformed.append({
            "auession": a.get("AUESSION", ""),
            "auession_gruppe": a.get("AUESSION_GRUPPE"),
            "auflage": a.get("AUFLAGE"),
            "auflage_gruppe": a.get("AUFLAGE_GRUPPE")
        })
    
    return transformed


def transform_kode(raw_data: dict) -> list:
    """Transformiert Kodelisten"""
    kode = raw_data.get("kode", [])
    
    transformed = []
    for k in kode:
        transformed.append({
            "koession": k.get("KOESSION", ""),
            "koession_art": k.get("KOESSION_ART", ""),
            "kode_text": k.get("KODE_TEXT"),
            "kode_zusatz": k.get("KODE_ZUSATZ")
        })
    
    return transformed


def transform_kodeliste(raw_data: dict) -> list:
    """Transformiert Kodelisten-Beschreibung"""
    kodeliste = raw_data.get("kodeliste", [])
    
    transformed = []
    for k in kodeliste:
        transformed.append({
            "koession_art": k.get("KOESSION_ART", ""),
            "beschreibung": k.get("BESCHREIBUNG")
        })
    
    return transformed


def transform_kultur_gruppe(raw_data: dict) -> list:
    """Transformiert Kultur-Gruppen (Lookup)"""
    kulturen = raw_data.get("kultur_gruppe", [])
    
    transformed = []
    for k in kulturen:
        transformed.append({
            "kultur": k.get("KULTUR", ""),
            "kultur_name": k.get("KULTUR_NAME", ""),
            "eppo_code": k.get("EPPO_CODE"),
            "kultur_gruppe": k.get("KULTUR_GRUPPE")
        })
    
    return transformed


def transform_schadorg_gruppe(raw_data: dict) -> list:
    """Transformiert Schadorganismen-Gruppen (Lookup)"""
    schadorg = raw_data.get("schadorg_gruppe", [])
    
    transformed = []
    for s in schadorg:
        transformed.append({
            "schadorg": s.get("SCHADORG", ""),
            "schadorg_name": s.get("SCHADORG_NAME", ""),
            "eppo_code": s.get("EPPO_CODE"),
            "schadorg_gruppe": s.get("SCHADORG_GRUPPE")
        })
    
    return transformed


def transform_adresse(raw_data: dict) -> list:
    """Transformiert Adressen"""
    adressen = raw_data.get("adresse", [])
    
    transformed = []
    for a in adressen:
        transformed.append({
            "aession": a.get("AESSION", ""),
            "firma": a.get("FIRMA"),
            "strasse": a.get("STRASSE"),
            "plz": a.get("PLZ"),
            "ort": a.get("ORT"),
            "land": a.get("LAND"),
            "telefon": a.get("TELEFON"),
            "email": a.get("EMAIL"),
            "url": a.get("URL")
        })
    
    return transformed


def transform_mittel_vertrieb(raw_data: dict) -> list:
    """Transformiert Mittel-Vertrieb"""
    vertrieb = raw_data.get("mittel_vertrieb", [])
    
    transformed = []
    for v in vertrieb:
        transformed.append({
            "kennr": v.get("KENNR", ""),
            "aession": v.get("AESSION", ""),
            "vertrieb_art": v.get("VERTRIEB_ART")
        })
    
    return transformed


def transform_ghs_gefahrenhinweise(raw_data: dict) -> list:
    """Transformiert GHS H-Sätze"""
    hinweise = raw_data.get("ghs_gefahrenhinweise", [])
    
    transformed = []
    for h in hinweise:
        transformed.append({
            "h_nr": h.get("H_NR", ""),
            "h_text": h.get("H_TEXT", ""),
            "signalwort": h.get("SIGNALWORT")
        })
    
    return transformed


def transform_ghs_sicherheitshinweise(raw_data: dict) -> list:
    """Transformiert GHS P-Sätze"""
    hinweise = raw_data.get("ghs_sicherheitshinweise", [])
    
    transformed = []
    for h in hinweise:
        transformed.append({
            "p_nr": h.get("P_NR", ""),
            "p_text": h.get("P_TEXT", "")
        })
    
    return transformed


def transform_ghs_gefahrensymbole(raw_data: dict) -> list:
    """Transformiert GHS-Symbole"""
    symbole = raw_data.get("ghs_gefahrensymbole", [])
    
    transformed = []
    for s in symbole:
        transformed.append({
            "symbol": s.get("SYMBOL", ""),
            "symbol_text": s.get("SYMBOL_TEXT", ""),
            "bild_url": s.get("BILD_URL")
        })
    
    return transformed


def transform_mittel_gefahren_symbol(raw_data: dict) -> list:
    """Transformiert Mittel-GHS-Zuordnung"""
    symbole = raw_data.get("mittel_gefahren_symbol", [])
    
    transformed = []
    for s in symbole:
        transformed.append({
            "kennr": s.get("KENNR", ""),
            "symbol": s.get("SYMBOL", ""),
            "h_nr": s.get("H_NR"),
            "p_nr": s.get("P_NR")
        })
    
    return transformed


def transform_hinweis(raw_data: dict) -> list:
    """Transformiert Hinweise"""
    hinweise = raw_data.get("hinweis", [])
    
    transformed = []
    for h in hinweise:
        transformed.append({
            "kennr": h.get("KENNR", ""),
            "hinweis_art": h.get("HINWEIS_ART"),
            "hinweis_text": h.get("HINWEIS_TEXT")
        })
    
    return transformed


def transform_staerkung(raw_data: dict) -> list:
    """Transformiert Pflanzenstärkungsmittel"""
    staerkung = raw_data.get("staerkung", [])
    
    transformed = []
    for s in staerkung:
        transformed.append({
            "kennr": s.get("KENNR", ""),
            "mittelname": s.get("MITTELNAME", ""),
            "formulierung_art": s.get("FORMULIERUNG_ART"),
            "antragsteller": s.get("ANTRAGSTELLER"),
            "listung_von": s.get("LISTUNG_VON"),
            "listung_bis": s.get("LISTUNG_BIS")
        })
    
    return transformed


def transform_zusatzstoff(raw_data: dict) -> list:
    """Transformiert Zusatzstoffe"""
    zusatzstoff = raw_data.get("zusatzstoff", [])
    
    transformed = []
    for z in zusatzstoff:
        transformed.append({
            "kennr": z.get("KENNR", ""),
            "mittelname": z.get("MITTELNAME", ""),
            "formulierung_art": z.get("FORMULIERUNG_ART"),
            "antragsteller": z.get("ANTRAGSTELLER"),
            "listung_von": z.get("LISTUNG_VON"),
            "listung_bis": z.get("LISTUNG_BIS")
        })
    
    return transformed


def transform_stand(raw_data: dict) -> list:
    """Transformiert Datenstand"""
    stand = raw_data.get("stand", [])
    
    transformed = []
    for s in stand:
        transformed.append({
            "stand_datum": s.get("STAND_DATUM"),
            "stand_text": s.get("STAND_TEXT"),
            "version": s.get("VERSION")
        })
    
    return transformed


def transform_all(raw_data: dict) -> dict:
    """Transformiert alle Daten"""
    print("\n🔄 Transformiere Daten...")
    
    transformers = {
        "mittel": transform_mittel,
        "mittel_abgelaufen": transform_mittel_abgelaufen,
        "wirkstoff": transform_wirkstoffe,
        "wirkstoff_gehalt": transform_wirkstoff_gehalt,
        "awg": transform_awg,
        "awg_kultur": transform_awg_kultur,
        "awg_schadorg": transform_awg_schadorg,
        "awg_aufwand": transform_awg_aufwand,
        "awg_wartezeit": transform_awg_wartezeit,
        "awg_zulassung": transform_awg_zulassung,
        "auflagen": transform_auflagen,
        "kode": transform_kode,
        "kodeliste": transform_kodeliste,
        "kultur_gruppe": transform_kultur_gruppe,
        "schadorg_gruppe": transform_schadorg_gruppe,
        "adresse": transform_adresse,
        "mittel_vertrieb": transform_mittel_vertrieb,
        "ghs_gefahrenhinweise": transform_ghs_gefahrenhinweise,
        "ghs_sicherheitshinweise": transform_ghs_sicherheitshinweise,
        "ghs_gefahrensymbole": transform_ghs_gefahrensymbole,
        "mittel_gefahren_symbol": transform_mittel_gefahren_symbol,
        "hinweis": transform_hinweis,
        "staerkung": transform_staerkung,
        "zusatzstoff": transform_zusatzstoff,
        "stand": transform_stand,
    }
    
    transformed = {}
    for name, transformer in transformers.items():
        if name in raw_data:
            transformed[name] = transformer(raw_data)
            print(f"  ✅ {name}: {len(transformed[name]):,} Datensätze")
        else:
            print(f"  ⚠️ {name}: keine Rohdaten vorhanden")
            transformed[name] = []
    
    return transformed


def save_transformed_data(data: dict, output_dir: str = DATA_DIR):
    """Speichert transformierte Daten"""
    out_dir = Path(output_dir) / "transformed"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    for name, items in data.items():
        file_path = out_dir / f"{name}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False)
        print(f"  💾 {name}.json")


def main():
    """Hauptfunktion"""
    print("📂 Lade Rohdaten...")
    raw_data = load_raw_data()
    
    if not raw_data:
        print("❌ Keine Rohdaten gefunden! Bitte erst fetch_bvl.py ausführen.")
        return 1
    
    transformed = transform_all(raw_data)
    
    print("\n💾 Speichere transformierte Daten...")
    save_transformed_data(transformed)
    
    print("\n✅ Transformation abgeschlossen!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
