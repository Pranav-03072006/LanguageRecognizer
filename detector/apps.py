"""
Detector AppConfig
Pre-loads the joblib model artifact once at application startup.
"""

import logging
import sys
from django.apps import AppConfig

logger = logging.getLogger("detector")


class DetectorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "detector"

    def ready(self):
        """
        Called when Django starts up. Pre-loads the trained model artifact
        into memory so it is ready for incoming requests without delay.
        """
        # Skip preloading during database migrations or initial collectstatic commands
        skip_commands = {"makemigrations", "migrate", "collectstatic"}
        if any(cmd in sys.argv for cmd in skip_commands):
            return

        try:
            from .services.model_service import LanguageModelService

            service = LanguageModelService.get_instance()
            loaded = service.load_model()
            if loaded:
                logger.info("Language Recognizer ML Model successfully pre-loaded at startup.")
            else:
                logger.warning(
                    "Model artifact not found yet. Run `python train_model.py` "
                    "to generate artifacts/language_recognizer.joblib."
                )
        except Exception as exc:
            logger.warning("Could not pre-load model artifact at startup: %s", exc)
