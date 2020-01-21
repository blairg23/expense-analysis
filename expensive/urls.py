from django.urls import re_path

from rest_framework.routers import DefaultRouter

from expensive import viewsets

app_name = 'expensive'

router = DefaultRouter()
router.register(f"{app_name}/transactions", viewsets.TransactionViewSet, basename="expensive.Transaction")
