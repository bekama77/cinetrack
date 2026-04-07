from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("common.urls")),
    path("accounts/", include("accounts.urls")),
    path("movies/", include("movies.urls")),
    path("watchlists/", include("watchlists.urls")),
    path("reviews/", include("reviews.urls")),
    path("api/", include("api.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "common.views.custom_404"
handler500 = "common.views.custom_500"
