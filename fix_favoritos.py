import os
import re

# ==========================================
# RUTAS A TUS ARCHIVOS
# ==========================================
NAVBAR_JS = 'js/navbar-global.js'
MAIN_JS = 'js/geekwave-main.js' # Archivo donde cargas los listeners
CSS_FILE = 'css/styles.css'     # Archivo donde están los estilos del panel

def aplicar_parche(ruta, patron_busqueda, reemplazo, usar_regex=False):
    if not os.path.exists(ruta):
        print(f"⚠️ No encontrado: {ruta}")
        return
        
    with open(ruta, 'r', encoding='utf-8') as f:
        contenido = f.read()
        
    if usar_regex:
        nuevo_contenido = re.sub(patron_busqueda, reemplazo, contenido, flags=re.DOTALL)
    else:
        nuevo_contenido = contenido.replace(patron_busqueda, reemplazo)
        
    if contenido != nuevo_contenido:
        # IMPORTANTE: Se sobrescribe el archivo SIN CREAR BACKUPS (Regla #2)
        with open(ruta, 'w', encoding='utf-8') as f:
            f.write(nuevo_contenido)
        print(f"✅ Parche aplicado con éxito en: {ruta}")
    else:
        print(f"ℹ️ Sin cambios en {ruta}. El patrón no coincidió o ya estaba corregido.")

def ejecutar_correcciones():
    print("🚀 Iniciando parcheo quirúrgico de favoritos para GeekWave...\n")

    # ---------------------------------------------------------
    # CORRECCIÓN 1: NAVBAR-GLOBAL.JS (Contador y Multi-pestaña)
    # Se reemplaza la lectura de estado en caché por una fresca del localStorage
    # y se añade el evento 'storage' para que se actualice sin presionar F5.
    # ---------------------------------------------------------
    navbar_regex = r"(document\.addEventListener\('favoritesUpdated',\s*(?:async\s*)?(?:function|\(\))\s*(?:\([^)]*\))?\s*=>?\s*\{)(.*?)(}\);?)"
    
    navbar_fix = r"""\1
    // [FIX] LECTURA FRESCA DIRECTA
    const favs = JSON.parse(localStorage.getItem('geekwave_favorites')) || [];
    const favBadge = document.querySelector('.favorite-counter-class'); // <-- Asegúrate de que el selector sea el de tu badge
    if (favBadge) {
        favBadge.textContent = favs.length;
        // Opcional: mostrar/ocultar el badge si length es 0
    }
\3

// [FIX] SINCRONIZACIÓN MULTI-PESTAÑA (Evita requerir F5)
window.addEventListener('storage', function(e) {
    if (e.key === 'geekwave_favorites') {
        document.dispatchEvent(new CustomEvent('favoritesUpdated'));
    }
});"""
    
    aplicar_parche(NAVBAR_JS, navbar_regex, navbar_fix, usar_regex=True)

    # ---------------------------------------------------------
    # CORRECCIÓN 2: GEEKWAVE-MAIN.JS (Delegación de Eventos)
    # Reemplaza los listeners directos que se pierden cuando el panel 
    # de favoritos se re-renderiza, delegando el clic al body/panel global.
    # ---------------------------------------------------------
    # Buscamos donde asignabas originalmente el listener de '.favorite-btn'
    panel_regex = r"(document\.querySelectorAll\('\.favorite-btn'\)\.forEach[^\n]+)(\n\s*.*addEventListener.*?\n)(.*?)(}\);?)"
    
    panel_fix = r"""// [FIX] DELEGACIÓN DE EVENTOS: Ahora funciona en botones inyectados dinámicamente
document.body.addEventListener('click', function(e) {
    const btn = e.target.closest('.favorite-btn');
    if (!btn) return;
    
    // Mismo código que ya tenías, pero ejecutado de forma delegada
    const productId = btn.dataset.id || btn.getAttribute('id'); 
    let favs = JSON.parse(localStorage.getItem('geekwave_favorites')) || [];
    
    if (favs.includes(productId)) {
        favs = favs.filter(id => id !== productId);
        btn.classList.remove('is-active'); // Asegura que esta clase es la que usas
    } else {
        favs.push(productId);
        btn.classList.add('is-active');
    }
    
    localStorage.setItem('geekwave_favorites', JSON.stringify(favs));
    document.dispatchEvent(new CustomEvent('favoritesUpdated'));
});"""

    aplicar_parche(MAIN_JS, panel_regex, panel_fix, usar_regex=True)

    # ---------------------------------------------------------
    # CORRECCIÓN 3: STYLES.CSS (Maquetación)
    # Soluciona los problemas de espaciado/desbordamiento del panel
    # ---------------------------------------------------------
    # Suponiendo que el contenedor se llama .favorites-panel
    css_old = ".favorites-panel {"
    css_new = """.favorites-panel {
    /* [FIX] Control de scroll y maquetación de los items internos */
    display: flex;
    flex-direction: column;
    max-height: 400px; /* Evita que desborde de la pantalla */
    overflow-y: auto;
    overflow-x: hidden;"""
    
    aplicar_parche(CSS_FILE, css_old, css_new, usar_regex=False)

    print("\n✨ Proceso finalizado. Todo editado in-place respetando tus reglas.")

if __name__ == '__main__':
    ejecutar_correcciones()