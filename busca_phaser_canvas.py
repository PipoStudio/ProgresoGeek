import os
import re

# Palabras clave a buscar y contexto
targets = [
    r'new\s+Phaser\.Game\s*\(',
    r'parent\s*:\s*[\'\"]content[\'\"]',
    r'\.canvas',
    r'\.resize\(',
    r'window\.addEventListener\s*\(\s*[\'\"]resize[\'\"]',
    r'document\.addEventListener\s*\(\s*[\'\"]DOMContentLoaded[\'\"]'
]

def buscar(raiz):
    print("Buscando fragmentos problemáticos relacionados con Phaser y el canvas...\n")
    for root, dirs, files in os.walk(raiz):
        for f in files:
            if f.endswith('.js'):
                path = os.path.join(root, f)
                try:
                    with open(path, encoding="utf-8") as arch:
                        lines = arch.readlines()
                        for i, line in enumerate(lines):
                            for pat in targets:
                                if re.search(pat, line):
                                    print(f"{path}:{i+1}: {line.strip()}")
                                    # También muestra contexto
                                    cstart = max(0, i-2)
                                    cend = min(len(lines), i+3)
                                    for j in range(cstart, cend):
                                        if j != i:
                                            print(f"    {j+1}: {lines[j].strip()}")
                                    print()
                except Exception as e:
                    print(f"...error leyendo {path}: {e}")

if __name__ == "__main__":
    BASE = os.getcwd()
    buscar(BASE)