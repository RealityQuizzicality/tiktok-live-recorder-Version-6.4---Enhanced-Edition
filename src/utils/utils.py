import json
import os
import random
from typing import Optional

from utils.enums import Info
from utils.colors import Colors, VisualUtils


def banner(enhanced: bool = True, animated: bool = False) -> None:
    """
    Prints a banner with the name of the tool and its version number.
    
    Args:
        enhanced: Use the enhanced styled banner
        animated: Animate the banner text
    """
    if enhanced:
        # Use enhanced banner with colors
        banner_text = str(Info.ENHANCED_BANNER)
        
        # Apply TikTok theme colors to the banner
        lines = banner_text.split('\n')
        colored_lines = []
        
        for line in lines:
            if '████' in line or '███' in line:
                # Color the ASCII art with TikTok colors
                colored_line = Colors.tiktok_theme(line, use_pink=True)
            elif 'Version' in line:
                # Highlight version info
                colored_line = Colors.highlight(line)
            elif '🚀' in line or '🎥' in line:
                # Color emoji lines
                colored_line = Colors.cyan(line)
            elif '═' in line or '║' in line:
                # Color borders
                colored_line = Colors.tiktok_theme(line, use_pink=False)
            else:
                colored_line = line
                
            colored_lines.append(colored_line)
        
        banner_output = '\n'.join(colored_lines)
        
        if animated:
            # Clear screen and animate banner
            print('\033[2J\033[H')  # Clear screen and move cursor to top
            VisualUtils.animate_text(banner_output, delay=0.01)
        else:
            print(banner_output)
            
        # Add some extra visual flair
        print()
        VisualUtils.print_status("TikTok Live Recorder is ready!", "SUCCESS")
        print()
        
    else:
        # Use classic banner
        print(str(Info.BANNER))


def show_startup_info() -> None:
    """
    Display enhanced startup information
    """
    features = [
        "🎯 Multi-stream recording support",
        "🔄 Automatic retry mechanism", 
        "📱 Telegram upload integration",
        "🎨 Enhanced visual interface",
        "⚡ Improved performance"
    ]
    
    print(Colors.info("Key Features:"))
    for feature in features:
        print(f"  {Colors.success('•')} {feature}")
    
    print()
    VisualUtils.print_status("Ready to record! Use --help for available options.", "INFO")


def read_cookies():
    """
    Loads the config file and returns it.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "..", "cookies.json")
    with open(config_path, "r") as f:
        return json.load(f)


def read_telegram_config():
    """
    Loads the telegram config file and returns it.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "..", "telegram.json")
    with open(config_path, "r") as f:
        return json.load(f)
