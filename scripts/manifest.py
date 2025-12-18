#!/usr/bin/env python3
"""
Manifest Generator
==================
Generiert manifest.json mit Metadaten, Checksummen und Statistiken.
"""

import gzip
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from config import DATA_DIR, get_endpoint_count


def sha256_file(file_path: Path) -> str:
    """Berechnet SHA256-Checksum einer Datei"""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def count_records_in_gz(file_path: Path) -> int:
    """Zählt Datensätze in einer GZIP-JSON-Datei"""
    try:
        with gzip.open(file_path, "rt", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return len(data)
            return 1
    except Exception:
        return 0


def generate_manifest(data_dir: str = DATA_DIR) -> dict:
    """
    Generiert das manifest.json für GitHub Pages.
    
    Returns:
        Manifest-Dictionary
    """
    compressed_dir = Path(data_dir) / "compressed"
    
    if not compressed_dir.exists():
        print("❌ Verzeichnis 'compressed/' nicht gefunden!")
        return {}
    
    now = datetime.now(timezone.utc)
    version = now.strftime("%Y-%m-%d")
    generated = now.isoformat()
    
    files = {}
    total_records = 0
    total_size = 0
    
    print("\n📋 Generiere Manifest...")
    print("-" * 60)
    
    gz_files = sorted(compressed_dir.glob("*.json.gz"))
    
    for gz_path in gz_files:
        filename = gz_path.name
        checksum = sha256_file(gz_path)
        size_bytes = gz_path.stat().st_size
        size_kb = round(size_bytes / 1024, 2)
        count = count_records_in_gz(gz_path)
        
        files[filename] = {
            "count": count,
            "checksum": f"sha256:{checksum}",
            "size_kb": size_kb
        }
        
        total_records += count
        total_size += size_bytes
        
        print(f"  {filename:35} {count:>8,} records  {size_kb:>8.2f} KB")
    
    print("-" * 60)
    print(f"  {'GESAMT':35} {total_records:>8,} records  {total_size/1024:>8.2f} KB")
    
    manifest = {
        "version": version,
        "generated": generated,
        "endpoints": get_endpoint_count(),
        "total_records": total_records,
        "total_size_kb": round(total_size / 1024, 2),
        "files": files
    }
    
    return manifest


def save_manifest(manifest: dict, output_dir: str = DATA_DIR):
    """Speichert manifest.json im data/ Verzeichnis"""
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    manifest_path = out_dir / "manifest.json"
    
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Manifest gespeichert: {manifest_path}")


def copy_compressed_to_data(data_dir: str = DATA_DIR):
    """Kopiert komprimierte Dateien in data/ für GitHub Pages"""
    compressed_dir = Path(data_dir) / "compressed"
    out_dir = Path(data_dir)
    
    print("\n📦 Kopiere Dateien für GitHub Pages...")
    
    for gz_path in compressed_dir.glob("*.json.gz"):
        dest_path = out_dir / gz_path.name
        dest_path.write_bytes(gz_path.read_bytes())
        print(f"  📄 {gz_path.name}")


def main():
    """Hauptfunktion"""
    manifest = generate_manifest()
    
    if not manifest:
        return 1
    
    save_manifest(manifest)
    copy_compressed_to_data()
    
    print(f"\n✅ Manifest generiert!")
    print(f"   Version: {manifest['version']}")
    print(f"   Endpunkte: {manifest['endpoints']}")
    print(f"   Datensätze: {manifest['total_records']:,}")
    print(f"   Größe: {manifest['total_size_kb']:.2f} KB")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
