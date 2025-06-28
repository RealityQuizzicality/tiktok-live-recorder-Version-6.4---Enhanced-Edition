#!/usr/bin/env python3
"""
Multi-Stream Recording Visual Demo
Demonstrates the enhanced visual output for multi-stream mode
"""

import time
import random
import threading
from utils.colors import Colors, VisualUtils
from utils.logger_manager import LoggerManager

class MultiStreamDemo:
    """
    Demonstration class for multi-stream visual enhancements
    """
    
    def __init__(self):
        self.stream_progress = {}
        self.demo_targets = [
            ("user1", "example_user_1"),
            ("user2", "tiktoker_live"),
            ("user3", "content_creator"),
            ("room", "12345678")
        ]
        
    def run_demo(self):
        """Run the multi-stream visual demo"""
        logger_manager = LoggerManager()
        
        # Enhanced startup banner
        logger_manager.print_separator(color=Colors.TIKTOK_BLUE)
        
        banner_content = f"🎯 Multi-Stream Recording Setup\n\nTotal Streams: {len(self.demo_targets)}\nMode: AUTOMATIC | Duration: Unlimited"
        
        logger_manager.print_box(
            banner_content,
            padding=2,
            border_color=Colors.TIKTOK_PINK
        )
        
        # Show target list
        target_info = []
        for i, (stream_type, name) in enumerate(self.demo_targets):
            if stream_type == "user":
                target_info.append(f"Stream {i+1}: {Colors.cyan(f'@{name}')}")
            else:
                target_info.append(f"Stream {i+1}: {Colors.cyan(f'Room {name}')}")
        
        logger_manager.print_box(
            "📋 Target Streams:\n\n" + "\n".join(target_info),
            padding=2,
            border_color=Colors.INFO
        )
        
        logger_manager.print_separator(color=Colors.TIKTOK_BLUE)
        
        # Initialize progress tracking
        for i, (stream_type, name) in enumerate(self.demo_targets):
            stream_key = f"Stream-{i+1}"
            display_name = f"@{name}" if stream_type == "user" else f"Room {name}"
            self.stream_progress[stream_key] = {
                'name': display_name,
                'progress': 0,
                'duration': 0,
                'file_size': 0.0,
                'status': '⏳ Waiting'
            }
        
        # Display initial dashboard
        self._display_progress_dashboard()
        
        # Simulate recording progress
        self._simulate_recording()
        
        # Final summary
        self._display_final_summary()
        
    def _simulate_recording(self):
        """Simulate the recording process with progress updates"""
        logger_manager = LoggerManager()
        
        # Start each stream with a delay
        for i, (stream_type, name) in enumerate(self.demo_targets):
            stream_key = f"Stream-{i+1}"
            
            # Update to starting status
            self.stream_progress[stream_key]['status'] = '🔄 Starting'
            self._display_progress_dashboard()
            
            logger_manager.success(f"Started recording thread: {stream_key}")
            time.sleep(1)
            
            # Update to recording status
            self.stream_progress[stream_key]['status'] = '🔴 Recording'
            self._display_progress_dashboard()
            time.sleep(0.5)
        
        print("\n" + Colors.warning("Recording in progress... (demo simulation)"))
        time.sleep(2)
        
        # Simulate recording progress over 30 seconds
        duration = 30
        start_time = time.time()
        
        for second in range(duration):
            current_time = time.time()
            elapsed = current_time - start_time
            
            # Update each stream's progress
            for i, stream_key in enumerate(self.stream_progress.keys()):
                # Simulate different recording speeds
                stream_elapsed = elapsed + (i * 2)  # Stagger start times
                file_size = stream_elapsed * random.uniform(0.8, 1.2)  # MB/second
                progress = min(100, int((stream_elapsed / duration) * 100))
                
                self.stream_progress[stream_key].update({
                    'duration': int(stream_elapsed),
                    'file_size': file_size,
                    'progress': progress
                })
                
                # Some streams might finish early
                if progress >= 95 and random.random() < 0.1:
                    self.stream_progress[stream_key]['status'] = '✅ Completed'
            
            # Update dashboard every few seconds
            if second % 3 == 0:
                self._display_progress_dashboard()
            
            time.sleep(1)
        
        # Mark remaining streams as completed
        for stream_key in self.stream_progress.keys():
            if '✅' not in self.stream_progress[stream_key]['status']:
                self.stream_progress[stream_key]['status'] = '✅ Completed'
        
        self._display_progress_dashboard()
        print("\n")
        logger_manager.success("All recordings completed!")
        
    def _display_progress_dashboard(self):
        """Display the real-time progress dashboard"""
        print("\033[H\033[J", end='')  # Clear screen and move cursor to top
        
        logger_manager = LoggerManager()
        logger_manager.print_separator(color=Colors.TIKTOK_BLUE)
        
        # Dashboard header
        header = f"📊 {Colors.tiktok_theme('Multi-Stream Recording Dashboard', use_pink=True)}"
        print(VisualUtils.center_text(header))
        print()
        
        # Stream status table
        for stream_key, progress_data in self.stream_progress.items():
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
        print(f"  {Colors.info('ℹ️  Press Ctrl+C to stop all recordings')}", end='\r')
        
    def _display_final_summary(self):
        """Display final recording summary"""
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
            f"📈 Recording Session Summary\n\n"
            f"Completed Streams: {Colors.success(str(completed_streams))} / {len(self.stream_progress)}\n"
            f"Total Duration: {Colors.info(total_duration_str)}\n"
            f"Total File Size: {Colors.highlight(f'{total_size:.1f} MB')}\n\n"
            f"Stream Details:\n"
        )
        
        for stream_key, data in self.stream_progress.items():
            duration = data['duration']
            hours = duration // 3600
            minutes = (duration % 3600) // 60
            seconds = duration % 60
            duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            
            summary_content += (
                f"  • {Colors.cyan(stream_key)}: {data['status']} "
                f"({duration_str}, {data['file_size']:.1f} MB)\n"
            )
        
        logger_manager.print_box(
            summary_content,
            padding=2,
            border_color=Colors.SUCCESS
        )
        
        print()
        print(Colors.tiktok_theme("✨ Multi-Stream Recording Complete! ✨", use_pink=True))

def main():
    """Run the multi-stream demo"""
    print(Colors.tiktok_theme("🎭 Multi-Stream Visual Enhancement Demo", use_pink=True))
    print()
    
    demo = MultiStreamDemo()
    demo.run_demo()
    
    print()
    print(Colors.info("Demo complete! This showcases the enhanced visual output for multi-stream mode."))

if __name__ == "__main__":
    main()
