from django.contrib import admin
from django.urls import path
from levelupapi.views import register_user, check_user
from django.conf.urls import include
from rest_framework import routers
from levelupapi.views import GameTypeView, EventView, GameView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'gametypes', GameTypeView, 'gametype')
router.register(r'events', EventView, 'event')
router.register(r'games', GameView, 'game')

urlpatterns = [
    path('register', register_user),
    path('checkuser', check_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]

# Requests to http://localhost:8000/register will be routed to the register_user function
path('register', register_user)
# Requests to http://localhost:8000/checkuser will be routed to the login_user function
path('checkuser', check_user),
