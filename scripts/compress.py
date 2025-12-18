#!/usr/bin/env python3
"""
BVL Daten Kompressor
====================
Komprimiert transformierte JSON-Daten mit GZIP für effiziente Übertragung.
"""

import gzip
import json
import os
import sys
from pathlib import Path

from config import DATA_DIR


def compress_file(input_path: Path, output_path: Path) -> tuple:
    """
    Komprimiert eine JSON-Datei mit GZIP.
    
    Returns:
        (original_size, compressed_size)
    """
    with open(input_path, "rb") as f:
        data = f.read()
    
    original_size = len(data)
    
    with gzip.open(output_path, "wb", compresslevel=9) as f:
        f.write(data)
    
    compressed_size = output_path.stat().st_size
    
    return original_size, compressed_size


def compress_all(input_dir: str = DATA_DIR, output_dir: str = DATA_DIR) -> dict:
    """
    Komprimiert alle transformierten JSON-Dateien.
    
    Returns:
        Dictionary mit Statistiken pro Datei
    """
    transformed_dir = Path(input_dir) / "transformed"
    compressed_dir = Path(output_dir) / "compressed"
    compressed_dir.mkdir(parents=True, exist_ok=True)
    
    stats = {}
    total_original = 0
    total_compressed = 0
    
    print("\n🗜️ Komprimiere Daten...")
    print("-" * 60)
    
    json_files = sorted(transformed_dir.glob("*.json"))
    
    if not json_files:
        print("❌ Keine JSON-Dateien in transformed/ gefunden!")
        return stats
    
    for json_path in json_files:
        name = json_path.stem
        gz_path = compressed_dir / f"{name}.json.gz"
        
        original_size, compressed_size = compress_file(json_path, gz_path)
        
        ratio = (1 - compressed_size / original_size) * 100 if original_size > 0 else 0
        
        stats[f"{name}.json.gz"] = {
            "original_kb": round(original_size / 1024, 2),
            "compressed_kb": round(compressed_size / 1024, 2),
            "ratio": round(ratio, 1)
        }
        
        total_original += original_size
        total_compressed += compressed_size
        
        print(f"  {name:30} {original_size/1024:8.1f} KB → {compressed_size/1024:8.1f} KB ({ratio:5.1f}%)")
    
    print("-" * 60)
    total_ratio = (1 - total_compressed / total_original) * 100 if total_original > 0 else 0
    print(f"  {'GESAMT':30} {total_original/1024:8.1f} KB → {total_compressed/1024:8.1f} KB ({total_ratio:5.1f}%)")
    
    stats["_total"] = {
        "original_kb": round(total_original / 1024, 2),
        "compressed_kb": round(total_compressed / 1024, 2),
        "ratio": round(total_ratio, 1),
        "file_count": len(json_files)
    }
    
    return stats


def main():
    """Hauptfunktion"""
    stats = compress_all()
    
    if not stats:
        return 1
    
    total = stats.get("_total", {})
    print(f"\n✅ {total.get('file_count', 0)} Dateien komprimiert")
    print(f"   Gesamt-Komprimierung: {total.get('ratio', 0):.1f}%")
    print(f"   Von {total.get('original_kb', 0):.1f} KB auf {total.get('compressed_kb', 0):.1f} KB")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
