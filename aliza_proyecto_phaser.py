import os
import re
import json

def buscar_div_content_html(raiz):
    print("🔎 Buscando <div id=\"content\"> en archivos index.html:")
    encontrados = 0
    for root, dirs, files in os.walk(raiz):
        for f in files:
            if f.lower() == "index.html":
                path = os.path.join(root, f)
                with open(path, encoding="utf-8") as htmlfile:
                    contenido = htmlfile.read()
                    if '<div id="content">' in contenido or "<div id='content'>" in contenido:
                        print(f"✅ OK en: {path}")
                        encontrados += 1
                    else:
                        print(f"❌ FALTANTE en: {path}")
    if encontrados == 0:
        print("⚠️ No se encontró ningún <div id=\"content\"> en los index.html")
    print()

def buscar_nombre_tileset_json(json_path):
    print(f"🔎 Buscando nombre de tileset en {json_path}:")
    if not os.path.isfile(json_path):
        print(f"❌ No existe {json_path}")
        return None
    with open(json_path, encoding="utf-8") as f:
        try:
            data = json.load(f)
            nombre = data["tilesets"][0]["name"]
            print(f"✅ tileset: {nombre}")
            return nombre
        except Exception as e:
            print(f"❌ Error leyendo tileset del JSON: {e}")
            return None

def buscar_preload_phaser(raiz, tileset_expected):
    # Busca preload de imágenes y carga de tilemap en JS y verifica clave y ruta
    pattern_load = re.compile(r"this\.load\.image\(['\"](?P<key>[^'\"]+)['\"]\s*,\s*['\"](?P<ruta>[^'\"]+)['\"]\)")
    encontrados = []
    for root, dirs, files in os.walk(raiz):
        for f in files:
            if f.endswith('.js'):
                p = os.path.join(root, f)
                with open(p, encoding="utf-8") as source:
                    s = source.read()
                    for match in pattern_load.finditer(s):
                        key, ruta = match.group('key'), match.group('ruta')
                        if tileset_expected and tileset_expected in key:
                            print(f"✅ Se carga tileset '{key}' con ruta: {ruta} en {p}")
                        encontrados.append((key, ruta, p))
    print()
    return encontrados

def buscar_parent_config(raiz):
    print("🔎 Buscando 'parent' en config Phaser:")
    pattern = re.compile(r"parent\s*:\s*['\"]content['\"]")
    encontrados = 0
    for root, dirs, files in os.walk(raiz):
        for f in files:
            if f.endswith('.js'):
                p = os.path.join(root, f)
                with open(p, encoding="utf-8") as s:
                    src = s.read()
                    if pattern.search(src):
                        print(f"✅ parent: 'content' encontrado en {p}")
                        encontrados += 1
    if encontrados == 0:
        print("❌ No se encontró parent: 'content' en tu código Phaser.")
    print()

def buscar_service_worker(raiz):
    print("🔎 Buscando registro de Service Worker:")
    pattern = r"serviceWorker\.register\(['\"](.*?)['\"]\)"
    for root, dirs, files in os.walk(raiz):
        for f in files:
            if f.endswith('.js'):
                p = os.path.join(root, f)
                with open(p, encoding="utf-8") as s:
                    src = s.read()
                    for m in re.findall(pattern, src):
                        print(f"SW registrado en {p}: {m}")
                        if m.startswith("/service-worker"):
                            print("⚠️  ¡Cámbialo por '/juego/service-worker.js'!")
    print()

if __name__ == "__main__":
    BASE = os.getcwd()
    # 1. Busca el div content en los index.html
    buscar_div_content_html(BASE)
    # 2. Lee el tileset del map.json (ajusta la ruta si no coincide)
    map_json = os.path.join("Game", "keepYourSheep", "build", "assets", "maps", "map.json")
    tileset = buscar_nombre_tileset_json(map_json)
    # 3. Busca en preload Phaser que uses el tileset de ese nombre
    buscar_preload_phaser(BASE, tileset)
    # 4. Busca parent: 'content'
    buscar_parent_config(BASE)
    # 5. Busca uso de SW
    buscar_service_worker(BASE)