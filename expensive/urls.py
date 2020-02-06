from django.urls import  path

from rest_framework.routers import DefaultRouter

from expensive import viewsets

app_name = 'expensive'

expensive_api_router = DefaultRouter()
expensive_api_router.register(f"{app_name}/transactions", viewsets.TransactionViewSet, basename="expensive.Transaction")
expensive_api_router.register(f"{app_name}/yearly_report", viewsets.TransactionViewSet, basename="expensive.Transaction")
expensive_api_router.register(f"{app_name}/monthly_report", viewsets.TransactionViewSet, basename="expensive.Transaction")

# urlpatterns = expensive_api_router.urls
# urlpatterns += [
#     path(f"{app_name}/transactions/upload_file/", view=viewsets.TransactionViewSet.as_view({'post': 'upload_file'}), name='upload-file'),
# ]
