import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


class AppLogger:
    _instance = None

    def __new__(cls, name: str = "app") -> "AppLogger":
        """Singleton pattern to ensure only one logger instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._setup_logger(name)
        return cls._instance
    
    def get_logger(self, name: str = "app") -> logging.Logger:
        """Returns the logger instance."""
        if not hasattr(self, 'logger'):
            self._setup_logger(name)
        return self.logger
    
    def _setup_logger(self, name: str = "app") -> None:
        """Set up the logger with console and file handlers."""
        log_dir = Path("logs")
        log_dir.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(pathname)s:%(lineno)d - %(funcName)s() | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # Avoid duplicate handlers
        if self.logger.hasHandlers():
            # Stream events to terminal
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.DEBUG)
            stream_handler.setFormatter(formatter)

            # Handler for storing results in a file for upto 5 backups max, 5 MB each
            file_handler = RotatingFileHandler(
                log_dir / "app.log", maxBytes=5 * 1024 * 1024, backupCount=5
            )
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)
            
            # Add handlers to the logger
            self.logger.addHandler(stream_handler)
            self.logger.addHandler(file_handler)