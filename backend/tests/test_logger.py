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

        file_handler = logger_module.file_handler
        assert file_handler in logger.handlers

        log_path = file_handler.baseFilename
        assert os.path.exists(log_path)
        assert re.match(r'.*\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}\.log$', log_path)

        test_message = "Test log message"
        logger.info(test_message)
        with open(log_path, encoding='utf-8') as f:
            content = f.read()
            assert test_message in content