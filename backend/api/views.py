

from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from .models import RentSpace, User
from .serializers import LoginSerializer,UserRegistrationSerializer, RentSpaceSerializer, UserProfileSerializer

User = get_user_model()

# ✅ FIXED: JWT + Token support
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token

# class LoginView(generics.GenericAPIView):
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
        
#         # Clear admin session
#         if 'sessionid' in request.COOKIES:
#             request.session.flush()
        
#         refresh = RefreshToken.for_user(user)
#         return Response({
#             'access': str(refresh.access_token),
#             'refresh': str(refresh),
#             'is_admin': user.is_superuser,
#             'is_seller': getattr(user, 'is_seller', False)
#         })


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer  # ✅ ADD THIS LINE
    permission_classes = [AllowAny]     # ✅ ADD THIS LINE
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'is_admin': user.is_superuser,
            'is_seller': getattr(user, 'is_seller', False)
        })



class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

class RentSpaceViewSet(viewsets.ModelViewSet):
    queryset = RentSpace.objects.all()
    serializer_class = RentSpaceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return RentSpace.objects.all()           # ✅ Admin: ALL spaces
        if hasattr(user, 'is_seller') and user.is_seller:
            return RentSpace.objects.filter(owner=user)  # ✅ Seller: OWN spaces only
        return RentSpace.objects.all()    

    def perform_create(self, serializer):
        if not self.request.user.is_seller:
            raise PermissionDenied("Only sellers can create rent spaces.")
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        if self.request.user.is_staff:
            instance.delete()
            return
        if instance.owner != self.request.user:
            raise PermissionDenied("Only admins/sellers can delete own spaces")
        instance.delete()

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

class AdminSpacesViewSet(viewsets.ModelViewSet):
    queryset = RentSpace.objects.all()
    serializer_class = RentSpaceSerializer
    permission_classes = [IsAdminUser]

# ✅ FIXED: Email (your code perfect)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_inquiry_email(request):
    try:
        data = request.data
        print("📧 Request data:", data)
        
        rent_space_id = data.get('rent_space_id')
        space_type = data.get('space_type', 'Unknown Space')
        seller_id = data.get('seller_id')
        consumer_name = data.get('consumer_name', 'Anonymous')
        consumer_email = data.get('consumer_email', 'no-email@example.com')
        message = data.get('message', '')

        seller = User.objects.get(id=seller_id)
        
        subject = f"New Inquiry: {space_type} - {consumer_name}"
        email_body = f"""
Hi {seller.username},

{consumer_name} ({consumer_email}) is interested in your {space_type}!

Message: {message}

Reply directly to {consumer_email}
Best regards,
Rental Platform Team
        """
        
        send_mail(
            subject=subject,
            message=email_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[seller.email],
            fail_silently=False,
        )
        
        return Response({"message": "✅ Email sent successfully!"}, status=200)
        
    except User.DoesNotExist:
        return Response({"error": "Seller not found"}, status=404)
    except Exception as e:
        print(f"❌ Email error: {str(e)}")
        return Response({"error": f"Server error: {str(e)}"}, status=500)

# ✅ Admin APIs (fixed duplicates)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_users(request):
    users = User.objects.all().values('id', 'username', 'email', 'is_seller', 'is_active', 'is_staff')
    return Response(list(users))

@api_view(['POST'])
@permission_classes([IsAdminUser])
def make_seller(request):
    user_ids = request.data.get('user_ids', [])
    updated = User.objects.filter(id__in=user_ids).update(is_seller=True)
    return Response({"message": f"{updated} users made sellers"})

@api_view(['POST'])
@permission_classes([IsAdminUser])
def make_consumer(request):
    user_ids = request.data.get('user_ids', [])
    updated = User.objects.filter(id__in=user_ids).update(is_seller=False)
    return Response({"message": f"{updated} users made consumers"})

@api_view(['POST'])
@permission_classes([IsAdminUser])
def activate_users(request):
    user_ids = request.data.get('user_ids', [])
    updated = User.objects.filter(id__in=user_ids).update(is_active=True)
    return Response({"message": f"{updated} users activated"})

@api_view(['POST'])
@permission_classes([IsAdminUser])
def deactivate_users(request):
    user_ids = request.data.get('user_ids', [])
    updated = User.objects.filter(id__in=user_ids).update(is_active=False)
    return Response({"message": f"{updated} users deactivated"})

# @api_view(['GET'])
# @permission_classes([IsAdminUser])
# def admin_spaces(request):
#     spaces = RentSpace.objects.select_related('owner').values(
#         'id', 'space_type', 'image', 'image_file', 'rent', 'deposit', 
#         'is_occupied', 'district', 'state', 'owner_id', 'owner__username', 'owner__email'
#     )
#     return Response(list(spaces))

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_spaces(request):
    try:
        spaces = RentSpace.objects.select_related('owner').all()
        serializer = RentSpaceSerializer(spaces, many=True)       # ✅ Use serializer!
        return Response(serializer.data)
        # spaces = RentSpace.objects.select_related('owner').values(
        #     'id', 'space_type', 'image', 'rent', 'deposit',
        #     'is_occupied', 'district', 'state', 
        #     'owner_id', 
        #     'owner__username',      # ✅ Frontend expects this
        #     'owner__email'          # ✅ Frontend expects this
        # )
        # return Response(list(spaces))
    except Exception as e:
        print(f"❌ Admin spaces error: {e}")  # DEBUG
        return Response({"error": str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def mark_occupied(request):
    space_ids = request.data.get('space_ids', [])
    updated = RentSpace.objects.filter(id__in=space_ids).update(is_occupied=True)
    return Response({"message": f"{updated} spaces marked occupied"})

@api_view(['POST'])
@permission_classes([IsAdminUser])
def mark_vacant(request):
    space_ids = request.data.get('space_ids', [])
    updated = RentSpace.objects.filter(id__in=space_ids).update(is_occupied=False)
    return Response({"message": f"{updated} spaces marked vacant"})

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_rentspace(request, pk):
    try:
        space = RentSpace.objects.get(pk=pk)
        space.delete()
        return Response({"message": "Space deleted successfully"})
    except RentSpace.DoesNotExist:
        return Response({"error": "Space not found"}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user_data = {
        'id': request.user.id,
        'username': request.user.username,
        'email': request.user.email,
        'is_staff': request.user.is_staff,
        'is_seller': getattr(request.user, 'is_seller', False),
        'is_active': request.user.is_active,
    }
    return Response(user_data)
