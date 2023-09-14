import logging
from typing import Any

from django.core.management.base import BaseCommand

from feature.flags import FLAGS
from feature.models import Flag

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Detect new flags"

    def handle(self, *args: list[Any], **options: dict[str, Any]) -> None:
        logger.info("Detecting new flags")
        for flag_name in FLAGS:
            exists = Flag.objects.filter(name=flag_name).exists()
            if not exists:
                Flag.objects.create(name=flag_name, enabled=False)
                logger.info(f"Added disabled flag '{flag_name}'")
