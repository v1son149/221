import os
import json
import urllib.parse

valid_extensions = ('.jpg', '.jpeg', '.png', '.webp', '.JPG', '.JPEG', '.PNG', '.HEIC', '.heic', '.GIF', '.gif')

res = {}

for root, dirs, files in os.walk('.'):
    if '.git' in root or '__pycache__' in root or root == '.':
        continue
        
    folder_name = os.path.basename(root)
    folder_lower = folder_name.lower().strip()
    
    # Пропускаем неиспользуемые альбомы
    if folder_lower in ['one year', '1 year']:
        continue
        
    # Объединяем ВСЕ old photos (old photos, old photos2, old photos 3 и т.д.) в один альбом
    if folder_lower.startswith('old photo'):
        album_key = 'old photos'
    # Объединяем нервы и нервы 2 в один общий альбом
    elif 'nervy' in folder_lower or 'нерв' in folder_lower:
        album_key = 'nervy'
    elif 'hallow' in folder_lower:
        album_key = 'hallowen'
    else:
        album_key = folder_name
        
    images = []
    for file in files:
        if file.endswith(valid_extensions):
            file_path = os.path.join(root, file).replace('./', '')
            encoded_path = urllib.parse.quote(file_path)
            if album_key not in res or encoded_path not in res[album_key]:
                images.append(encoded_path)
                
    if images:
        if album_key not in res:
            res[album_key] = []
        res[album_key].extend(images)

print("✨ Актуальные альбомы и количество фото:")
for k, v in res.items():
    print(f"📁 Альбом '{k}': {len(v)} фото")

# Записываем результат в photos.js
with open("photos.js", "w", encoding="utf-8") as file:
    file.write("window.ALBUM_PHOTOS = " + json.dumps(res, ensure_ascii=False, indent=2))