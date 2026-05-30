import os

# Directorio que contiene los archivos compilados
target_dir = './Game/keepYourSheep/build/'
# La ruta que se antepondrá a los assets
new_path_prefix = '/Game/keepYourSheep/build/'

def fix_paths():
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file.endswith('.js') or file.endswith('.html'):
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Reemplazamos patrones como 'assets/' por '/Game/keepYourSheep/build/assets/'
                # Ajusta esta lógica si tus archivos usan rutas diferentes
                new_content = content.replace('"assets/', f'"{new_path_prefix}assets/')
                new_content = new_content.replace("'assets/", f"'{new_path_prefix}assets/")
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f'Procesado: {file_path}')

if __name__ == '__main__':
    fix_paths()
    print('¡Listo! Rutas de assets corregidas.')