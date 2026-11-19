from PIL import Image, ImageDraw

taille = 256
img = Image.new("RGBA", (taille, taille), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Fond carré aux coins arrondis (Bleu moderne)
draw.rounded_rectangle([(10, 10), (246, 246)], radius=50, fill="#3b82f6")

# Deux flèches de conversion stylisées (Blanc et Vert émeraude)
draw.polygon([(65, 95), (155, 95), (155, 70), (200, 110), (155, 150), (155, 125), (65, 125)], fill="#ffffff")
draw.polygon([(191, 161), (101, 161), (101, 186), (56, 146), (101, 106), (101, 131), (191, 131)], fill="#10b981")

img.save("assets/icon.ico", format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
print("Icône créée dans assets/icon.ico !")
