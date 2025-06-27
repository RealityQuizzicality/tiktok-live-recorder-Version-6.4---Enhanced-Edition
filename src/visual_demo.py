#!/usr/bin/env python3
"""
Visual Demo Script for TikTok Live Recorder Enhanced Edition
Showcases the new visual features and progress indicators
"""

import time
import random
from utils.colors import Colors, VisualUtils
from utils.logger_manager import LoggerManager

def demo_colors():
    """Demonstrate color capabilities"""
    print(Colors.tiktok_theme("🎨 Color Demonstration", use_pink=True))
    print()
    
    # Basic colors
    print("Basic Colors:")
    print(f"  {Colors.red('Red Text')}")
    print(f"  {Colors.green('Green Text')}")
    print(f"  {Colors.blue('Blue Text')}")
    print(f"  {Colors.cyan('Cyan Text')}")
    print(f"  {Colors.yellow('Yellow Text')}")
    print(f"  {Colors.magenta('Magenta Text')}")
    print()
    
    # Theme colors
    print("Theme Colors:")
    print(f"  {Colors.success('✓ Success Message')}")
    print(f"  {Colors.warning('⚠ Warning Message')}")
    print(f"  {Colors.error('✗ Error Message')}")
    print(f"  {Colors.info('ℹ Info Message')}")
    print(f"  {Colors.highlight('★ Highlighted Text')}")
    print()
    
    # TikTok theme
    print("TikTok Brand Colors:")
    print(f"  {Colors.tiktok_theme('TikTok Pink', use_pink=True)}")
    print(f"  {Colors.tiktok_theme('TikTok Blue', use_pink=False)}")
    print()

def demo_visual_utils():
    """Demonstrate visual utilities"""
    print(Colors.tiktok_theme("📦 Visual Utilities Demo", use_pink=False))
    print()
    
    # Separator
    print("Separator Lines:")
    print(VisualUtils.create_separator(color=Colors.CYAN))
    print(VisualUtils.create_separator(char='═', color=Colors.MAGENTA))
    print(VisualUtils.create_separator(char='⚡', width=40, color=Colors.YELLOW))
    print()
    
    # Text box
    print("Text Boxes:")
    box_content = "This is a sample text box\nwith multiple lines\nand custom styling!"
    print(VisualUtils.create_box(box_content, padding=3, border_color=Colors.TIKTOK_PINK))
    print()
    
    # Progress bars
    print("Progress Bars:")
    for i in range(0, 101, 20):
        progress = VisualUtils.create_progress_bar(i, 100, width=30)
        colored_progress = Colors.tiktok_theme(progress, use_pink=True)
        print(f"  {colored_progress}")
        time.sleep(0.3)
    print()

def demo_logger_enhancements():
    """Demonstrate enhanced logger features"""
    print(Colors.tiktok_theme("📝 Enhanced Logger Demo", use_pink=True))
    print()
    
    logger = LoggerManager()
    
    # Status messages
    logger.print_status("Initializing system...", "INFO")
    time.sleep(0.5)
    logger.print_status("Loading configuration...", "INFO")
    time.sleep(0.5)
    logger.print_status("All systems ready!", "SUCCESS")
    time.sleep(0.5)
    logger.print_status("Minor issue detected", "WARNING")
    time.sleep(0.5)
    
    # Enhanced messages
    logger.success("Operation completed successfully!")
    logger.warning("This is a warning message")
    logger.info_enhanced("Enhanced info message")
    logger.highlight("Important highlighted message")
    logger.tiktok_style("TikTok styled message!", use_pink=True)
    
    print()
    
    # Box messages
    logger.print_box(
        "🎯 Recording Session\n\nUser: @example_user\nDuration: 30 minutes\nOutput: /recordings/",
        padding=2,
        border_color=Colors.SUCCESS
    )

def demo_progress_simulation():
    """Simulate recording progress"""
    print(Colors.tiktok_theme("🔴 Recording Progress Simulation", use_pink=True))
    print()
    
    logger = LoggerManager()
    logger.print_box(
        "🔴 Starting Recording Simulation\n\n📝 Output: demo_recording.mp4\n⏱️ Duration: 30 seconds",
        padding=2,
        border_color=Colors.SUCCESS
    )
    
    print()
    print(Colors.warning("Recording in progress... (simulated)"))
    
    duration = 30  # 30 second simulation
    start_time = time.time()
    
    for i in range(duration):
        current_time = time.time()
        elapsed = current_time - start_time
        file_size = (i + 1) * 0.5  # Simulate growing file size
        bitrate = random.randint(800, 1200)  # Random bitrate
        
        # Format time
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        seconds = int(elapsed % 60)
        duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        # Progress bar
        progress_bar = VisualUtils.create_progress_bar(i + 1, duration, width=25)
        
        # Status line
        status_line = (f"\r{Colors.tiktok_theme('🔴 RECORDING', use_pink=True)} "
                      f"{progress_bar} "
                      f"{Colors.info(duration_str)} "
                      f"| {Colors.success(f'{file_size:.1f} MB')} "
                      f"| {Colors.cyan(f'{bitrate} kbps')}")
        
        print(status_line, end='', flush=True)
        time.sleep(1)
    
    print("\n")
    logger.success("Recording completed!")
    
    # Final summary
    logger.print_box(
        "✓ Recording Complete!\n\n📁 File: demo_recording.mp4\n📊 Size: 15.0 MB\n⏱️ Duration: 00:00:30",
        padding=2,
        border_color=Colors.SUCCESS
    )

def main():
    """Run the visual demo"""
    # Enhanced banner
    from utils.utils import banner
    banner(enhanced=True, animated=False)
    
    print(Colors.tiktok_theme("🎭 Visual Features Demonstration", use_pink=True))
    print()
    
    # Demo sections
    demo_colors()
    time.sleep(1)
    
    demo_visual_utils()
    time.sleep(1)
    
    demo_logger_enhancements()
    time.sleep(1)
    
    demo_progress_simulation()
    
    print()
    print(Colors.tiktok_theme("✨ Demo Complete! ✨", use_pink=True))
    print(Colors.info("All enhanced visual features have been demonstrated."))

if __name__ == "__main__":
    main()
