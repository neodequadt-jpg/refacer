# Временный скрипт для замены
import sys

with open('webui.py', 'r') as f:
    content = f.read()

# Замена метода face_swapper.get() на прямой вызов
old = '''    result = ref.face_swapper.get(
        dest_img,
        ref.replacement_faces[0][1],
        ref.replacement_faces[0][0],
        alpha=blend_strength
    )'''

new = '''    result = ref.face_swapper(
        dest_img,
        ref.replacement_faces[0][0],
        ref.replacement_faces[0][1],
        paste_back=True
    )'''

content = content.replace(old, new)

with open('webui.py', 'w') as f:
    f.write(content)

print("✓ webui.py обновлён")
