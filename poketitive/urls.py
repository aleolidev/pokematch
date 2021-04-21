from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.config import settings
from django.config.urls.static import static

from pokemoncompetitive import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    # path('', views.showmons, name='showmons')
] +static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# urlpatterns += staticfiles_urlpatterns()