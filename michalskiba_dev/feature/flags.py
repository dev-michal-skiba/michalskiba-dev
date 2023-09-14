import logging

from feature.models import Flag

logger = logging.getLogger(__name__)

ENABLE_SENTRY_TESTING_ENDPOINT = "enable_sentry_testing_endpoint"
FLAGS = [ENABLE_SENTRY_TESTING_ENDPOINT]


def is_flag_enabled(flag_name: str) -> bool:
    if flag_name not in FLAGS:
        return False
    try:
        flag = Flag.objects.get(name=flag_name)
        return flag.enabled
    except Flag.DoesNotExist:
        logger.error("Tried to check non existing flag '%s'", flag_name)
        return False
