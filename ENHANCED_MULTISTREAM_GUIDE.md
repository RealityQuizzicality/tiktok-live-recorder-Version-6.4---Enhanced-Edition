# 🎯 Enhanced Multi-Stream Mode Guide

The multi-stream mode now features **dramatically improved visual output** with real-time dashboards, progress bars, and enhanced color coding.

## 🚀 Quick Start

### Automatic Mode (Recommended)
```bash
# Monitor multiple users automatically
python main.py -users user1 user2 user3 -mode automatic -automatic-interval 5

# Import usernames from a text file
python main.py -users-file usernames.txt -mode automatic -automatic-interval 5

# Combine command line users and file import
python main.py -users user1 user2 -users-file usernames.txt -mode automatic -automatic-interval 5

# Monitor multiple room IDs automatically  
python main.py -room-ids 123456 789012 345678 -mode automatic -automatic-interval 10

# Monitor with custom output directory
python main.py -users streamer1 streamer2 -mode automatic -automatic-interval 3 -output ./recordings/
```

### Manual Mode
```bash
# Record multiple users (must be live now)
python main.py -users user1 user2 user3 -mode manual

# Record multiple room IDs
python main.py -room-ids 123456 789012 -mode manual
```

## 🎨 Visual Features

### ✨ Enhanced Startup Display
- **Colorful banner** with TikTok branding
- **Stream overview** showing all targets
- **Mode confirmation** (AUTOMATIC/MANUAL)
- **Progress initialization** for each stream

### 📊 Real-Time Dashboard
- **Live progress bars** with TikTok pink theme
- **Status indicators** with emojis:
  - ⏳ Waiting for user to go live
  - 🔄 Starting recording
  - 🔴 Currently recording  
  - ✅ Recording completed
- **Duration tracking** in HH:MM:SS format
- **File size monitoring** in real-time
- **Stream identification** with color coding

### 📈 Final Summary Report
- **Completion statistics** (X/Y streams completed)
- **Total duration** and file size
- **Individual stream details**
- **Professional boxed layout**

## 🔄 Automatic Mode Benefits

### Continuous Monitoring
- Checks user status every X minutes (configurable)
- Automatically starts recording when users go live
- Handles users going offline gracefully
- Perfect for 24/7 monitoring

### Smart Status Updates
```
⏳ Waiting for user to go live
🔄 User went live! Starting recording...
🔴 Recording (with live progress)
✅ Recording completed (user went offline)
```

### Example Automatic Mode Session
```bash
python main.py -users tiktoker1 tiktoker2 tiktoker3 -mode automatic -automatic-interval 5
```

**What you'll see:**
1. Enhanced startup banner
2. Target stream list
3. Real-time dashboard showing:
   - Which users are being monitored
   - Current status of each user
   - Recording progress when live
   - File sizes and durations

## 🎛️ Dashboard Features

### Real-Time Updates
- **Progress bars** show recording progress
- **Duration counters** update every second
- **File size tracking** shows growing recordings
- **Status changes** reflect user activity

### Color Coding
- **TikTok Pink**: Progress bars and highlights
- **TikTok Blue**: Separators and borders
- **Cyan**: Stream names and identifiers
- **Green**: Success messages and completed status
- **Yellow**: Warnings and important info
- **Red**: Errors (if any occur)

## 📋 Status Indicators Explained

| Status | Meaning |
|--------|---------|
| ⏳ Waiting | Monitoring user, waiting for them to go live |
| 🔄 Starting | User went live, initializing recording |
| 🔴 Recording | Actively recording the live stream |
| ✅ Completed | Recording finished successfully |
| ⚠️ Warning | Minor issue (will retry automatically) |
| ❌ Error | Recording failed for this stream |

## 🛠️ Advanced Usage

### With Duration Limits
```bash
python main.py -users user1 user2 -mode automatic -duration 3600 -automatic-interval 5
```

### With Custom Intervals
```bash
# Check every 2 minutes (fast monitoring)
python main.py -users user1 user2 -mode automatic -automatic-interval 2

# Check every 15 minutes (conservative monitoring)
python main.py -users user1 user2 -mode automatic -automatic-interval 15
```

### Multiple Stream Types
```bash
# Mix users and room IDs (not recommended, but possible)
python main.py -users user1 user2 -room-ids 123456 -mode automatic
```

## 💡 Tips & Best Practices

### For Automatic Mode
1. **Use reasonable intervals**: 5-10 minutes is usually optimal
2. **Monitor disk space**: Multiple streams can generate large files
3. **Plan for peak times**: Popular streamers may go live simultaneously

### For Visual Experience
1. **Use a wide terminal**: Better dashboard display
2. **Dark terminal theme**: Colors show better on dark backgrounds
3. **Keep terminal open**: Dashboard updates in real-time

### For Performance
1. **Limit concurrent streams**: 3-5 streams work well on most systems
2. **Monitor network usage**: Multiple streams use significant bandwidth
3. **Use SSD storage**: Better performance for multiple file writes

## 🎭 Demo Scripts

### Try the Visual Demo
```bash
cd src/
python3 multi_stream_demo.py
```

### Try the Automatic Mode Demo
```bash
cd src/
python3 automatic_mode_example.py
```

## 🔧 Troubleshooting

### Dashboard Not Updating
- Ensure terminal supports ANSI escape codes
- Try using a different terminal application
- Check if terminal width is sufficient

### Colors Not Showing
- Terminal may not support colors
- Try updating your terminal application
- Use `export TERM=xterm-256color` if needed

### Performance Issues
- Reduce number of concurrent streams
- Increase automatic interval time
- Check available disk space and network bandwidth

---

## 🌟 Summary

The enhanced multi-stream mode provides:
- **Professional visual experience** with real-time dashboards
- **Automatic monitoring** of multiple streamers
- **Comprehensive progress tracking** with colored indicators
- **Smart status management** for each stream
- **Beautiful summary reports** when recording completes

Perfect for content creators, archivists, or anyone who needs to monitor multiple TikTok live streams simultaneously!
