#!/usr/bin/env python3
"""
Quick test of the new grid layout for multi-stream recording
"""

from utils.colors import Colors, VisualUtils
from utils.logger_manager import LoggerManager

def test_grid_layout():
    """Test the grid layout with 20 streams"""
    logger_manager = LoggerManager()
    
    print(Colors.tiktok_theme("🎯 Grid Layout Test - 20 Streams", use_pink=True))
    print()
    
    # Create test data for 20 streams
    stream_progress = {}
    for i in range(20):
        stream_key = f"Stream-{i+1}"
        stream_progress[stream_key] = {
            'name': f"@user{i+1}",
            'progress': (i * 5) % 100,  # Varied progress
            'duration': i * 45,  # Varied durations
            'file_size': i * 2.3,  # Varied file sizes
            'status': ['⏳ Waiting', '🔄 Starting', '🔴 Recording', '✅ Completed'][i % 4]
        }
    
    # Display grid layout
    logger_manager.print_separator(color=Colors.TIKTOK_BLUE)
    header = f"📊 {Colors.tiktok_theme('Multi-Stream Grid Layout Dashboard', use_pink=True)}"
    print(VisualUtils.center_text(header))
    print()
    
    # Grid layout logic
    terminal_width = VisualUtils.get_terminal_width()
    min_column_width = 35
    max_columns = min(4, terminal_width // min_column_width)
    columns_per_row = max(2, max_columns)
    
    print(f"Terminal width: {terminal_width}, Using {columns_per_row} columns")
    print()
    
    # Group streams into rows
    stream_items = list(stream_progress.items())
    rows = [stream_items[i:i + columns_per_row] for i in range(0, len(stream_items), columns_per_row)]
    
    for row_idx, row in enumerate(rows):
        print(f"Row {row_idx + 1}:")
        
        # Create compact displays
        for stream_key, progress_data in row:
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
            
            # Create compact progress bar
            progress_bar = VisualUtils.create_progress_bar(
                progress_percent, 100, width=20, show_percentage=False
            )
            
            # Get status emoji
            status_emoji = '⏳'
            if '🔄' in status:
                status_emoji = '🔄'
            elif '🔴' in status:
                status_emoji = '🔴'
            elif '✅' in status:
                status_emoji = '✅'
            
            # Create compact display
            stream_info = (
                f"  {Colors.cyan(stream_key)} {status_emoji} | "
                f"{Colors.highlight(name[:15])} | "
                f"{Colors.info(duration_str)} | "
                f"{Colors.success(f'{file_size:.1f}MB')} | "
                f"{Colors.tiktok_theme(progress_bar, use_pink=True)}"
            )
            
            print(stream_info)
        
        print()  # Empty line between rows
    
    logger_manager.print_separator(color=Colors.TIKTOK_BLUE)
    
    # Show summary stats
    total_streams = len(stream_progress)
    active_streams = sum(1 for data in stream_progress.values() if '🔴' in data['status'])
    completed_streams = sum(1 for data in stream_progress.values() if '✅' in data['status'])
    waiting_streams = sum(1 for data in stream_progress.values() if '⏳' in data['status'])
    
    status_info = f"📊 Total: {total_streams} | 🔴 Active: {active_streams} | ✅ Completed: {completed_streams} | ⏳ Waiting: {waiting_streams}"
    print(f"  {Colors.info(status_info)}")
    
    print()
    print(Colors.success("✅ Grid layout test complete!"))
    print(Colors.info("This layout automatically activates when monitoring >6 streams"))

if __name__ == "__main__":
    test_grid_layout()
