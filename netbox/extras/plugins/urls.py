from django.apps import apps
from django.conf import settings
from django.conf.urls import include
from django.urls import path
from django.utils.module_loading import import_string

from . import views

# Plugins
plugin_patterns = []
plugin_api_patterns = []

for plugin in settings.PLUGINS:
    app = apps.get_app_config(plugin)

    base_url = getattr(app, 'base_url') or app.label

    # Check if the plugin specifies any URLs
    try:
        urlpatterns = import_string(f"{plugin}.urls.urlpatterns")
        plugin_patterns.append(
            path(f"{base_url}/", include((urlpatterns, app.label)))
        )
    except ImportError:
        pass

    # Check if the plugin specifies any API URLs
    try:
        urlpatterns = import_string(f"{plugin}.api.urls.urlpatterns")
        plugin_api_patterns.append(
            path(f"{base_url}/", include((urlpatterns, f"{app.label}-api")))
        )
    except ImportError:
        pass

# Plugin list admin view
admin_plugin_patterns = [
    path('', views.installed_plugins_admin_view, name='plugins_list')
]

# Plugin list API view
plugin_api_patterns += [
    path('', views.PluginsAPIRootView.as_view(), name='api-root'),
    path('installed-plugins/', views.InstalledPluginsAPIView.as_view(), name='plugins-list')
]
