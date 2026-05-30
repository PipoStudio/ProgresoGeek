import requests

BASE_PATH = "/juego"

CHECKS = [
    "/assets/maps/map.json",
    "/assets/images/medieval_tilesheet.png",
    "/assets/images/portraits.png",
    "/assets/images/sheep_spritesheet.png",
    "/assets/images/rune_sheet.png",
    "/assets/images/rune_sheet.xml",
    "/assets/images/uipack_rpg_sheet.png",
    "/assets/images/uipack_rpg_sheet.xml",
    "/assets/images/forest_background.png",
    "/assets/images/musicOn.png",
    "/assets/images/musicOff.png",
    "/assets/images/clouds.png",
    "/assets/images/boom.png",
    "/assets/sounds/Red Carpet Wooden Floor.mp3",
    "/dist/bundle.js",
    "/dist/1.bundle.js",
]

def url_join(root, path):
    return root.rstrip("/") + BASE_PATH + path

if __name__ == "__main__":
    root_url = input("Escribe la URL base de tu Netlify (ej: https://miproyecto.netlify.app): ").strip()
    print("\nProbando acceso web a recursos críticos...\n")
    for rela in CHECKS:
        url = url_join(root_url, rela)
        try:
            r = requests.head(url, allow_redirects=True)
            if r.status_code == 200:
                print(f"✅ OK     {url}")
            else:
                print(f"❌ ERROR {r.status_code} {url}")
        except Exception as e:
            print(f"❌ ERR   {url}    {e}")