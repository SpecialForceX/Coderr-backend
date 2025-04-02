from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from offers_app.api.urls import offer_urls, offerdetail_urls
from orders_app.api.views import CompletedOrderCountView, InProgressOrderCountView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/offers/', include(offer_urls)),
    path('api/offerdetails/', include(offerdetail_urls)),
    path('api/orders/', include('orders_app.api.urls')),
    path('api/profiles/', include('users_app.api.urls')),
    path('api/base-info/', include('baseinfo_app.api.urls')),
    path('api/reviews/', include('reviews_app.api.urls')),
    path('api/order-count/<int:business_user_id>/', InProgressOrderCountView.as_view(), name='order-count'),
    path('api/completed-order-count/<int:business_user_id>/', CompletedOrderCountView.as_view(), name='completed-order-count'),
    path('api/', include('users_app.api.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

