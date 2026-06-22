#!/usr/bin/env python3
"""Duplicate Code Detection"""
import sys
from pathlib import Path
from difflib import SequenceMatcher

def find_duplicates(files, min_lines=6):
    """Find duplicate code blocks"""
    duplicates = []
    for i, f1 in enumerate(files):
        lines1 = Path(f1).read_text().splitlines()
        for f2 in files[i+1:]:
            lines2 = Path(f2).read_text().splitlines()
            matcher = SequenceMatcher(None, lines1, lines2)
            for match in matcher.get_matching_blocks():
                if match.size >= min_lines:
                    duplicates.append({
                        "file1": f1,
                        "file2": f2,
                        "lines": match.size
                    })
    return duplicates

if __name__ == "__main__":
    print(find_duplicates(sys.argv[1:]))
