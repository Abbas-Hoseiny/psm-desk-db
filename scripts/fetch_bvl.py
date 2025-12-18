#!/usr/bin/env python3
"""
BVL API Fetcher
===============
Lädt alle 25 Endpunkte von der BVL API mit Pagination und Retry-Logik.
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

from config import (
    BVL_BASE_URL,
    DEFAULT_LIMIT,
    MAX_RETRIES,
    RETRY_DELAY,
    DATA_DIR,
    get_endpoints_by_priority,
    get_endpoint_count
)


def fetch_with_retry(url: str, retries: int = MAX_RETRIES) -> dict:
    """Fetch URL mit Retry-Logik"""
    last_error = None
    
    for attempt in range(retries):
        try:
            req = Request(url, headers={
                "Accept": "application/json",
                "User-Agent": "PSM-Desk-DB/1.0"
            })
            with urlopen(req, timeout=60) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as e:
            last_error = e
            if e.code == 429:  # Too Many Requests
                wait_time = RETRY_DELAY * (attempt + 1) * 2
                print(f"    ⏳ Rate limited, warte {wait_time}s...")
                time.sleep(wait_time)
            elif e.code >= 500:  # Server Error
                wait_time = RETRY_DELAY * (attempt + 1)
                print(f"    ⚠️ Server Error {e.code}, Retry in {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
        except URLError as e:
            last_error = e
            wait_time = RETRY_DELAY * (attempt + 1)
            print(f"    ⚠️ Netzwerkfehler, Retry in {wait_time}s...")
            time.sleep(wait_time)
    
    raise last_error


def fetch_endpoint(name: str, path: str) -> list:
    """
    Fetch einen Endpunkt mit Pagination.
    Gibt alle Datensätze zurück.
    """
    all_items = []
    offset = 0
    
    while True:
        url = f"{BVL_BASE_URL}{path}?limit={DEFAULT_LIMIT}&offset={offset}"
        
        try:
            data = fetch_with_retry(url)
        except Exception as e:
            print(f"    ❌ Fehler bei Offset {offset}: {e}")
            break
        
        items = data.get("items", [])
        if not items:
            break
        
        all_items.extend(items)
        
        # Prüfen ob es mehr Daten gibt
        if len(items) < DEFAULT_LIMIT:
            break
        
        offset += DEFAULT_LIMIT
        
        # Fortschritt anzeigen bei großen Datensätzen
        if offset % 5000 == 0:
            print(f"    📥 {len(all_items):,} Datensätze geladen...")
        
        # Kurze Pause um API nicht zu überlasten
        time.sleep(0.1)
    
    return all_items


def fetch_all_endpoints(test_mode: bool = False) -> dict:
    """
    Fetch alle 25 Endpunkte in der richtigen Reihenfolge.
    
    Args:
        test_mode: Wenn True, nur ersten Datensatz pro Endpunkt laden
    
    Returns:
        Dictionary mit allen Daten
    """
    results = {}
    total = get_endpoint_count()
    
    print(f"\n{'='*60}")
    print(f"🌐 BVL API Fetch - {total} Endpunkte")
    print(f"{'='*60}")
    print(f"📅 Start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🔧 Test-Modus: {'JA (nur 1 Datensatz)' if test_mode else 'NEIN (alle Daten)'}")
    print(f"{'='*60}\n")
    
    start_time = time.time()
    
    for idx, (name, cfg) in enumerate(get_endpoints_by_priority(), 1):
        path = cfg["path"]
        desc = cfg["description"]
        group = cfg["group"]
        
        print(f"[{idx:2}/{total}] 📡 {name}")
        print(f"        Gruppe: {group} | {desc}")
        
        endpoint_start = time.time()
        
        try:
            if test_mode:
                # Test-Modus: nur 1 Datensatz
                url = f"{BVL_BASE_URL}{path}?limit=1&offset=0"
                data = fetch_with_retry(url)
                items = data.get("items", [])
            else:
                items = fetch_endpoint(name, path)
            
            results[name] = items
            
            elapsed = time.time() - endpoint_start
            print(f"        ✅ {len(items):,} Datensätze in {elapsed:.1f}s")
            
        except Exception as e:
            print(f"        ❌ FEHLER: {e}")
            results[name] = []
    
    total_time = time.time() - start_time
    total_records = sum(len(v) for v in results.values())
    
    print(f"\n{'='*60}")
    print(f"✅ Fetch abgeschlossen!")
    print(f"   📊 {total_records:,} Datensätze von {total} Endpunkten")
    print(f"   ⏱️  Gesamtzeit: {total_time:.1f}s")
    print(f"{'='*60}\n")
    
    return results


def save_raw_data(data: dict, output_dir: str = DATA_DIR):
    """Speichert Rohdaten als JSON"""
    raw_dir = Path(output_dir) / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    for name, items in data.items():
        file_path = raw_dir / f"{name}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        print(f"  💾 {name}.json ({len(items):,} Datensätze)")


def main():
    """Hauptfunktion"""
    import argparse
    
    parser = argparse.ArgumentParser(description="BVL API Fetcher für PSM-Desk-DB")
    parser.add_argument("--test", action="store_true", help="Test-Modus (nur 1 Datensatz pro Endpunkt)")
    parser.add_argument("--output", default=DATA_DIR, help="Output-Verzeichnis")
    args = parser.parse_args()
    
    # Fetch alle Daten
    data = fetch_all_endpoints(test_mode=args.test)
    
    # Speichern
    print("💾 Speichere Rohdaten...")
    save_raw_data(data, args.output)
    
    print("\n✅ Fertig!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
