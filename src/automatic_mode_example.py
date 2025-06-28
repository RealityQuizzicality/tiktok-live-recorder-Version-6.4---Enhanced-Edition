#!/usr/bin/env python3
"""
Example: Enhanced Multi-Stream Recording with Automatic Mode
Shows how the visual enhancements work with automatic mode (-mode automatic)
"""

import time
import random
from utils.colors import Colors, VisualUtils
from utils.logger_manager import LoggerManager

def demonstrate_automatic_mode():
    """
    Demonstrate how the enhanced visuals work with automatic mode
    """
    logger_manager = LoggerManager()
    
    print(Colors.tiktok_theme("🎭 Enhanced Multi-Stream with Automatic Mode Demo", use_pink=True))
    print()
    
    # Show typical automatic mode command
    print(Colors.highlight("Example Command:"))
    print(Colors.cyan("python main.py -users user1 user2 user3 -mode automatic -automatic-interval 5"))
    print()
    
    # Enhanced startup display
    logger_manager.print_separator(color=Colors.TIKTOK_BLUE)
    
    banner_content = "🎯 Multi-Stream Recording Setup\n\nTotal Streams: 3\nMode: AUTOMATIC | Interval: 5 minutes"
    
    logger_manager.print_box(
        banner_content,
        padding=2,
        border_color=Colors.TIKTOK_PINK
    )
    
    # Show target list
    target_info = [
        f"Stream 1: {Colors.cyan('@user1')}",
        f"Stream 2: {Colors.cyan('@user2')}",
        f"Stream 3: {Colors.cyan('@user3')}"
    ]
    
    logger_manager.print_box(
        "📋 Target Streams:\n\n" + "\n".join(target_info),
        padding=2,
        border_color=Colors.INFO
    )
    
    logger_manager.print_separator(color=Colors.TIKTOK_BLUE)
    
    # Simulate automatic mode behavior
    stream_progress = {
        'Stream-1': {
            'name': '@user1',
            'progress': 0,
            'duration': 0,
            'file_size': 0.0,
            'status': '⏳ Waiting for user to go live'
        },
        'Stream-2': {
            'name': '@user2', 
            'progress': 0,
            'duration': 0,
            'file_size': 0.0,
            'status': '⏳ Waiting for user to go live'
        },
        'Stream-3': {
            'name': '@user3',
            'progress': 0,
            'duration': 0,
            'file_size': 0.0,
            'status': '⏳ Waiting for user to go live'
        }
    }
    
    def display_dashboard():
        """Display the progress dashboard"""
        print("\033[H\033[J", end='')  # Clear screen
        
        logger_manager.print_separator(color=Colors.TIKTOK_BLUE)
        header = f"📊 {Colors.tiktok_theme('Multi-Stream Recording Dashboard (AUTOMATIC MODE)', use_pink=True)}"
        print(VisualUtils.center_text(header))
        print()
        
        for stream_key, data in stream_progress.items():
            name = data['name']
            status = data['status']
            duration = data['duration']
            file_size = data['file_size']
            progress_percent = data['progress']
            
            # Format duration
            hours = duration // 3600
            minutes = (duration % 3600) // 60
            seconds = duration % 60
            duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            
            # Create progress bar
            progress_bar = VisualUtils.create_progress_bar(
                progress_percent, 100, width=30, show_percentage=False
            )
            
            status_line = (
                f"  {Colors.cyan(stream_key)}: {status}\n"
                f"    📺 {Colors.highlight(name)}\n"
                f"    ⏱️  {Colors.info(duration_str)} | "
                f"📁 {Colors.success(f'{file_size:.1f} MB')} | "
                f"{Colors.tiktok_theme(progress_bar, use_pink=True)}"
            )
            
            print(status_line)
            print()
        
        logger_manager.print_separator(color=Colors.TIKTOK_BLUE)
        print(f"  {Colors.info('ℹ️  Automatic mode: Checking every 5 minutes | Press Ctrl+C to stop')}", end='\r')
    
    # Initial display
    display_dashboard()
    time.sleep(2)
    
    # Simulate automatic mode behavior
    print(Colors.warning("\nSimulating automatic mode behavior..."))
    print(Colors.info("Checking if users are live..."))
    time.sleep(2)
    
    # User 1 goes live first
    stream_progress['Stream-1']['status'] = '🔄 User went live! Starting recording...'
    display_dashboard()
    time.sleep(1)
    
    stream_progress['Stream-1']['status'] = '🔴 Recording'
    display_dashboard()
    time.sleep(2)
    
    # User 2 goes live
    stream_progress['Stream-2']['status'] = '🔄 User went live! Starting recording...'
    display_dashboard()
    time.sleep(1)
    
    stream_progress['Stream-2']['status'] = '🔴 Recording'
    display_dashboard()
    time.sleep(2)
    
    # Simulate recording progress
    for i in range(10):
        for stream_key in ['Stream-1', 'Stream-2']:
            if '🔴' in stream_progress[stream_key]['status']:
                stream_progress[stream_key]['duration'] += 1
                stream_progress[stream_key]['file_size'] += random.uniform(0.8, 1.2)
                stream_progress[stream_key]['progress'] = min(100, (i + 1) * 10)
        
        # User 3 still waiting
        if i == 5:
            stream_progress['Stream-3']['status'] = '⏳ Still waiting... (next check in 3 min)'
        
        display_dashboard()
        time.sleep(1)
    
    # User 1 goes offline
    stream_progress['Stream-1']['status'] = '✅ Recording completed (user went offline)'
    display_dashboard()
    time.sleep(2)
    
    # User 3 finally goes live
    stream_progress['Stream-3']['status'] = '🔄 User went live! Starting recording...'
    display_dashboard()
    time.sleep(1)
    
    stream_progress['Stream-3']['status'] = '🔴 Recording'
    display_dashboard()
    time.sleep(2)
    
    # Continue for a bit more
    for i in range(5):
        for stream_key in ['Stream-2', 'Stream-3']:
            if '🔴' in stream_progress[stream_key]['status']:
                stream_progress[stream_key]['duration'] += 1
                stream_progress[stream_key]['file_size'] += random.uniform(0.8, 1.2)
        
        display_dashboard()
        time.sleep(1)
    
    # All complete
    stream_progress['Stream-2']['status'] = '✅ Recording completed'
    stream_progress['Stream-3']['status'] = '✅ Recording completed'
    display_dashboard()
    
    print("\n\n")
    logger_manager.success("Demo complete! This shows how automatic mode works with enhanced visuals.")
    
    # Show key features
    print(Colors.highlight("\n🌟 Key Features in Automatic Mode:"))
    features = [
        "🔄 Continuously monitors users for live status",
        "⏰ Checks at specified intervals (5 minutes in this example)",
        "🎯 Automatically starts recording when users go live",
        "📊 Real-time dashboard shows waiting/recording status",
        "✨ Enhanced visual feedback for all operations",
        "🛑 Graceful handling of users going offline"
    ]
    
    for feature in features:
        print(f"  {feature}")
    
    print(f"\n{Colors.tiktok_theme('Perfect for monitoring multiple streamers 24/7!', use_pink=True)}")

if __name__ == "__main__":
    demonstrate_automatic_mode()
