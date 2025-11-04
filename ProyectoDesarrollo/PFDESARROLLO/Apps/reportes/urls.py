from django.urls import path
from .views import DashboardReportesView, generar_reporte_dia

app_name = 'reportes_app'

urlpatterns = [

    path('dashboard/', DashboardReportesView.as_view(), name='dashboard'),
    path('generar/', generar_reporte_dia, name='generar_reporte'),

]