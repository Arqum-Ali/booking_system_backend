# serializers.py
from rest_framework import serializers
from .models import Listing, Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'  # This includes all fields in the Address model

class ListingCreateSerializer(serializers.ModelSerializer):
    address = serializers.CharField(write_only=True)  # Full address from frontend
    city = serializers.CharField(write_only=True)     # City from frontend
    state = serializers.CharField(write_only=True)    # State from frontend
    address_details = AddressSerializer(source='address_id', read_only=True)  # Address details in the response

    class Meta:
        model = Listing
        fields = [
            'property_type',
            'room_type',
            'bedrooms',
            'beds',
            'bathrooms',
            'address',
            'city',
            'state',
            'accommodates',
            'address_details',  # Add address details to the response
        ]

    def create(self, validated_data):
        # Extract address, city, and state from the validated data
        address_input = validated_data.pop('address')
        city_input = validated_data.pop('city')
        state_input = validated_data.pop('state')

        # Create the Address object
        address_obj = Address.objects.create(
            address=address_input,
            city=city_input,
            state=state_input
        )

        # Assign the address object to the listing and create the listing
        listing = Listing.objects.create(address_id=address_obj, **validated_data)
        return listing

    # Optionally override to_representation if you want to customize the output further
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # You can customize what else you want to include in the response
        return representation









from rest_framework import serializers
from .models import Listing, Amenity, Image

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['id', 'name', 'icon_url']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'imageable_id', 'imageable_type', 'image_url', 'caption', 'is_primary']

class ListingSerializer(serializers.ModelSerializer):
    amenities = AmenitySerializer(many=True)  # Handles a list of amenities
    images = ImageSerializer(many=True, required=False)  # Allows multiple images

    class Meta:
        model = Listing
        fields = ['id', 'title', 'description', 'amenities', 'images']

    def create(self, validated_data):
        # Extract amenities and images data from the input
        amenities_data = validated_data.pop('amenities', [])
        images_data = validated_data.pop('images', [])
        
        # Create the listing
        listing = Listing.objects.create(**validated_data)

        # Handle amenities
        for amenity_data in amenities_data:
            amenity, _ = Amenity.objects.get_or_create(**amenity_data)
            listing.amenities.add(amenity)

        # Handle images
        for image_data in images_data:
            # Remove 'imageable_id' and 'imageable_type' from image_data if they exist
            image_data.pop('imageable_id', None)
            image_data.pop('imageable_type', None)
            
            # Create the Image object using the listing's id
            Image.objects.create(imageable_id=listing.id, imageable_type='listing', **image_data)
    
        return listing

    def update(self, instance, validated_data):
        amenities_data = validated_data.pop('amenities', [])
        images_data = validated_data.pop('images', [])
        
        # Update the title and description
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        # Update amenities
        if amenities_data:
            instance.amenities.clear()  # Remove existing amenities
            for amenity_data in amenities_data:
                amenity, _ = Amenity.objects.get_or_create(**amenity_data)
                instance.amenities.add(amenity)

        # Update images (for simplicity, this example assumes all new images replace existing ones)
        if images_data:
            Image.objects.filter(imageable_id=instance.id, imageable_type='listing').delete()  # Clear existing images
            for image_data in images_data:
                Image.objects.create(imageable_id=instance.id, imageable_type='listing', **image_data)
        
        return instance
