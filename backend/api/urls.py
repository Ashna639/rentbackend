# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import ( RentSpaceViewSet, RegisterView, UserProfileView,delete_rentspace,user_profile, LoginView, send_inquiry_email , admin_users, make_seller, make_consumer, activate_users, deactivate_users,
#     admin_spaces, mark_occupied, mark_vacant, AdminSpacesViewSet)

# router = DefaultRouter()
# router.register(r'rentspace', RentSpaceViewSet)

# urlpatterns = [
#     path('register/', RegisterView.as_view(), name='register'),
#     path('', include(router.urls)),
#     path('user/profile/', UserProfileView.as_view(), name='user-profile'),
#     path('api/login/', LoginView.as_view(), name='login'),
#     path('send-inquiry/', send_inquiry_email, name='send-inquiry-email'),

#     path('admin/users/', admin_users, name='admin_users'),
#     path('admin/users/make-seller/', make_seller, name='make_seller'),
#     path('admin/users/make-consumer/', make_consumer, name='make_consumer'),
#     path('admin/users/activate/', activate_users, name='activate_users'),
#     path('admin/users/deactivate/', deactivate_users, name='deactivate_users'),
#     path('admin/spaces/', admin_spaces, name='admin_spaces'),
#     path('admin/spaces/mark-occupied/', mark_occupied, name='mark_occupied'),
#     path('admin/spaces/mark-vacant/', mark_vacant, name='mark_vacant'),
#     path('profile/', user_profile, name='user_profile'),
    
#     path('api/rentspace/<int:pk>/', delete_rentspace, name='delete_rentspace'),
# ]



from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'rentspace', views.RentSpaceViewSet, basename='rentspace')

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('api/login/', views.LoginView.as_view(), name='login'),
    path('user/profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('send-inquiry/', views.send_inquiry_email, name='send-inquiry'),
    
    # Admin
    path('admin/users/', views.admin_users, name='admin_users'),
    path('admin/users/make-seller/', views.make_seller, name='make_seller'),
    path('admin/users/make-consumer/', views.make_consumer, name='make_consumer'),
    path('admin/users/activate/', views.activate_users, name='activate_users'),
    path('admin/users/deactivate/', views.deactivate_users, name='deactivate_users'),
    path('admin/spaces/', views.admin_spaces, name='admin_spaces'),
    path('admin/spaces/mark-occupied/', views.mark_occupied, name='mark_occupied'),
    path('admin/spaces/mark-vacant/', views.mark_vacant, name='mark_vacant'),
    
    path('', include(router.urls)),
]
