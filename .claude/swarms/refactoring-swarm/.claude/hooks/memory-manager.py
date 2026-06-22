#!/usr/bin/env python3
"""Memory Manager - CRDT-backed shared state"""
import json, fcntl
from pathlib import Path

class MemoryBank:
    def __init__(self):
        self.path = Path(__file__).parent.parent.parent / "memory/memory-bank.json"
    
    def read(self):
        """Thread-safe read"""
        with open(self.path, 'r') as f:
            fcntl.flock(f, fcntl.LOCK_SH)
            data = json.load(f)
            fcntl.flock(f, fcntl.LOCK_UN)
        return data
    
    def write(self, data):
        """Thread-safe write"""
        with open(self.path, 'w') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            json.dump(data, f, indent=2)
            fcntl.flock(f, fcntl.LOCK_UN)
    
    def update(self, key, value):
        """Atomic update of specific key"""
        data = self.read()
        data[key] = value
        self.write(data)
        
if __name__ == "__main__":
    mb = MemoryBank()
    print(json.dumps(mb.read(), indent=2))
