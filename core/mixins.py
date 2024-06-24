from typing import Dict, Self
from pusher import Pusher
from rest_framework.pagination import PageNumberPagination

from app import settings

class BasePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class AppBroadcaster(object):
    broadcaster: Pusher|None = None

    def __new__(cls) -> Self:
        if not hasattr(cls, 'instance'):
            cls.instance = super(AppBroadcaster, cls).__new__(cls)
        if cls.broadcaster == None:
            if settings.WSS_TYPE == 'pusher':
                cls.broadcaster = Pusher(
                    app_id=settings.WSS_APP_ID,
                    key=settings.WSS_APP_KEY,
                    secret=settings.WSS_APP_SECRET,
                    cluster=settings.WSS_APP_CLUSTER,
                )
            else:
                cls.broadcaster = Pusher(
                    host=settings.WSS_HOST,
                    port=int(settings.WSS_PORT),
                    app_id=settings.WSS_APP_ID,
                    key=settings.WSS_APP_KEY,
                    secret=settings.WSS_APP_SECRET,
                    ssl=False,
                )
        return cls.instance

    def notify(self, event: str, data: Dict|None, user: object|None):
        if user is not None:
            self.broadcaster.trigger(
                [f'account-{user.uuid}'],
                event,
                data,
            )
        else:
            self.broadcaster.trigger(
                ['public'],
                event,
                data,
            )
