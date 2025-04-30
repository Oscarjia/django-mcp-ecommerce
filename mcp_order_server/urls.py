from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'orders', views.OrderViewSet)
router.register(r'inventory', views.InventoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('orders/', views.get_orders, name='get_orders'),
    path('inventory/', views.get_inventory, name='get_inventory'),
    path('purchase/', views.purchase, name='purchase'),
    
    # MCP Server endpoints
    path('mcp/tool/<str:tool_name>/', views.mcp_tool_handler, name='mcp_tool_handler'),
    path('mcp/tools/', views.mcp_tools, name='mcp_tools'),
]