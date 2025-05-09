import os
import re
import logging

from backend.services import logger as logger_module

# Test para la configuración del logger
class TestLogger:
    def test_configuration(self):
        logger = logger_module.logger
        assert logger.name == "iptv_logger"
        assert logger.level == getattr(logging, logger_module.config.LOGS_LEVEL.upper(), logging.INFO)

        handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
        assert handlers

        log_path = handlers[0].baseFilename
        assert os.path.exists(log_path)
        assert re.match(r'.*\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}\.log$', log_path)