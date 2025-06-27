#!/usr/bin/env python3
"""
Configuration utility for TikTok Live Recorder resolution restart settings
"""

import argparse
import sys
import os

# Add the parent directory to sys.path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.config_manager import ConfigManager
from utils.resolution_detector import ResolutionDetector
from utils.logger_manager import logger


def main():
    parser = argparse.ArgumentParser(
        description="Configure resolution restart settings for TikTok Live Recorder",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='action', help='Available actions')
    
    # List settings
    list_parser = subparsers.add_parser('list', help='List current settings')
    
    # Enable restart
    enable_parser = subparsers.add_parser('enable', help='Enable resolution restart')
    enable_parser.add_argument('--user', help='Username to configure')
    enable_parser.add_argument('--room', help='Room ID to configure')
    enable_parser.add_argument('--global', action='store_true', help='Set as global default')
    
    # Disable restart
    disable_parser = subparsers.add_parser('disable', help='Disable resolution restart')
    disable_parser.add_argument('--user', help='Username to configure')
    disable_parser.add_argument('--room', help='Room ID to configure')
    disable_parser.add_argument('--global', action='store_true', help='Set as global default')
    
    # Set interval
    interval_parser = subparsers.add_parser('interval', help='Set resolution check interval')
    interval_parser.add_argument('seconds', type=int, help='Check interval in seconds')
    interval_parser.add_argument('--user', help='Username to configure')
    interval_parser.add_argument('--room', help='Room ID to configure')
    interval_parser.add_argument('--global', action='store_true', help='Set as global default')
    
    # Test detection
    test_parser = subparsers.add_parser('test', help='Test resolution detection capability')
    test_parser.add_argument('url', nargs='?', help='Test URL (optional)')
    
    args = parser.parse_args()
    
    if not args.action:
        parser.print_help()
        return
    
    config_manager = ConfigManager()
    
    if args.action == 'list':
        print("🔧 TikTok Live Recorder - Resolution Restart Settings")
        print("=" * 60)
        
        # Show global defaults
        default_config = config_manager.config.get('default', {})
        print(f"Global Defaults:")
        print(f"  Restart on resolution change: {default_config.get('restart_on_resolution_change', False)}")
        print(f"  Check interval: {default_config.get('resolution_check_interval', 5)} seconds")
        print()
        
        # Show user settings
        users = config_manager.config.get('users', {})
        if users:
            print("User-specific settings:")
            for user, settings in users.items():
                print(f"  @{user}:")
                print(f"    Restart on resolution change: {settings.get('restart_on_resolution_change', 'default')}")
                print(f"    Check interval: {settings.get('resolution_check_interval', 'default')} seconds")
            print()
        
        # Show room settings
        rooms = config_manager.config.get('rooms', {})
        if rooms:
            print("Room-specific settings:")
            for room_id, settings in rooms.items():
                print(f"  Room {room_id}:")
                print(f"    Restart on resolution change: {settings.get('restart_on_resolution_change', 'default')}")
                print(f"    Check interval: {settings.get('resolution_check_interval', 'default')} seconds")
            print()
        
        # Check ffprobe availability
        if ResolutionDetector.is_ffprobe_available():
            print("✅ ffprobe is available - resolution detection is supported")
        else:
            print("❌ ffprobe is NOT available - resolution detection is disabled")
            print("   Install ffmpeg to enable resolution change detection")
    
    elif args.action == 'enable':
        if getattr(args, 'global'):
            config_manager.config['default']['restart_on_resolution_change'] = True
            config_manager._save_config()
            print("✅ Enabled resolution restart globally")
        elif args.user:
            config_manager.set_user_setting(args.user, 'restart_on_resolution_change', True)
            print(f"✅ Enabled resolution restart for user @{args.user}")
        elif args.room:
            config_manager.set_room_setting(args.room, 'restart_on_resolution_change', True)
            print(f"✅ Enabled resolution restart for room {args.room}")
        else:
            print("❌ Please specify --user, --room, or --global")
    
    elif args.action == 'disable':
        if getattr(args, 'global'):
            config_manager.config['default']['restart_on_resolution_change'] = False
            config_manager._save_config()
            print("✅ Disabled resolution restart globally")
        elif args.user:
            config_manager.set_user_setting(args.user, 'restart_on_resolution_change', False)
            print(f"✅ Disabled resolution restart for user @{args.user}")
        elif args.room:
            config_manager.set_room_setting(args.room, 'restart_on_resolution_change', False)
            print(f"✅ Disabled resolution restart for room {args.room}")
        else:
            print("❌ Please specify --user, --room, or --global")
    
    elif args.action == 'interval':
        if args.seconds < 1:
            print("❌ Interval must be at least 1 second")
            return
        
        if getattr(args, 'global'):
            config_manager.config['default']['resolution_check_interval'] = args.seconds
            config_manager._save_config()
            print(f"✅ Set global resolution check interval to {args.seconds} seconds")
        elif args.user:
            config_manager.set_user_setting(args.user, 'resolution_check_interval', args.seconds)
            print(f"✅ Set resolution check interval to {args.seconds} seconds for user @{args.user}")
        elif args.room:
            config_manager.set_room_setting(args.room, 'resolution_check_interval', args.seconds)
            print(f"✅ Set resolution check interval to {args.seconds} seconds for room {args.room}")
        else:
            print("❌ Please specify --user, --room, or --global")
    
    elif args.action == 'test':
        if not ResolutionDetector.is_ffprobe_available():
            print("❌ ffprobe is not available. Install ffmpeg to test resolution detection.")
            return
        
        test_url = args.url
        if not test_url:
            print("🧪 Testing ffprobe availability...")
            print("✅ ffprobe is available and can be used for resolution detection")
            print("To test with a specific stream, provide a URL: python configure_resolution.py test <url>")
            return
        
        print(f"🧪 Testing resolution detection on: {test_url}")
        
        detector = ResolutionDetector(test_url)
        resolution = detector.get_current_resolution()
        
        if resolution:
            print(f"✅ Resolution detected: {resolution[0]}x{resolution[1]}")
        else:
            print("❌ Could not detect resolution. This might be because:")
            print("   - The URL is not accessible")
            print("   - The stream is not currently live")
            print("   - The stream format is not supported")
            print("   - Network connectivity issues")


if __name__ == "__main__":
    main()
