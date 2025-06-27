"""
Enhanced color and visual utility module for console output
"""
import shutil
import time
import sys
from typing import Optional

class Colors:
    """ANSI color codes and visual utilities for terminal output"""
    # Reset
    RESET = '\033[0m'
    
    # Standard colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    # Text styles
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    STRIKETHROUGH = '\033[9m'
    
    # Custom theme colors for TikTok Live Recorder
    TIKTOK_PINK = '\033[38;5;198m'  # Bright pink
    TIKTOK_BLUE = '\033[38;5;39m'   # Bright blue
    SUCCESS = '\033[38;5;46m'       # Bright green
    WARNING = '\033[38;5;220m'      # Golden yellow
    ERROR = '\033[38;5;196m'        # Bright red
    INFO = '\033[38;5;75m'          # Light blue
    HIGHLIGHT = '\033[38;5;226m'    # Bright yellow

    @staticmethod
    def colorize(text: str, color: str) -> str:
        """
        Apply color to text
        
        Args:
            text: The text to colorize
            color: The color code to apply
            
        Returns:
            Colored text string
        """
        return f"{color}{text}{Colors.RESET}"
    
    @staticmethod
    def red(text: str) -> str:
        """Make text red"""
        return Colors.colorize(text, Colors.RED)
    
    @staticmethod
    def green(text: str) -> str:
        """Make text green"""
        return Colors.colorize(text, Colors.GREEN)
    
    @staticmethod
    def yellow(text: str) -> str:
        """Make text yellow"""
        return Colors.colorize(text, Colors.YELLOW)
    
    @staticmethod
    def blue(text: str) -> str:
        """Make text blue"""
        return Colors.colorize(text, Colors.BLUE)
    
    @staticmethod
    def magenta(text: str) -> str:
        """Make text magenta"""
        return Colors.colorize(text, Colors.MAGENTA)
    
    @staticmethod
    def cyan(text: str) -> str:
        """Make text cyan"""
        return Colors.colorize(text, Colors.CYAN)
    
    @staticmethod
    def bold(text: str) -> str:
        """Make text bold"""
        return Colors.colorize(text, Colors.BOLD)
    
    @staticmethod
    def underline(text: str) -> str:
        """Make text underlined"""
        return Colors.colorize(text, Colors.UNDERLINE)
    
    @staticmethod
    def success(text: str) -> str:
        """Style text as success message"""
        return Colors.colorize(text, Colors.SUCCESS)
    
    @staticmethod
    def warning(text: str) -> str:
        """Style text as warning message"""
        return Colors.colorize(text, Colors.WARNING)
    
    @staticmethod
    def error(text: str) -> str:
        """Style text as error message"""
        return Colors.colorize(text, Colors.ERROR)
    
    @staticmethod
    def info(text: str) -> str:
        """Style text as info message"""
        return Colors.colorize(text, Colors.INFO)
    
    @staticmethod
    def highlight(text: str) -> str:
        """Highlight text"""
        return Colors.colorize(text, Colors.HIGHLIGHT)
    
    @staticmethod
    def tiktok_theme(text: str, use_pink: bool = True) -> str:
        """Apply TikTok brand colors"""
        color = Colors.TIKTOK_PINK if use_pink else Colors.TIKTOK_BLUE
        return Colors.colorize(text, color)


class VisualUtils:
    """Utility class for enhanced visual output"""
    
    @staticmethod
    def get_terminal_width() -> int:
        """Get the width of the terminal"""
        return shutil.get_terminal_size().columns
    
    @staticmethod
    def center_text(text: str, width: Optional[int] = None, fill_char: str = ' ') -> str:
        """Center text in terminal"""
        if width is None:
            width = VisualUtils.get_terminal_width()
        return text.center(width, fill_char)
    
    @staticmethod
    def create_separator(char: str = '─', width: Optional[int] = None, color: Optional[str] = None) -> str:
        """Create a separator line"""
        if width is None:
            width = VisualUtils.get_terminal_width()
        separator = char * width
        if color:
            separator = Colors.colorize(separator, color)
        return separator
    
    @staticmethod
    def create_box(text: str, padding: int = 2, border_color: Optional[str] = None) -> str:
        """Create a text box with borders"""
        lines = text.split('\n')
        max_length = max(len(line) for line in lines) if lines else 0
        box_width = max_length + (padding * 2) + 2
        
        # Top border
        top = '┌' + '─' * (box_width - 2) + '┐'
        if border_color:
            top = Colors.colorize(top, border_color)
        
        # Content lines
        content_lines = []
        for line in lines:
            padded_line = '│' + ' ' * padding + line.ljust(max_length) + ' ' * padding + '│'
            if border_color:
                padded_line = Colors.colorize(padded_line, border_color)
            content_lines.append(padded_line)
        
        # Bottom border
        bottom = '└' + '─' * (box_width - 2) + '┘'
        if border_color:
            bottom = Colors.colorize(bottom, border_color)
        
        return '\n'.join([top] + content_lines + [bottom])
    
    @staticmethod
    def create_progress_bar(current: int, total: int, width: int = 30, 
                           fill_char: str = '█', empty_char: str = '░',
                           show_percentage: bool = True) -> str:
        """Create a progress bar"""
        if total == 0:
            percentage = 0
        else:
            percentage = min(100, int((current / total) * 100))
        
        filled_width = int((percentage / 100) * width)
        bar = fill_char * filled_width + empty_char * (width - filled_width)
        
        if show_percentage:
            return f"[{bar}] {percentage}%"
        return f"[{bar}]"
    
    @staticmethod
    def print_status(message: str, status: str = "INFO", color_map: Optional[dict] = None) -> None:
        """Print a formatted status message"""
        default_colors = {
            "INFO": Colors.INFO,
            "SUCCESS": Colors.SUCCESS,
            "WARNING": Colors.WARNING,
            "ERROR": Colors.ERROR,
        }
        
        if color_map:
            default_colors.update(color_map)
        
        color = default_colors.get(status, Colors.WHITE)
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        
        status_badge = Colors.colorize(f"[{status}]", color)
        time_badge = Colors.colorize(f"[{timestamp}]", Colors.DIM)
        
        print(f"{time_badge} {status_badge} {message}")
    
    @staticmethod
    def animate_text(text: str, delay: float = 0.05) -> None:
        """Animate text by typing it out character by character"""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()  # New line at the end
    
    @staticmethod
    def create_banner_box(title: str, subtitle: str = "", version: str = "") -> str:
        """Create an enhanced banner box"""
        terminal_width = VisualUtils.get_terminal_width()
        box_width = min(80, terminal_width - 4)  # Leave some margin
        
        # Title styling
        styled_title = Colors.tiktok_theme(Colors.bold(title), use_pink=True)
        
        lines = [styled_title]
        if subtitle:
            lines.append(Colors.colorize(subtitle, Colors.CYAN))
        if version:
            lines.append(Colors.colorize(f"Version {version}", Colors.DIM))
        
        content = '\n'.join(lines)
        return VisualUtils.create_box(content, padding=3, border_color=Colors.TIKTOK_BLUE)
