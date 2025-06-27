# print enhanced banner
from utils.utils import banner, show_startup_info

banner(enhanced=True, animated=False)
show_startup_info()


import sys
import os

from utils.args_handler import validate_and_parse_args
from utils.utils import read_cookies
from utils.logger_manager import logger
from utils.config_manager import ConfigManager
from utils.resolution_detector import ResolutionDetector

from core.tiktok_recorder import TikTokRecorder
from core.multi_stream_recorder import MultiStreamRecorder
from utils.enums import TikTokError
from utils.custom_exceptions import LiveNotFound, ArgsParseError, \
    UserLiveException, IPBlockedByWAF, TikTokException

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    try:
        args, mode = validate_and_parse_args()


        # read cookies from file
        cookies = read_cookies()
        
        # Handle resolution restart configuration
        config_manager = ConfigManager()
        
        # Check if ffprobe is available for resolution detection
        if (args.enable_resolution_restart or args.disable_resolution_restart or 
            args.resolution_check_interval is not None):
            if not ResolutionDetector.is_ffprobe_available():
                logger.warning("ffprobe is not available. Resolution change detection features disabled.")
                logger.warning("Install ffmpeg to enable resolution change detection.")
            else:
                # Handle enable/disable resolution restart
                if args.enable_resolution_restart:
                    setting_type = args.enable_resolution_restart.lower()
                    if setting_type not in ['user', 'room']:
                        raise ArgsParseError("Invalid value for -enable-resolution-restart. Use 'user' or 'room'.")
                    
                    # Handle single stream mode
                    if setting_type == 'user' and args.user:
                        config_manager.set_user_setting(args.user, "restart_on_resolution_change", True)
                    elif setting_type == 'room' and args.room_id:
                        config_manager.set_room_setting(args.room_id, "restart_on_resolution_change", True)
                    # Handle multi-stream mode
                    elif setting_type == 'user' and args.users:
                        for user in args.users:
                            config_manager.set_user_setting(user, "restart_on_resolution_change", True)
                    elif setting_type == 'room' and args.room_ids:
                        for room_id in args.room_ids:
                            config_manager.set_room_setting(room_id, "restart_on_resolution_change", True)
                    else:
                        logger.warning(f"Cannot set {setting_type} setting without providing {setting_type} identifier.")
                
                if args.disable_resolution_restart:
                    setting_type = args.disable_resolution_restart.lower()
                    if setting_type not in ['user', 'room']:
                        raise ArgsParseError("Invalid value for -disable-resolution-restart. Use 'user' or 'room'.")
                    
                    # Handle single stream mode
                    if setting_type == 'user' and args.user:
                        config_manager.set_user_setting(args.user, "restart_on_resolution_change", False)
                    elif setting_type == 'room' and args.room_id:
                        config_manager.set_room_setting(args.room_id, "restart_on_resolution_change", False)
                    # Handle multi-stream mode
                    elif setting_type == 'user' and args.users:
                        for user in args.users:
                            config_manager.set_user_setting(user, "restart_on_resolution_change", False)
                    elif setting_type == 'room' and args.room_ids:
                        for room_id in args.room_ids:
                            config_manager.set_room_setting(room_id, "restart_on_resolution_change", False)
                    else:
                        logger.warning(f"Cannot set {setting_type} setting without providing {setting_type} identifier.")
                
                # Handle resolution check interval
                if args.resolution_check_interval is not None:
                    if args.resolution_check_interval < 1:
                        raise ArgsParseError("Resolution check interval must be at least 1 second.")
                    
                    # Apply to user or room based on what's provided
                    if args.user:
                        config_manager.set_user_setting(args.user, "resolution_check_interval", args.resolution_check_interval)
                    elif args.room_id:
                        config_manager.set_room_setting(args.room_id, "resolution_check_interval", args.resolution_check_interval)
                    # Handle multi-stream mode
                    elif args.users:
                        for user in args.users:
                            config_manager.set_user_setting(user, "resolution_check_interval", args.resolution_check_interval)
                    elif args.room_ids:
                        for room_id in args.room_ids:
                            config_manager.set_room_setting(room_id, "resolution_check_interval", args.resolution_check_interval)
                    else:
                        # Set as default if no specific user/room provided
                        config_manager.config["default"]["resolution_check_interval"] = args.resolution_check_interval
                        config_manager._save_config()

        # Check if using multi-stream mode
        if args.urls or args.users or args.room_ids:
            # Multi-stream mode
            targets = []
            
            if args.urls:
                targets = [(url, None, None) for url in args.urls]
            elif args.users:
                targets = [(None, user, None) for user in args.users]
            elif args.room_ids:
                targets = [(None, None, room_id) for room_id in args.room_ids]
            
            logger.info(f"Multi-stream mode: Recording {len(targets)} streams")
            
            MultiStreamRecorder(
                targets=targets,
                mode=mode,
                automatic_interval=args.automatic_interval,
                cookies=cookies,
                proxy=args.proxy,
                output=args.output,
                duration=args.duration,
                use_telegram=args.telegram,
            ).run()
        else:
            # Single stream mode (original behavior)
            TikTokRecorder(
                url=args.url,
                user=args.user,
                room_id=args.room_id,
                mode=mode,
                automatic_interval=args.automatic_interval,
                cookies=cookies,
                proxy=args.proxy,
                output=args.output,
                duration=args.duration,
                use_telegram=args.telegram,
            ).run()

    except ArgsParseError as ex:
        logger.error(ex)

    except LiveNotFound as ex:
        logger.error(ex)

    except IPBlockedByWAF:
        logger.error(TikTokError.WAF_BLOCKED)

    except UserLiveException as ex:
        logger.error(ex)

    except TikTokException as ex:
        logger.error(ex)

    except Exception as ex:
        logger.error(ex)


if __name__ == "__main__":
    main()
