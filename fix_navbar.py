from pathlib import Path
import re

archivo = Path("js/navbar-global.js")

if not archivo.exists():
    print("❌ No encontré js/navbar-global.js")
    exit()

contenido = archivo.read_text(encoding="utf-8")

# ====================================================
# ELIMINAR BLOQUE DUPLICADO DE saveCart
# ====================================================

contenido = re.sub(
    r"// En pago\.js.*?window\.addEventListener\('storage'.*?\}\);\s*",
    "",
    contenido,
    flags=re.S
)

# ====================================================
# ELIMINAR FAVORITOS MAL UBICADOS
# ====================================================

contenido = re.sub(
    r"function updateFavoritesBadge\(\).*",
    "",
    contenido,
    flags=re.S
)

# ====================================================
# INSERTAR FAVORITOS DENTRO DE initializeNavbarLogic
# ====================================================

codigo_favoritos = r"""

    // ==========================================
    // FAVORITOS
    // ==========================================

    function updateFavoritesBadge() {

        const favorites =
            JSON.parse(
                localStorage.getItem(
                    "geekwave_favorites"
                )
            ) || [];

        const btn =
            document.getElementById(
                "favoritesBtn"
            );

        const badge =
            document.getElementById(
                "favoritesBadge"
            );

        if (!btn) return;

        if (favorites.length > 0) {

            btn.classList.add(
                "has-favorites"
            );

            if (badge) {

                badge.textContent =
                    favorites.length;

                badge.classList.add(
                    "show"
                );
            }

        } else {

            btn.classList.remove(
                "has-favorites"
            );

            if (badge) {

                badge.classList.remove(
                    "show"
                );
            }
        }
    }

    function renderFavorites() {

        const favoritos =
            JSON.parse(
                localStorage.getItem(
                    "geekwave_favorites"
                )
            ) || [];

        const container =
            document.getElementById(
                "favoritesContainer"
            );

        if (!container) return;

        const productos =
            inventario.filter(
                p =>
                    favoritos.includes(
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
                    >

                    <div>

                        <h4>${prod.nombre}</h4>

                        <span>
                            $${prod.precio_usd}
                        </span>

                    </div>

                </a>

            `).join("");
    }

    window.addEventListener(
        "favoritesUpdated",
        () => {

            updateFavoritesBadge();
            renderFavorites();

        }
    );

    updateFavoritesBadge();

"""

contenido = contenido.replace(
    "console.log(' Navbar completamente inicializado y listo');",
    codigo_favoritos + "\n\n    console.log(' Navbar completamente inicializado y listo');"
)

# ====================================================
# GUARDAR BACKUP
# ====================================================

backup = archivo.with_suffix(".backup.js")
backup.write_text(
    archivo.read_text(encoding="utf-8"),
    encoding="utf-8"
)

archivo.write_text(
    contenido,
    encoding="utf-8"
)

print("✅ navbar-global.js reparado")
print("✅ Backup creado:", backup)