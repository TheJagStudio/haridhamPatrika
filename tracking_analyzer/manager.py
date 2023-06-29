import logging
from django.contrib.auth.models import User
from django.db import models
from django.http import HttpRequest
from ipware.ip import get_client_ip
import pygeoip

logger = logging.getLogger('tracking_analyzer')


class TrackerManager(models.Manager):
    def create_from_request(self, request, content_object):
        assert isinstance(request, HttpRequest), \
            '`request` object is not an `HTTPRequest`'
        assert issubclass(content_object.__class__, models.Model), \
            '`content_object` is not a Django model'

        user = request.user
        user = user if isinstance(user, User) else None

        if request.user_agent.is_mobile:
            device_type = self.model.MOBILE
        elif request.user_agent.is_tablet:
            device_type = self.model.TABLET
        elif request.user_agent.is_pc:
            device_type = self.model.PC
        elif request.user_agent.is_bot:
            device_type = self.model.BOT
        else:
            device_type = self.model.UNKNOWN

        ip_address, _ = get_client_ip(request) or ''
        if not ip_address:
            logger.debug(
                'Could not determine IP address for request %s', request)
        else:
            geo = pygeoip.GeoIP('/static/GeoIPCity.dat')

        tracker = self.model.objects.create(
            content_object=content_object,
            ip_address=ip_address,
            ip_country=geo['country_name'] or '',
            ip_region=geo['region_code'] or '',
            ip_city=geo['city'] or '',
            referrer=request.META.get('HTTP_REFERER', ''),
            device_type=device_type,
            device=request.user_agent.device.family,
            browser=request.user_agent.browser.family[:30],
            browser_version=request.user_agent.browser.version_string,
            system=request.user_agent.os.family,
            system_version=request.user_agent.os.version_string,
            user=user
        )
        logger.info(
            'Tracked click in %s %s.',
            content_object._meta.object_name, content_object.pk
        )

        return tracker
