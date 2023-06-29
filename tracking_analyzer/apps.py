from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TrackingAnalyzerAppConfig(AppConfig):
    name = 'tracking_analyzer'
    verbose_name = _('Django Tracking Analyzer')
