from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# The added static allows urls to be created out of images when they are uploaded
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Chirper.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
