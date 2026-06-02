// js/menu-fixes.js
// Script to normalize inventory globals and fix menu links at runtime
// - Ensures window.inventario / window.INVENTARIO / window.inventarioGlobal are synced
// - Rewrites links from producto.html -> info.html inside the mega-menu
// - Removes inline event.preventDefault() that blocks navigation
// - Converts absolute /juego/ -> relative juego/

(function(){
  document.addEventListener('DOMContentLoaded', () => {
    try {
      const data = window.INVENTARIO || window.inventario || window.inventarioGlobal || [];
      // Expose all common globals for compatibility
      window.INVENTARIO = data;
      window.inventario = data;
      window.inventarioGlobal = data;
      console.log('[menu-fixes] Inventario normalized', {
        INVENTARIO: !!window.INVENTARIO,
        inventario: !!window.inventario,
        inventarioGlobal: !!window.inventarioGlobal
      });

      // Fix anchors that point to producto.html -> info.html
      document.querySelectorAll('a[href*="producto.html"]').forEach(a => {
        try {
          const href = a.getAttribute('href');
          a.setAttribute('href', href.replace(/producto\.html/g, 'info.html'));
        } catch (err) { console.error('[menu-fixes] rewrite anchor href error', err); }
      });

      // Fix absolute /juego/ -> relative juego/
      document.querySelectorAll('a[href^="/juego/"]').forEach(a => {
        try {
          const href = a.getAttribute('href');
          // remove leading slash(es)
          a.setAttribute('href', href.replace(/^\/+/, ''));
        } catch (err) { console.error('[menu-fixes] rewrite juego href error', err); }
      });

      const productosMenu = document.getElementById('productosMenu');
      if (productosMenu) {
        // Remove inline onclick that prevents default inside anchors within the menu
        productosMenu.querySelectorAll('a[onclick]').forEach(a => {
          const onclick = a.getAttribute('onclick') || '';
          if (onclick.includes('event.preventDefault')) {
            a.removeAttribute('onclick');
            // ensure the anchor href points to info.html if it referenced producto.html
            const href = a.getAttribute('href') || '';
            if (href.includes('producto.html')) a.setAttribute('href', href.replace(/producto\.html/g, 'info.html'));
          }
        });

        // Delegated click handler: when clicking a .menu-item (or its contents), prefer the anchor href
        productosMenu.addEventListener('click', e => {
          try {
            const item = e.target.closest && e.target.closest('.menu-item');
            if (!item) return;
            // If there's an anchor inside, navigate to its href (with producto->info rewrite)
            const a = item.querySelector('a[href]');
            if (a) {
              e.preventDefault();
              let href = a.getAttribute('href');
              if (!href) return;
              href = href.replace(/producto\.html/g, 'info.html').replace(/^\/+/, '');
              window.location.href = href;
            } else {
              // If no anchor, but li has an inline onclick that sets window.location.href, try to read it
              const onclick = item.getAttribute('onclick') || '';
              const m = onclick.match(/window\.location\.href\s*=\s*['\"]([^'\"]+)['\"]/);
              if (m && m[1]) {
                e.preventDefault();
                let href = m[1].replace(/producto\.html/g, 'info.html').replace(/^\/+/, '');
                window.location.href = href;
              }
            }
          } catch (err) { console.error('[menu-fixes] delegated click handler error', err); }
        });

        console.log('[menu-fixes] productosMenu fixes applied');
      } else {
        console.log('[menu-fixes] productosMenu not found');
      }
    } catch (err) {
      console.error('[menu-fixes] initialization error', err);
    }
  });
})();
