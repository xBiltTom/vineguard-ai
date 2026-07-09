"""
Script de Preprocesamiento y Limpieza de Datos para VineGuard AI.

Este script agarra un dataset crudo (como el descargado de Kaggle), 
y aplica el pipeline de limpieza descrito en el Dashboard:
1. Elimina imágenes corruptas o de 0 KB.
2. Identifica y elimina duplicados usando un hash criptográfico simple (MD5).
3. Redimensiona las imágenes válidas a 224x224 (estándar para CNNs).
4. Exporta los resultados limpios a una nueva carpeta de forma segura.

Uso:
    python scripts/prepare_dataset.py --input dataset/ --output dataset_cleaned/
"""

import os
import hashlib
import argparse
from pathlib import Path
from PIL import Image
from tqdm import tqdm

def get_image_hash(image_path):
    """Calcula el hash MD5 de un archivo para detectar duplicados exactos."""
    hash_md5 = hashlib.md5()
    with open(image_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def clean_and_prepare_dataset(input_dir, output_dir, target_size=(224, 224)):
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    if not input_path.exists():
        print(f"❌ Error: El directorio de entrada '{input_dir}' no existe.")
        return

    # Crear directorio de salida si no existe
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"🚀 Iniciando Pipeline de Limpieza en: {input_dir}")
    print(f"📁 Directorio de salida: {output_dir}")
    
    stats = {
        "procesadas": 0,
        "corruptas": 0,
        "duplicadas": 0,
        "exportadas": 0
    }
    
    # Set para llevar registro de hashes y evitar duplicados globales o por clase
    seen_hashes = set()
    
    # Recorrer subcarpetas (Clases)
    classes = [d for d in os.listdir(input_path) if os.path.isdir(input_path / d)]
    
    if not classes:
        print("⚠️ No se encontraron subcarpetas (clases) en el directorio de entrada.")
        return

    for class_name in classes:
        print(f"\n🔍 Procesando clase: {class_name}")
        class_input_dir = input_path / class_name
        class_output_dir = output_path / class_name
        
        # Crear la subcarpeta de la clase en el destino
        class_output_dir.mkdir(parents=True, exist_ok=True)
        
        images = [f for f in os.listdir(class_input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
        
        for img_name in tqdm(images, desc=f"Limpiando {class_name}", unit="img"):
            stats["procesadas"] += 1
            img_path = class_input_dir / img_name
            
            # 1. Filtro de integridad: Peso 0 KB
            if os.path.getsize(img_path) == 0:
                stats["corruptas"] += 1
                continue
                
            # 2. Filtro de duplicados (Hash MD5)
            img_hash = get_image_hash(img_path)
            if img_hash in seen_hashes:
                stats["duplicadas"] += 1
                continue
                
            # 3. Filtro de Calidad Visual y Formato (Intentar abrir con PIL)
            try:
                with Image.open(img_path) as img:
                    img.verify() # Verifica si está corrupta sin cargarla toda en RAM
            except Exception:
                stats["corruptas"] += 1
                continue
                
            # 4. Normalización Geométrica (Resize) y Exportación Segura
            try:
                # Volvemos a abrir porque verify() cierra el archivo lógicamente
                with Image.open(img_path) as img:
                    # Convertir a RGB por si hay imágenes RGBA (con transparencia) o Escala de Grises
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # Redimensionar al estándar 224x224
                    img_resized = img.resize(target_size, Image.Resampling.LANCZOS)
                    
                    # Guardar en el directorio limpio como JPG
                    new_name = f"{img_hash[:8]}_{img_name}" # Evita colisión de nombres
                    # Forzamos .jpg
                    if not new_name.lower().endswith('.jpg'):
                        new_name = new_name.rsplit('.', 1)[0] + '.jpg'
                        
                    export_path = class_output_dir / new_name
                    img_resized.save(export_path, 'JPEG', quality=95)
                    
                    seen_hashes.add(img_hash)
                    stats["exportadas"] += 1
                    
            except Exception as e:
                # Captura imágenes que pasaron verify() pero fallan al procesar píxeles (ej. truncation)
                stats["corruptas"] += 1
                continue

    # Resumen Ejecutivo
    print("\n" + "="*40)
    print("🎯 REPORTE FINAL DE LIMPIEZA DE DATOS")
    print("="*40)
    print(f"Total imágenes analizadas : {stats['procesadas']}")
    print(f"❌ Corruptas / Ilegibles   : {stats['corruptas']}")
    print(f"🗑️ Duplicadas eliminadas   : {stats['duplicadas']}")
    print(f"✅ Exportadas con éxito    : {stats['exportadas']}")
    print("="*40)
    print(f"Las imágenes redimensionadas a {target_size} están listas en: {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script de Limpieza y Preprocesamiento de Imágenes")
    parser.add_argument("--input", type=str, default="dataset", help="Ruta de la carpeta del dataset crudo.")
    parser.add_argument("--output", type=str, default="dataset_cleaned", help="Ruta donde se guardará el dataset limpio.")
    parser.add_argument("--size", type=int, default=224, help="Resolución final (ej. 224 para MobileNet).")
    
    args = parser.parse_args()
    
    clean_and_prepare_dataset(args.input, args.output, target_size=(args.size, args.size))
