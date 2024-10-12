from django.contrib import admin
from .models import Listing, Image, Amenity


# Register the models with the admin site
admin.site.register(Listing )
admin.site.register(Image)  # You can choose to register or not depending on your needs
admin.site.register(Amenity)
