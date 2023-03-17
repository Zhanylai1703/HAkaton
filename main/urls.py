from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from apps.users import views
from rest_framework.routers import DefaultRouter
from apps.users.views import UserViewSet



schema_view = get_schema_view(
   openapi.Info(
      title="user API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

router = DefaultRouter()
router.register(r'users/', UserViewSet, basename='users')
urlpatterns = router.urls

api_v1 = [
    path('reg/', views.RegisterView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('profiles/', views.ProfileCreateView.as_view()),
    path('prpfile/', views.ProfileCreateView.as_view()),
    path('profile/', views.ProfileRetrieveUpdateDestroyView.as_view())
    

]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/', include(api_v1)),
    path('users/', include('apps.users.urls')),
    path('', include('apps.dashboard.urls')),
    
    ]
