from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .models import RentSpace, User  # ✅ NO INQUIRY
import cloudinary.uploader
User = get_user_model()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(
                request=self.context.get('request'), 
                username=email,  # ✅ Django uses username field
                password=password
            )
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include email and password')
        return attrs

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username','email','password','is_seller']
        extra_kwargs = {'password': {'write_only': True}}
    def create(self,validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_seller=validated_data.get('is_seller', False)
        )
        return user

class RentSpaceSerializer(serializers.ModelSerializer):
    owner_user_id = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    owner_email = serializers.SerializerMethodField()
    image_file = serializers.ImageField(write_only=True, required=False)
    image = serializers.ImageField(read_only=True)
    
    class Meta:
        model = RentSpace
        fields = [
            'id', 'owner_user_id', 'owner', 'space_type', 'rent', 'deposit', 
            'is_occupied', 'street_address', 'district', 'state', 'country', 
            'image', 'image_file', 'owner_email'
        ]
        read_only_fields = ['owner_user_id', 'owner', 'image_url' , 'image']
    def get_owner_user_id(self, obj):
        return obj.owner.id if obj.owner else None
    def get_owner(self, obj):
        return obj.owner.username if obj.owner else "Unknown"
    
    def get_owner_email(self, obj):
        return obj.owner.email if obj.owner and obj.owner.email else "No email"
    
    def create(self, validated_data):
        image_file = validated_data.pop('image_file', None)
        
        if image_file:
            validated_data['image'] = image_file
            
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Do the same for updates
        image_file = validated_data.pop('image_file', None)
        
        if image_file:
            instance.image = image_file
        return super().update(instance, validated_data)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_seller', 'is_staff', 'is_superuser'] 
        read_only_fields = fields
