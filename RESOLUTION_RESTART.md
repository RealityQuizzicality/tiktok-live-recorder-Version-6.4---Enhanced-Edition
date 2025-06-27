# Resolution Change Auto-Restart Feature

This feature automatically detects when a TikTok live stream changes resolution (due to multi-streamer challenges, 4-way split screens, etc.) and can restart the recording with the new resolution.

## Overview

TikTok live streams can change resolution dynamically in several scenarios:
- **Single to dual streaming**: When a streamer joins a 2-person challenge
- **Dual to quad streaming**: When moving to a 4-person split screen
- **Device changes**: When streamers switch devices with different capabilities
- **Network adaptation**: When TikTok adjusts quality based on connection

## Requirements

- **ffmpeg/ffprobe**: Must be installed and available in your system PATH
- **Python 3.7+**: Required for the TikTok Live Recorder

### Installing ffmpeg

**macOS (using Homebrew):**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
1. Download from https://ffmpeg.org/download.html
2. Add ffmpeg to your system PATH

## Configuration

### Command Line Arguments

**Enable auto-restart for a specific user:**
```bash
python main.py -user username -enable-resolution-restart user
```

**Enable auto-restart for a specific room:**
```bash
python main.py -room_id 12345 -enable-resolution-restart room
```

**Disable auto-restart:**
```bash
python main.py -user username -disable-resolution-restart user
```

**Set check interval (how often to check for resolution changes):**
```bash
python main.py -user username -resolution-check-interval 3
```

### Configuration Utility

Use the `configure_resolution.py` utility for advanced configuration:

**List current settings:**
```bash
python configure_resolution.py list
```

**Enable globally for all streams:**
```bash
python configure_resolution.py enable --global
```

**Enable for specific user:**
```bash
python configure_resolution.py enable --user username
```

**Set check interval for specific user:**
```bash
python configure_resolution.py interval 5 --user username
```

**Test resolution detection:**
```bash
python configure_resolution.py test
python configure_resolution.py test https://example.com/stream.m3u8
```

## How It Works

1. **Resolution Monitoring**: The system uses ffprobe to periodically check the current resolution of the live stream
2. **Change Detection**: When a resolution change is detected, the system logs the change
3. **Auto-Restart**: If enabled for the user/room, the current recording stops gracefully and a new recording starts
4. **Seamless Transition**: The original recording is processed (converted to MP4, uploaded if configured) while the new recording begins

## Configuration File

Settings are stored in `src/config/user_settings.json`:

```json
{
  "default": {
    "restart_on_resolution_change": false,
    "resolution_check_interval": 5
  },
  "users": {
    "username1": {
      "restart_on_resolution_change": true,
      "resolution_check_interval": 3
    }
  },
  "rooms": {
    "12345": {
      "restart_on_resolution_change": true,
      "resolution_check_interval": 5
    }
  }
}
```

## Settings Hierarchy

The system checks settings in this order:
1. **User-specific settings** (if recording by username)
2. **Room-specific settings** (if recording by room ID)
3. **Global default settings**

## Performance Considerations

- **Check Interval**: Lower intervals (1-3 seconds) provide faster detection but use more CPU
- **Default Interval**: 5 seconds balances responsiveness with system resources
- **Network Impact**: Resolution checking has minimal network impact (only metadata is retrieved)

## Output File Naming

When auto-restart occurs, each recording session gets a unique timestamp:
```
TK_username_2024.01.15_14-30-25_flv.mp4  # First recording
TK_username_2024.01.15_14-35-10_flv.mp4  # After resolution change
```

## Logging

Resolution changes are logged with detailed information:
```
[INFO] Resolution change detected: 720x1280 → 1080x1920
[INFO] Auto-restart enabled. Stopping current recording to restart with new resolution.
[INFO] 🔄 AUTO-RESTART: Starting new recording with updated resolution...
```

## Troubleshooting

### ffprobe not found
```
❌ ffprobe is not available. Resolution change detection features disabled.
Install ffmpeg to enable resolution change detection.
```
**Solution**: Install ffmpeg and ensure it's in your system PATH.

### Resolution detection fails
```
❌ Could not detect resolution
```
**Possible causes**:
- Stream is not currently live
- Network connectivity issues
- Stream URL is invalid
- Stream format not supported by ffprobe

### Auto-restart not working
1. Check if feature is enabled: `python configure_resolution.py list`
2. Verify ffmpeg is installed: `python configure_resolution.py test`
3. Check logs for resolution change detection messages

## Examples

### Recording with auto-restart enabled
```bash
# Enable auto-restart for user and start recording
python main.py -user tiktoker123 -enable-resolution-restart user
python main.py -user tiktoker123 -mode automatic
```

### Multi-stream with different settings
```bash
# Configure different users with different settings
python configure_resolution.py enable --user streamer1
python configure_resolution.py interval 3 --user streamer1
python configure_resolution.py disable --user streamer2

# Start multi-stream recording
python main.py -users streamer1 streamer2 -mode automatic
```

### Testing before recording
```bash
# Test if resolution detection works
python configure_resolution.py test
python configure_resolution.py test https://live-stream-url.com/stream.m3u8

# Configure and test
python configure_resolution.py enable --user testuser
python main.py -user testuser -duration 60  # Test for 1 minute
```

## Best Practices

1. **Test First**: Use the test command to verify resolution detection works in your environment
2. **Appropriate Intervals**: Use 3-5 second intervals for most scenarios
3. **Per-User Configuration**: Configure settings per-user rather than globally for more control
4. **Monitor Logs**: Watch the logs during recording to see resolution changes being detected
5. **Storage Space**: Be aware that auto-restart will create multiple files per stream session

## Limitations

- Requires ffmpeg/ffprobe to be installed
- Small delay (check interval) between resolution change and restart
- Each restart creates a separate video file
- May not detect very brief resolution changes that occur between checks
