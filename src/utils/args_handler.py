import argparse
import re

from utils.custom_exceptions import ArgsParseError
from utils.enums import Mode, Regex


def parse_args():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="TikTok Live Recorder - A tool for recording live TikTok sessions.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "-url",
        dest="url",
        help="Record a live session from the TikTok URL.",
        action='store'
    )

    parser.add_argument(
        "-user",
        dest="user",
        help="Record a live session from the TikTok username.",
        action='store'
    )

    parser.add_argument(
        "-room_id",
        dest="room_id",
        help="Record a live session from the TikTok room ID.",
        action='store'
    )

    # Multi-stream support
    parser.add_argument(
        "-urls",
        dest="urls",
        nargs='+',
        help="Record multiple live sessions from TikTok URLs (space-separated).",
        action='store'
    )

    parser.add_argument(
        "-users",
        dest="users",
        nargs='+',
        help="Record multiple live sessions from TikTok usernames (space-separated).",
        action='store'
    )

    parser.add_argument(
        "-users-file",
        dest="users_file",
        help="Import usernames from a text file (one username per line).",
        action='store'
    )

    parser.add_argument(
        "-room_ids",
        dest="room_ids",
        nargs='+',
        help="Record multiple live sessions from TikTok room IDs (space-separated).",
        action='store'
    )

    parser.add_argument(
        "-mode",
        dest="mode",
        help=(
            "Recording mode: (manual, automatic) [Default: manual]\n"
            "[manual] => Manual live recording.\n"
            "[automatic] => Automatic live recording when the user is live."
        ),
        default="manual",
        action='store'
    )

    parser.add_argument(
        "-automatic_interval",
        dest="automatic_interval",
        help="Sets the interval in minutes to check if the user is live in automatic mode. [Default: 5]",
        type=int,
        default=5,
        action='store'
    )


    parser.add_argument(
        "-proxy",
        dest="proxy",
        help=(
            "Use HTTP proxy to bypass login restrictions in some countries.\n"
            "Example: -proxy http://127.0.0.1:8080"
        ),
        action='store'
    )

    parser.add_argument(
        "-output",
        dest="output",
        help=(
            "Specify the output directory where recordings will be saved.\n"
        ),
        action='store'
    )

    parser.add_argument(
        "-duration",
        dest="duration",
        help="Specify the duration in seconds to record the live session [Default: None].",
        type=int,
        default=None,
        action='store'
    )

    parser.add_argument(
        "-telegram",
        dest="telegram",
        action="store_true",
        help="Activate the option to upload the video to Telegram at the end "
             "of the recording.\nRequires configuring the telegram.json file",
    )

    parser.add_argument(
        "-no-update-check",
        dest="update_check",
        action="store_false",
        help=(
            "Disable the check for updates before running the program. "
            "By default, update checking is enabled."
        )
    )

    parser.add_argument(
        "-enable-resolution-restart",
        dest="enable_resolution_restart",
        help=(
            "Enable automatic restart when resolution changes are detected.\n"
            "Specify 'user' or 'room' to set per-user or per-room setting.\n"
            "Example: -enable-resolution-restart user"
        ),
        action='store'
    )

    parser.add_argument(
        "-disable-resolution-restart",
        dest="disable_resolution_restart",
        help=(
            "Disable automatic restart when resolution changes are detected.\n"
            "Specify 'user' or 'room' to set per-user or per-room setting.\n"
            "Example: -disable-resolution-restart user"
        ),
        action='store'
    )

    parser.add_argument(
        "-resolution-check-interval",
        dest="resolution_check_interval",
        help="Set the interval in seconds to check for resolution changes. [Default: 5]",
        type=int,
        default=None,
        action='store'
    )

    args = parser.parse_args()

    return args


def validate_and_parse_args():
    args = parse_args()

    # Check if using single stream mode or multi-stream mode
    single_stream_args = [args.user, args.room_id, args.url]
    multi_stream_args = [args.users, args.room_ids, args.urls, args.users_file]
    
    single_stream_provided = any(single_stream_args)
    multi_stream_provided = any(multi_stream_args)
    
    if not single_stream_provided and not multi_stream_provided:
        raise ArgsParseError("Missing URL, username, or room ID. Please provide one of these parameters (or use -urls, -users, -room_ids, -users-file for multiple streams).")
    
    if single_stream_provided and multi_stream_provided:
        raise ArgsParseError("Cannot mix single stream and multi-stream arguments. Use either single stream (-url, -user, -room_id) or multi-stream (-urls, -users, -room_ids) arguments.")
    
    # For multi-stream mode, ensure only one type is provided (but allow -users and -users-file together)
    if multi_stream_provided:
        exclusive_args = [args.urls, args.room_ids]
        user_args = [args.users, args.users_file]
        
        exclusive_count = sum(1 for arg in exclusive_args if arg is not None)
        user_count = sum(1 for arg in user_args if arg is not None)
        
        if exclusive_count > 1 or (exclusive_count > 0 and user_count > 0):
            raise ArgsParseError("Please provide only one type of multi-stream input: either -urls, -room_ids, or user inputs (-users and/or -users-file).")
    
    # Process single stream arguments
    if single_stream_provided:
        if args.user and args.user.startswith('@'):
            args.user = args.user[1:]
        
        if (args.user and args.room_id) or (args.user and args.url) or (args.room_id and args.url):
            raise ArgsParseError("Please provide only one among username, room ID, or URL.")
        
        if args.url and not re.match(str(Regex.IS_TIKTOK_LIVE), args.url):
            raise ArgsParseError("The provided URL does not appear to be a valid TikTok live URL.")
    
    # Process multi-stream arguments
    if multi_stream_provided:
        if args.users:
            # Clean up usernames (remove @ prefix if present)
            args.users = [user[1:] if user.startswith('@') else user for user in args.users]
        
        if args.urls:
            # Validate all URLs
            for url in args.urls:
                if not re.match(str(Regex.IS_TIKTOK_LIVE), url):
                    raise ArgsParseError(f"The provided URL '{url}' does not appear to be a valid TikTok live URL.")
    
    if not args.mode:
        raise ArgsParseError("Missing mode value. Please specify the mode (manual or automatic).")
    if args.mode not in ["manual", "automatic"]:
        raise ArgsParseError("Incorrect mode value. Choose between 'manual' and 'automatic'.")

    if (args.automatic_interval < 1):
        raise ArgsParseError("Incorrect automatic_interval value. Must be one minute or more.")

    mode = Mode.MANUAL if args.mode == "manual" else Mode.AUTOMATIC

    return args, mode
