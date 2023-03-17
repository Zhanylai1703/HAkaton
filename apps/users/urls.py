
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'', UserViewSet, basename='users')
router.register(r'dep/', DepartmentViewSet, basename='departments')
urlpatterns = router.urls