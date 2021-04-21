from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.conf import settings
from django.conf.urls.static import static

from pokemoncompetitive import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    # path('', views.showmons, name='showmons')
]

urlpatterns += staticfiles_urlpatterns()
# urlpatterns += +static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)