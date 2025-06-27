import logging
from utils.colors import Colors, VisualUtils

class MaxLevelFilter(logging.Filter):
    """
    Filter that only allows log records up to a specified maximum level.
    """
    def __init__(self, max_level):
        super().__init__()
        self.max_level = max_level

    def filter(self, record):
        # Only accept records whose level number is <= self.max_level
        return record.levelno <= self.max_level

class LoggerManager:

    _instance = None  # Singleton instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoggerManager, cls).__new__(cls)
            cls._instance.logger = None
            cls._instance.setup_logger()
        return cls._instance

    def setup_logger(self):
        if self.logger is None:
            self.logger = logging.getLogger('logger')
            self.logger.setLevel(logging.INFO)

            # 1) INFO handler
            info_handler = logging.StreamHandler()
            info_handler.setLevel(logging.INFO)
            info_format = '[*] %(asctime)s - %(message)s'
            info_datefmt = '%Y-%m-%d %H:%M:%S'
            info_formatter = logging.Formatter(info_format, info_datefmt)
            info_handler.setFormatter(info_formatter)

            # Add a filter to exclude ERROR level (and above) messages
            info_handler.addFilter(MaxLevelFilter(logging.INFO))

            self.logger.addHandler(info_handler)

            # 2) ERROR handler
            error_handler = logging.StreamHandler()
            error_handler.setLevel(logging.ERROR)
            error_format = '[!] %(asctime)s - %(message)s'
            error_datefmt = '%Y-%m-%d %H:%M:%S'
            error_formatter = logging.Formatter(error_format, error_datefmt)
            error_handler.setFormatter(error_formatter)

            self.logger.addHandler(error_handler)

    def info(self, message):
        """
        Log an INFO-level message.
        """
        self.logger.info(message)

    def error(self, message):
        """
        Log an ERROR-level message.
        """
        self.logger.error(message)

    def info_red(self, message):
        """
        Log an INFO-level message in red color.
        """
        colored_message = Colors.red(message)
        self.logger.info(colored_message)

    def info_green(self, message):
        """
        Log an INFO-level message in green color.
        """
        colored_message = Colors.green(message)
        self.logger.info(colored_message)
    
    def success(self, message):
        """
        Log a success message with enhanced styling.
        """
        colored_message = Colors.success(f"✓ {message}")
        self.logger.info(colored_message)
    
    def warning(self, message):
        """
        Log a warning message with enhanced styling.
        """
        colored_message = Colors.warning(f"⚠ {message}")
        self.logger.info(colored_message)
    
    def info_enhanced(self, message):
        """
        Log an info message with enhanced styling.
        """
        colored_message = Colors.info(f"ℹ {message}")
        self.logger.info(colored_message)
    
    def highlight(self, message):
        """
        Log a highlighted message.
        """
        colored_message = Colors.highlight(f"★ {message}")
        self.logger.info(colored_message)
    
    def tiktok_style(self, message, use_pink=True):
        """
        Log a message with TikTok brand styling.
        """
        colored_message = Colors.tiktok_theme(message, use_pink)
        self.logger.info(colored_message)
    
    def print_separator(self, char='─', color=None):
        """
        Print a separator line.
        """
        separator = VisualUtils.create_separator(char, color=color)
        print(separator)
    
    def print_box(self, message, padding=2, border_color=None):
        """
        Print a message in a box.
        """
        box = VisualUtils.create_box(message, padding, border_color)
        print(box)
    
    def print_status(self, message, status="INFO"):
        """
        Print a status message with timestamp and status badge.
        """
        VisualUtils.print_status(message, status)


logger = LoggerManager().logger
