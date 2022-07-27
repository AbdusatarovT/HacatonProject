
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
     openapi.Info(
        title='Pythonяшки: Команда: Тахир, Амир',
        default_version='Turbo Version',
        description='Интернет магазин сотовых телефонов'
    ),
    public=True
)


urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger')),
    path('admin/', admin.site.urls),
    path('product/', include('product.urls')),
    path('api/account/', include('account.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
