from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MapRegionViewSet, CandidateViewSet, GodPlayerViewSet, CampaignActionViewSet, RoundViewSet

router = DefaultRouter()
router.register(r'regions', MapRegionViewSet, basename='region')
router.register(r'candidates', CandidateViewSet, basename='candidate')
router.register(r'god', GodPlayerViewSet, basename='god')
router.register(r'actions', CampaignActionViewSet, basename='action')
router.register(r'rounds', RoundViewSet, basename='round')

urlpatterns = [
    path('', include(router.urls)),
]
