from django.urls import path
from .import views
from rest_framework.routers import SimpleRouter

router=SimpleRouter()
router.register("categorys",views.CategoryViewSet)
router.register("",views.ProductViewSet)

urlpatterns = [

] + router.urls