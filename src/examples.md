# TikTok Live Recorder - Multi-Stream Examples

This document provides examples of how to use the new multi-stream recording feature.

## Single Stream (Original Functionality)

### Record by username:
```bash
python3 main.py -user username -mode manual
```

### Record by URL:
```bash
python3 main.py -url "https://www.tiktok.com/@username/live" -mode manual
```

### Record by room ID:
```bash
python3 main.py -room_id 1234567890 -mode manual
```

## Multi-Stream Recording

### Record multiple users simultaneously:
```bash
# Manual mode - record if they are currently live
python3 main.py -users user1 user2 user3 -mode manual

# Automatic mode - wait for them to go live and record automatically
python3 main.py -users user1 user2 user3 -mode automatic -automatic_interval 2

# Import usernames from a text file
python3 main.py -users-file usernames.txt -mode automatic

# Combine command line users and file import
python3 main.py -users user1 user2 -users-file usernames.txt -mode automatic
```

### Record multiple URLs simultaneously:
```bash
python3 main.py -urls "https://www.tiktok.com/@user1/live" "https://www.tiktok.com/@user2/live" -mode manual
```

### Record multiple room IDs simultaneously:
```bash
python3 main.py -room_ids 1234567890 0987654321 1122334455 -mode automatic
```

## Advanced Examples

### Multi-stream with custom output directory:
```bash
python3 main.py -users user1 user2 user3 -mode automatic -output "/path/to/recordings/"
```

### Multi-stream with duration limit:
```bash
python3 main.py -users user1 user2 user3 -mode manual -duration 3600
```

### Multi-stream with Telegram upload:
```bash
python3 main.py -users user1 user2 user3 -mode automatic -telegram
```

### Multi-stream with proxy:
```bash
python3 main.py -users user1 user2 user3 -mode automatic -proxy "http://127.0.0.1:8080"
```

## Key Features

1. **Simultaneous Recording**: All streams are recorded at the same time using separate threads
2. **Unique Filenames**: Each recording gets a unique filename with thread identifier
3. **Individual Logging**: Each stream's activity is logged with a thread identifier for easy tracking
4. **Graceful Shutdown**: Press Ctrl+C once to stop all recordings cleanly
5. **Thread Safety**: All operations are thread-safe to prevent conflicts

## Output Files

Recordings are now organized in user-specific folders. When recording multiple streams, the structure looks like:

```
recordings/
├── user1/
│   └── TK_user1_2024.06.24_18-30-00_Stream-1-user1_flv.mp4
├── user2/
│   └── TK_user2_2024.06.24_18-30-00_Stream-2-user2_flv.mp4
└── user3/
    └── TK_user3_2024.06.24_18-30-00_Stream-3-user3_flv.mp4
```

For single stream recordings:
```
recordings/
└── username/
    └── TK_username_2024.06.24_18-30-00_flv.mp4
```

## Important Notes

- You cannot mix single-stream and multi-stream arguments in the same command
- All streams use the same configuration (proxy, output directory, duration, etc.)
- Each stream runs independently, so if one fails, others continue recording
- In automatic mode, each stream checks for live status at its own interval
