from rembg import remove
from PIL import Image

image_base = Image.open(sys.argv[1])  

  
# Store path of the output image in the variable output_path
output_path = sys.argv[1]
  
# Processing the image
input = Image.open(image_base)
  
# Removing the background from the given Image
output = remove(input)
  
#Saving the image in the given path
output.save(output_path)