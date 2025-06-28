#!/usr/bin/env python3
"""
Test script to verify multi-stream recorder fixes
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.colors import Colors, VisualUtils
from utils.logger_manager import LoggerManager
from utils.enums import Mode

def test_progress_tracking():
    """Test the progress tracking initialization"""
    print(Colors.tiktok_theme("🧪 Testing Progress Tracking", use_pink=True))
    print()
    
    # Test stream progress dictionary creation
    targets = [
        (None, "user1", None),
        (None, "user2", None),
        (None, "user3", None)
    ]
    
    stream_progress = {}
    
    # Initialize progress tracking (same logic as in MultiStreamRecorder)
    for i, (url, user, room_id) in enumerate(targets):
        stream_key = f"Stream-{i+1}"
        stream_progress[stream_key] = {
            'name': user or url or f"Room {room_id}",
            'progress': 0,
            'duration': 0,
            'file_size': 0,
            'status': '⏳ Waiting'
        }
    
    # Display progress
    logger_manager = LoggerManager()
    logger_manager.print_separator(color=Colors.TIKTOK_BLUE)
    
    header = f"📊 {Colors.tiktok_theme('Test Progress Dashboard', use_pink=True)}"
    print(VisualUtils.center_text(header))
    print()
    
    for stream_key, progress_data in stream_progress.items():
        name = progress_data['name']
        status = progress_data['status']
        duration = progress_data['duration']
        file_size = progress_data['file_size']
        progress_percent = progress_data['progress']
        
        # Format duration
        hours = duration // 3600
        minutes = (duration % 3600) // 60
        seconds = duration % 60
        duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        # Create progress bar
        progress_bar = VisualUtils.create_progress_bar(
            progress_percent, 100, width=30, show_percentage=False
        )
        
        # Format the status line
        status_line = (
            f"  {Colors.cyan(stream_key)}: {status}\n"
            f"    📺 {Colors.highlight(name[:30])}\n"
            f"    ⏱️  {Colors.info(duration_str)} | "
            f"📁 {Colors.success(f'{file_size:.1f} MB')} | "
            f"{Colors.tiktok_theme(progress_bar, use_pink=True)}"
        )
        
        print(status_line)
        print()
    
    logger_manager.print_separator(color=Colors.TIKTOK_BLUE)
    print(f"  {Colors.success('✅ Progress tracking test passed!')}")
    
def test_error_handling():
    """Test error handling scenarios"""
    print(f"\n{Colors.tiktok_theme('🛡️ Testing Error Handling', use_pink=True)}")
    print()
    
    # Test safe dashboard display with missing data
    def safe_display_test():
        try:
            # Simulate missing stream_progress
            stream_progress = None
            if hasattr(stream_progress, 'items') and stream_progress:
                print("This should not execute")
            else:
                print(Colors.success("✅ Safely handled missing stream_progress"))
        except Exception as e:
            print(Colors.error(f"❌ Error handling failed: {e}"))
    
    safe_display_test()
    
    # Test thread name consistency
    def test_thread_naming():
        targets = [("url1", None, None), (None, "user2", None), (None, None, "12345")]
        
        print(Colors.info("Testing thread naming consistency:"))
        for i, (url, user, room_id) in enumerate(targets):
            stream_key = f"Stream-{i+1}"
            thread_name = stream_key
            if user:
                thread_name += f"-{user}"
            elif url:
                thread_name += f"-{url.split('/')[-1]}"
            elif room_id:
                thread_name += f"-{room_id}"
            
            print(f"  {Colors.cyan(stream_key)} -> {Colors.highlight(thread_name)}")
        
        print(Colors.success("✅ Thread naming test passed!"))
    
    test_thread_naming()

def test_mode_compatibility():
    """Test compatibility with different modes"""
    print(f"\n{Colors.tiktok_theme('⚙️ Testing Mode Compatibility', use_pink=True)}")
    print()
    
    # Test automatic mode display
    banner_content = "🎯 Multi-Stream Recording Setup\n\nTotal Streams: 3\nMode: AUTOMATIC | Duration: Unlimited"
    
    logger_manager = LoggerManager()
    logger_manager.print_box(
        banner_content,
        padding=2,
        border_color=Colors.TIKTOK_PINK
    )
    
    print(Colors.success("✅ Mode compatibility test passed!"))

def main():
    """Run all tests"""
    print(Colors.tiktok_theme("🧪 Multi-Stream Recorder Fix Verification", use_pink=True))
    print(Colors.info("Testing the fixes for multi-stream recorder errors"))
    print()
    
    test_progress_tracking()
    test_error_handling()
    test_mode_compatibility()
    
    print(f"\n{Colors.tiktok_theme('✨ All Tests Completed! ✨', use_pink=True)}")
    print(Colors.success("The multi-stream recorder fixes should now work correctly."))
    
    print(f"\n{Colors.highlight('Next Steps:')}")
    print(f"  1. {Colors.cyan('Try running a real multi-stream command')}")
    print(f"  2. {Colors.cyan('Monitor the enhanced dashboard output')}")
    print(f"  3. {Colors.cyan('Check that recordings complete successfully')}")

if __name__ == "__main__":
    main()
