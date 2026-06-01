from pathlib import Path
import shutil
import re
from datetime import datetime

# =====================================================
# GEEKWAVE NAVBAR PATCHER
# =====================================================
# SOLO MODIFICA:
# - updateFavoritesBadge()
# - renderFavorites()
# - listener favoritesUpdated
#
# NO TOCA:
# - carrito
# - buscador
# - megamenu
# - login
# - filtros
# =====================================================

NAVBAR_FILE = Path("js/navbar-global.js")

if not NAVBAR_FILE.exists():
    print(f"❌ No existe: {NAVBAR_FILE}")
    exit()

# =====================================================
# BACKUP
# =====================================================

backup_name = (
    NAVBAR_FILE.parent
    / f"navbar-global.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}.js"
)

shutil.copy2(NAVBAR_FILE, backup_name)

print("✅ Backup creado:")
print(backup_name)

# =====================================================
# LEER
# =====================================================

content = NAVBAR_FILE.read_text(
    encoding="utf-8",
    errors="ignore"
)

# =====================================================
# EVITAR DUPLICADOS
# =====================================================

if "GEEKWAVE FAVORITES PATCH V2" in content:
    print("⚠️ El parche ya fue aplicado.")
    exit()

# =====================================================
# BUSCAR BLOQUE FAVORITOS
# =====================================================

pattern = re.compile(
    r"// ==========================================\s*"
    r"// FAVORITOS\s*"
    r"// ==========================================.*?"
    r"console\.log\(' Navbar completamente inicializado y listo'\);",
    re.DOTALL
)

replacement = r"""
    // ==========================================
    // FAVORITOS
    // ==========================================
    // GEEKWAVE FAVORITES PATCH V2
    // NO MODIFICAR MANUALMENTE
    // ==========================================

    function getFavorites() {
        try {
            return JSON.parse(
                localStorage.getItem(
                    "geekwave_favorites"
                )
            ) || [];
        } catch {
            return [];
        }
    }

    function updateFavoritesBadge() {

        const favorites = getFavorites();

        const btn =
            document.getElementById(
                "favoritesBtn"
            );

        const badge =
            document.getElementById(
                "favoritesBadge"
            );

        if (!btn || !badge) return;

        badge.textContent =
            favorites.length;

        if (favorites.length > 0) {

            badge.classList.add("show");
            btn.classList.add("has-favorites");

        } else {

            badge.classList.remove("show");
            btn.classList.remove("has-favorites");

        }
    }

    function renderFavorites() {

        const container =
            document.getElementById(
                "favoritesContainer"
            );

        if (!container) return;

        const favorites =
            getFavorites();

        const productos =
            inventario.filter(
                p =>
                    favorites.includes(
                        String(p.id)
                    )
            );

        if (productos.length === 0) {

            container.innerHTML = `
                <div class="favorites-empty">
                    No tienes favoritos aún
                </div>
            `;

            return;
        }

        container.innerHTML =
            productos.map(prod => `
                <a
                    href="info.html?id=${prod.id}"
                    class="favorite-item"
                >
                    <img
                        src="${prod.imagen_principal}"
                        alt="${prod.nombre}"
                    >

                    <div>
                        <h4>${prod.nombre}</h4>
                        <span>$${prod.precio_usd}</span>
                    </div>
                </a>
            `).join("");
    }

    function refreshFavoritesUI() {

        updateFavoritesBadge();

        if (
            inventario &&
            inventario.length
        ) {
            renderFavorites();
        }
    }

    window.removeEventListener(
        "favoritesUpdated",
        refreshFavoritesUI
    );

    window.addEventListener(
        "favoritesUpdated",
        refreshFavoritesUI
    );

    window.addEventListener(
        "storage",
        e => {

            if (
                e.key ===
                "geekwave_favorites"
            ) {
                refreshFavoritesUI();
            }
        }
    );

    setTimeout(
        refreshFavoritesUI,
        500
    );

    updateFavoritesBadge();

    console.log(' Navbar completamente inicializado y listo');
"""

new_content = pattern.sub(
    replacement,
    content
)

if new_content == content:
    print(
        "❌ No encontré la sección FAVORITOS."
    )
    exit()

# =====================================================
# GUARDAR
# =====================================================

NAVBAR_FILE.write_text(
    new_content,
    encoding="utf-8"
)

print(
    "✅ navbar-global.js actualizado."
)

print(
    "✅ Favoritos protegidos."
)

print(
    "✅ Listener duplicado evitado."
)

print(
    "✅ Badge sincronizado."
)

print(
    "✅ Backup creado automáticamente."
)