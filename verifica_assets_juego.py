import os

# Asume que estás en la raíz del proyecto (donde está tu README y netlify.toml)
base_path = os.path.join("Game", "keepYourSheep", "build")

ASSETS = [
    # Maps
    os.path.join(base_path, "assets", "maps", "map.json"),
    # Tilesets, imágenes principales del juego
    os.path.join(base_path, "assets", "images", "medieval_tilesheet.png"),
    os.path.join(base_path, "assets", "images", "portraits.png"),
    os.path.join(base_path, "assets", "images", "sheep_spritesheet.png"),
    os.path.join(base_path, "assets", "images", "rune_sheet.png"),
    os.path.join(base_path, "assets", "images", "rune_sheet.xml"),
    os.path.join(base_path, "assets", "images", "uipack_rpg_sheet.png"),
    os.path.join(base_path, "assets", "images", "uipack_rpg_sheet.xml"),
    os.path.join(base_path, "assets", "images", "forest_background.png"),
    os.path.join(base_path, "assets", "images", "musicOn.png"),
    os.path.join(base_path, "assets", "images", "musicOff.png"),
    os.path.join(base_path, "assets", "images", "clouds.png"),
    os.path.join(base_path, "assets", "images", "boom.png"),
    # Sonidos
    os.path.join(base_path, "assets", "sounds", "Red Carpet Wooden Floor.mp3"),
]
# Bundle principal
BUNDLES = [
    os.path.join(base_path, "dist", "bundle.js"),
    os.path.join(base_path, "dist", "1.bundle.js"),
]

def check_file(path):
    if os.path.isfile(path):
        print(f"✅ OK     {path}")
    else:
        print(f"❌ FALTANTE {path}")

if __name__ == "__main__":
    print("Verificando archivos básicos para el juego Phaser en Netlify...\n")
    for asset in ASSETS+BUNDLES:
        check_file(asset)