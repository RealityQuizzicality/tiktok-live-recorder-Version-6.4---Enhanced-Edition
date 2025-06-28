#!/usr/bin/env python3
"""
Grid Layout Demo for Multi-Stream Recording
Demonstrates the new horizontal grid layout for monitoring many streams (like 20 users)
"""

import time
import random
from utils.colors import Colors, VisualUtils
from utils.logger_manager import LoggerManager

class GridLayoutDemo:
    """
    Demonstration class for the new grid layout feature
    """
    
    def __init__(self, num_streams=20):
        self.num_streams = num_streams
        self.stream_progress = {}
        
        # Generate demo usernames
        demo_users = [
            "tiktoker1", "dancer_pro", "gamer_live", "cook_master", "artist_23",
            "music_vid", "comedy_king", "sports_fan", "travel_vlog", "tech_guru",
            "fashion_style", "pet_lover", "fitness_coach", "book_reader", "car_enthusiast",
            "food_blogger", "nature_lover", "movie_buff", "craft_maker", "science_geek",
            "beauty_tips", "diy_creator", "news_today", "history_facts", "language_learn"
        ]
        
        self.demo_targets = [(f"user{i+1}", demo_users[i % len(demo_users)]) 
                            for i in range(num_streams)]
        
    def run_demo(self):
        """Run the grid layout demo"""
        logger_manager = LoggerManager()
        
        print(Colors.tiktok_theme(f"🎯 Grid Layout Demo - {self.num_streams} Streams", use_pink=True))
        print(Colors.info(f"Demonstrating horizontal grid layout for monitoring many streams"))
        print()
        
        # Enhanced startup banner
        logger_manager.print_separator(color=Colors.TIKTOK_BLUE)
        
        banner_content = f"🎯 Multi-Stream Recording Setup\n\nTotal Streams: {self.num_streams}\nMode: AUTOMATIC | Layout: GRID"
        
        logger_manager.print_box(
            banner_content,
            padding=2,
            border_color=Colors.TIKTOK_PINK
        )
        
        print(Colors.info(f"With {self.num_streams} streams, the system will automatically use grid layout"))
        print()
        
        # Initialize progress tracking for many streams
        for i, (stream_type, name) in enumerate(self.demo_targets):
            stream_key = f"Stream-{i+1}"
            self.stream_progress[stream_key] = {
                'name': f"@{name}",
                'progress': 0,
                'duration': 0,
                'file_size': 0.0,
                'status': '⏳ Waiting'
            }
        
        # Show comparison between layouts
        self._show_layout_comparison()
        
        # Simulate the recording process
        self._simulate_grid_recording()
        
        # Final summary
        self._display_final_summary()
        
    def _show_layout_comparison(self):
        """Show the difference between vertical and grid layouts"""
        print(Colors.highlight("📊 Layout Comparison:"))
        print()
        
        print(Colors.cyan("🔹 Vertical Layout (≤6 streams):"))
        print("  Perfect for small numbers of streams")
        print("  Shows detailed information for each stream")
        print("  Full-width progress bars")
        print()
        
        print(Colors.cyan("🔹 Grid Layout (>6 streams):"))
        print("  Efficient for monitoring many streams")
        print("  Compact view with essential information")
        print("  2-4 columns based on terminal width")
        print("  Status emojis for quick recognition")
        print()
        
        try:
            input(Colors.warning("Press Enter to see the grid layout in action..."))
        except EOFError:
            # Handle piped input by just continuing
            pass
        print()
        
    def _simulate_grid_recording(self):
        """Simulate recording with grid layout updates"""
        print(Colors.warning("Simulating multi-stream recording with grid layout..."))
        time.sleep(2)
        
        # Display initial grid
        self._display_grid_dashboard()
        time.sleep(2)
        
        # Simulate streams starting at different times
        start_indices = list(range(len(self.demo_targets)))
        random.shuffle(start_indices)
        
        # Start some streams
        for i in range(0, min(8, len(start_indices))):  # Start first 8 streams
            stream_idx = start_indices[i]
            stream_key = f"Stream-{stream_idx+1}"
            
            # Update to starting status
            self.stream_progress[stream_key]['status'] = '🔄 Starting'
            self._display_grid_dashboard()
            time.sleep(0.5)
            
            # Update to recording status
            self.stream_progress[stream_key]['status'] = '🔴 Recording'
            self._display_grid_dashboard()
            time.sleep(0.3)
        
        # Simulate recording progress
        for second in range(30):  # 30 second simulation
            # Update progress for recording streams
            for stream_key, data in self.stream_progress.items():
                if '🔴' in data['status']:
                    data['duration'] += 1
                    data['file_size'] += random.uniform(0.8, 1.5)
                    data['progress'] = min(100, int((data['duration'] / 60) * 100))  # Progress based on time
                    
                    # Some streams might finish
                    if data['duration'] > 25 and random.random() < 0.05:
                        data['status'] = '✅ Completed'
            
            # Occasionally start new streams
            if second % 8 == 0 and second < 24:
                remaining_waiting = [k for k, v in self.stream_progress.items() if '⏳' in v['status']]
                if remaining_waiting:
                    new_stream = random.choice(remaining_waiting)
                    self.stream_progress[new_stream]['status'] = '🔄 Starting'
                    time.sleep(0.5)
                    self.stream_progress[new_stream]['status'] = '🔴 Recording'
            
            # Update dashboard every few seconds
            if second % 3 == 0:
                self._display_grid_dashboard()
            
            time.sleep(1)
        
        # Complete remaining streams
        for stream_key, data in self.stream_progress.items():
            if '🔴' in data['status']:
                data['status'] = '✅ Completed'
        
        self._display_grid_dashboard()
        print()
        print(Colors.success("🎉 Grid layout simulation complete!"))
        
    def _display_grid_dashboard(self):
        """Display the grid dashboard (adapted from MultiStreamRecorder)"""
        print("\033[H\033[J", end='')  # Clear screen
        
        logger_manager = LoggerManager()
        logger_manager.print_separator(color=Colors.TIKTOK_BLUE)
        
        # Dashboard header
        header = f"📊 {Colors.tiktok_theme('Multi-Stream Grid Layout Dashboard', use_pink=True)}"
        print(VisualUtils.center_text(header))
        print()
        
        # Display grid layout
        terminal_width = VisualUtils.get_terminal_width()
        
        # Calculate optimal column width and number of columns
        min_column_width = 35
        max_columns = min(4, terminal_width // min_column_width)
        columns_per_row = max(2, max_columns)
        
        # Group streams into rows
        stream_items = list(self.stream_progress.items())
        rows = [stream_items[i:i + columns_per_row] for i in range(0, len(stream_items), columns_per_row)]
        
        for row in rows:
            # Create the display for each stream in this row
            stream_displays = []
            
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
                
                # Create compact display for this stream
                stream_display = (
                    f"{Colors.cyan(stream_key)} {status_emoji}\n"
                    f"{Colors.highlight(name[:15])}\n"
                    f"{Colors.info(duration_str)} {Colors.success(f'{file_size:.1f}MB')}\n"
                    f"{Colors.tiktok_theme(progress_bar, use_pink=True)}"
                )
                
                stream_displays.append(stream_display.split('\n'))
            
            # Print the row with proper alignment
            max_lines = max(len(display) for display in stream_displays)
            
            for line_idx in range(max_lines):
                line_parts = []
                for display in stream_displays:
                    if line_idx < len(display):
                        # Simple padding for demo
                        padded_text = display[line_idx].ljust(min_column_width)
                        line_parts.append(padded_text)
                    else:
                        line_parts.append(' ' * min_column_width)
                
                print('  ' + '  '.join(line_parts))
            
            print()  # Empty line between rows
        
        logger_manager.print_separator(color=Colors.TIKTOK_BLUE)
        
        # Show summary stats
        total_streams = len(self.stream_progress)
        active_streams = sum(1 for data in self.stream_progress.values() if '🔴' in data['status'])
        completed_streams = sum(1 for data in self.stream_progress.values() if '✅' in data['status'])
        waiting_streams = sum(1 for data in self.stream_progress.values() if '⏳' in data['status'])
        
        status_info = f"📊 Total: {total_streams} | 🔴 Active: {active_streams} | ✅ Completed: {completed_streams} | ⏳ Waiting: {waiting_streams}"
        print(f"  {Colors.info(status_info)}")
        print(f"  {Colors.info('ℹ️  Grid layout automatically used for >6 streams')}", end='\r')
        
    def _display_final_summary(self):
        """Display final summary with grid layout benefits"""
        logger_manager = LoggerManager()
        
        # Calculate totals
        total_duration = sum(data['duration'] for data in self.stream_progress.values())
        total_size = sum(data['file_size'] for data in self.stream_progress.values())
        completed_streams = sum(1 for data in self.stream_progress.values() if '✅' in data['status'])
        
        # Format total duration
        hours = total_duration // 3600
        minutes = (total_duration % 3600) // 60
        seconds = total_duration % 60
        total_duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        summary_content = (
            f"📈 Grid Layout Demo Summary\n\n"
            f"Streams Monitored: {Colors.success(str(len(self.stream_progress)))}\n"
            f"Completed Streams: {Colors.success(str(completed_streams))}\n"
            f"Total Duration: {Colors.info(total_duration_str)}\n"
            f"Total File Size: {Colors.highlight(f'{total_size:.1f} MB')}\n\n"
            f"Grid Layout Benefits:\n"
            f"✅ Efficient space usage\n"
            f"✅ Clear status indicators\n"
            f"✅ Scalable to many streams\n"
            f"✅ Quick visual overview"
        )
        
        logger_manager.print_box(
            summary_content,
            padding=2,
            border_color=Colors.SUCCESS
        )
        
        print()
        print(Colors.tiktok_theme("✨ Perfect for monitoring 20+ streams! ✨", use_pink=True))

def main():
    """Run the grid layout demo"""
    print(Colors.tiktok_theme("🎭 Multi-Stream Grid Layout Demo", use_pink=True))
    print()
    
    # Ask user for number of streams to demo
    try:
        num_streams = input(Colors.cyan("Enter number of streams to demo (default 20): ")).strip()
        num_streams = int(num_streams) if num_streams else 20
        num_streams = min(max(num_streams, 7), 50)  # Between 7-50 streams
    except ValueError:
        num_streams = 20
    
    print(f"Demonstrating grid layout with {Colors.highlight(str(num_streams))} streams")
    print()
    
    demo = GridLayoutDemo(num_streams)
    demo.run_demo()
    
    print()
    print(Colors.info("Demo complete! This shows how the grid layout handles many streams efficiently."))

if __name__ == "__main__":
    main()
