from django.urls import path
from .views import DashboardReportesView, generar_reporte

app_name = 'reportes_app'

urlpatterns = [

    path('dashboard/', DashboardReportesView.as_view(), name='dashboard'),
    path('dashboard/generar/', generar_reporte, name='generar_reporte'),

]