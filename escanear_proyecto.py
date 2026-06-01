import os
import json

def escanear_proyecto():
    datos = {
        "archivos_html": [],
        "estructura_js": {},
        "inventario_encontrado": None
    }
    
    # 1. Buscar archivos HTML importantes
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".html"):
                datos["archivos_html"].append(os.path.join(root, file))
            # 2. Leer el inventario si existe
            if file == "inventario.json":
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    datos["inventario_encontrado"] = json.load(f)

    # 3. Leer los JS clave para entender cómo manejan el estado
    archivos_js = ['js/info.js', 'js/productos.js', 'js/state.js']
    for js_path in archivos_js:
        if os.path.exists(js_path):
            with open(js_path, 'r', encoding='utf-8') as f:
                datos["estructura_js"][js_path] = f.read()

    # Guardar resultados
    with open("resultado_escaneo.json", "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4)
    
    print("Escaneo completado. Se ha generado 'resultado_escaneo.json'.")

if __name__ == "__main__":
    escanear_proyecto()