from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import PIL.Image
import cv2
import matplotlib.pyplot as plt
import numpy as np

# Create your models here.
choices = [
    ('live', 'Live'),
    ('deceased',"Deceased")
]
class Coral(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20,choices=choices)
    source = models.TextField() 
    purchaseDate = models.DateField()
    purchaseCost = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='upload/',null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
    
#class User(models.Model):
#    first_name = models.CharField(max_length=100)
#   last_name = models.CharField(max_length=100)
    
class Photos(models.Model):
    coral = models.ForeignKey(Coral, on_delete=models.PROTECT,null=True, blank=True)
    image_date = models.DateField()
    images = models.ImageField(upload_to='upload/',null=True, blank=True)

    def crop_center(pil_img, crop_width, crop_height):
        img_width, img_height = pil_img.size
        return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        pil_img = PIL.Image.open(self.images)
        image = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        hgt, wdt = image.shape[:2]
        start_row, start_col = int(hgt * .05), int(wdt * .05)
        end_row, end_col = int(hgt * .95), int(wdt * .95)
        cropped = image[start_row:end_row , start_col:end_col]
        cropped_final = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
#       import numpy as np
        resized_img = cv2.resize(cropped_final, (500, 400), interpolation = cv2.INTER_LINEAR)
        pil_img_final = PIL.Image.fromarray(resized_img)

        #cv2.imwrite(self.images.path, cropped_final)

        
        pil_img_final.save(self.images.path, quality=100)
        pil_img_final.close()
        self.images.close()

        #super().save(*args, **kwargs)
        #pil_img = Image.open(self.images)
        #img = cv2.imread(pil_img)
        #image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #hgt, wdt = image.shape[:2]
        #start_row, start_col = int(hgt * .15), int(wdt * .15)
        #end_row, end_col = int(hgt * .85), int(wdt * .85)
        #cropped = image[start_row:end_row , start_col:end_col]
        #cropped_final = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
#
        #cv2.imwrite(self.images.path, cropped_final)
        #
#
        #self.images.close()


