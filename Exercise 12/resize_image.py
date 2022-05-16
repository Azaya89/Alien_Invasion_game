from PIL import Image

image_file = r"Exercise 13\image\raindrop.bmp"
img = Image.open(image_file)
# get the image's width and height in pixels
width, height = img.size
# get the largest dimension
max_dim = max(img.size)

# resize the image using the largest side as dimension
factor = 0.1
side = int(max_dim*factor)
resized_image = img.resize((side, side), Image.ANTIALIAS)

# save the resized image to a file
# and view it with your favorite image viewer
resized_image_file = "redu_raindrop.bmp"
resized_image.save(resized_image_file)
