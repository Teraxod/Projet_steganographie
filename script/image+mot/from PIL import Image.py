from PIL import Image
img = Image.open("image_secrete.png")
print(img.info.get("message_secret"))
