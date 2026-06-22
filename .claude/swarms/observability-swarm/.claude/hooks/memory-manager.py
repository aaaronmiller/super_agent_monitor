#!/usr/bin/env python3
import json
import fcntl

class MemoryBank:
    def __init__(self, path):
        self.path = path

    def read(self):
        with open(self.path, 'r') as f:
            fcntl.flock(f, fcntl.LOCK_SH)
            data = json.load(f)
            fcntl.flock(f, fcntl.LOCK_UN)
        return data

    def write(self, data):
        with open(self.path, 'w') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            json.dump(data, f, indent=2)
            fcntl.flock(f, fcntl.LOCK_UN)
