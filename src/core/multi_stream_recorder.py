import os
import threading
import time
from typing import List, Tuple, Optional

from core.tiktok_recorder import TikTokRecorder
from utils.logger_manager import logger, LoggerManager
from utils.colors import Colors, VisualUtils
from utils.custom_exceptions import LiveNotFound, UserLiveException, TikTokException
from utils.enums import Mode
from utils.config_manager import ConfigManager
from utils.resolution_detector import ResolutionDetector


class MultiStreamRecorder:
    """
    Handles recording multiple TikTok live streams simultaneously using threading.
    """

    def __init__(
        self,
        targets: List[Tuple[Optional[str], Optional[str], Optional[str]]],  # (url, user, room_id) tuples
        mode: Mode,
        automatic_interval: int,
        cookies: dict,
        proxy: Optional[str],
        output: Optional[str],
        duration: Optional[int],
        use_telegram: bool,
    ):
        """
        Initialize the multi-stream recorder.
        
        Args:
            targets: List of tuples containing (url, user, room_id) for each stream to record
            mode: Recording mode (manual or automatic)
            automatic_interval: Interval for automatic mode checking
            cookies: TikTok cookies for authentication
            proxy: Proxy settings
            output: Output directory
            duration: Recording duration in seconds
            use_telegram: Whether to upload to Telegram
        """
        self.targets = targets
        self.mode = mode
        self.automatic_interval = automatic_interval
        self.cookies = cookies
        self.proxy = proxy
        self.output = output
        self.duration = duration
        self.use_telegram = use_telegram
        
        self.recording_threads = []
        self.stop_event = threading.Event()
        self.stream_progress = {}  # Track progress for each stream
        self.stream_status = {}   # Track status for each stream
        
    def run(self):
        """
        Start recording all streams.
        """
        logger_manager = LoggerManager()
        
        # Enhanced multi-stream startup display with animated banner
        logger_manager.print_separator(color=Colors.TIKTOK_BLUE)
        
        # Create banner content as a string
        banner_content = f"🎯 Multi-Stream Recording Setup\n\nTotal Streams: {len(self.targets)}\nMode: {self.mode.name} | Duration: {self.duration or 'Unlimited'}"
        
        logger_manager.print_box(
            banner_content,
            padding=2,
            border_color=Colors.TIKTOK_PINK
        )
        
        # Show enhanced target list with progress placeholder
        progress_bars = []
        target_info = []
        
        for i, (url, user, room_id) in enumerate(self.targets):
            name = user or url or f"Room {room_id}"
            target_info.append(f"Stream {i+1}: {Colors.cyan(name)}")
            progress_bars.append(VisualUtils.create_progress_bar(0, 100, width=40))
        
        logger_manager.print_box(
            "📋 Target Streams:\n\n" + "\n".join(target_info),
            padding=2,
            border_color=Colors.INFO
        )
        
        logger_manager.print_separator(color=Colors.TIKTOK_BLUE)
        
        # Initialize progress tracking
        for i, (url, user, room_id) in enumerate(self.targets):
            stream_key = f"Stream-{i+1}"
            self.stream_progress[stream_key] = {
                'name': user or url or f"Room {room_id}",
                'progress': 0,
                'duration': 0,
                'file_size': 0,
                'status': '⏳ Waiting'
            }
        
        # Display initial status dashboard
        self._safe_display_dashboard()
        
        try:
            # Create and start a thread for each stream
            for i, (url, user, room_id) in enumerate(self.targets):
                # Use consistent naming for stream key
                stream_key = f"Stream-{i+1}"
                thread_name = stream_key
                if user:
                    thread_name += f"-{user}"
                elif url:
                    thread_name += f"-{url.split('/')[-1]}"
                elif room_id:
                    thread_name += f"-{room_id}"
                
                thread = threading.Thread(
                    target=self._record_stream,
                    args=(url, user, room_id, stream_key),
                    name=thread_name,
                    daemon=True
                )
                
                self.recording_threads.append(thread)
                thread.start()
                
                # Update status safely
                if stream_key in self.stream_progress:
                    self.stream_progress[stream_key]['status'] = '🔄 Starting'
                    self._safe_display_dashboard()
                
                logger_manager.success(f"Started recording thread: {thread_name}")
                
                # Small delay between starting threads to avoid overwhelming the API
                time.sleep(1)
            
            # Wait for all threads to complete or handle keyboard interrupt
            self._wait_for_completion()
            
        except KeyboardInterrupt:
            logger.info("Received interrupt signal, stopping all recordings...")
            self.stop_all_recordings()
        except Exception as ex:
            logger.error(f"Unexpected error in multi-stream recorder: {ex}  Stopping all recordings...")
            self.stop_all_recordings()
    
    def _record_stream(self, url: Optional[str], user: Optional[str], room_id: Optional[str], thread_name: str):
        """
        Record a single stream in a separate thread.
        """
        try:
            logger.info(f"[{thread_name}] Initializing recorder...")
            
            recorder = TikTokRecorder(
                url=url,
                user=user,
                room_id=room_id,
                mode=self.mode,
                automatic_interval=self.automatic_interval,
                cookies=self.cookies,
                proxy=self.proxy,
                output=self.output,
                duration=self.duration,
                use_telegram=self.use_telegram,
            )
            
            # Override the recorder's run method to respect our stop event
            self._run_recorder_with_stop_event(recorder, thread_name)
            
        except UserLiveException as ex:
            logger.info(f"[{thread_name}] {ex}")
        except TikTokException as ex:
            logger.error(f"[{thread_name}] TikTok error: {ex}")
        except Exception as ex:
            logger.error(f"[{thread_name}] Unexpected error: {ex}")
    
    def _run_recorder_with_stop_event(self, recorder: TikTokRecorder, thread_name: str):
        """
        Run the recorder while respecting the global stop event.
        """
        if self.mode == Mode.MANUAL:
            self._manual_mode_with_stop_event(recorder, thread_name)
        elif self.mode == Mode.AUTOMATIC:
            self._automatic_mode_with_stop_event(recorder, thread_name)
    
    def _manual_mode_with_stop_event(self, recorder: TikTokRecorder, thread_name: str):
        """
        Manual mode recording that respects the stop event.
        """
        if self.stop_event.is_set():
            return
            
        if not recorder.tiktok.is_room_alive(recorder.room_id):
            raise UserLiveException(
                f"[{thread_name}] @{recorder.user}: \033[31mUser is not currently live\033[0m"
            )
        
        self._start_recording_with_stop_event(recorder, thread_name)
    
    def _automatic_mode_with_stop_event(self, recorder: TikTokRecorder, thread_name: str):
        """
        Automatic mode recording that respects the stop event.
        """
        while not self.stop_event.is_set():
            try:
                recorder.room_id = recorder.tiktok.get_room_id_from_user(recorder.user)
                self._manual_mode_with_stop_event(recorder, thread_name)
                
            except UserLiveException as ex:
                logger.info(f"[{thread_name}] {ex}")
                # logger.info(f"[{thread_name}] Waiting {self.automatic_interval} minutes before recheck")
                
                # Wait for the interval or until stop event is set
                for _ in range(self.automatic_interval * 60):  # Convert minutes to seconds
                    if self.stop_event.is_set():
                        return
                    time.sleep(1)
            
            except Exception as ex:
                logger.error(f"[{thread_name}] Unexpected error: {ex}")
                break
    
    def _start_recording_with_stop_event(self, recorder: TikTokRecorder, thread_name: str):
        """
        Start recording with stop event support and resolution detection.
        """
        live_url = recorder.tiktok.get_live_url(recorder.room_id)
        if not live_url:
            raise Exception(f"[{thread_name}] Could not retrieve live URL")
        
        current_date = time.strftime("%Y.%m.%d_%H-%M-%S", time.localtime())
        
        # Create user-specific directory
        base_output = recorder.output if recorder.output else ''
        if isinstance(base_output, str) and base_output != '':
            if not (base_output.endswith('/') or base_output.endswith('\\')):
                if os.name == 'nt':
                    base_output = base_output + "\\"
                else:
                    base_output = base_output + "/"
        
        user_folder = f"{base_output}{recorder.user}/"
        
        # Create the user directory if it doesn't exist
        os.makedirs(user_folder, exist_ok=True)
        
        # Create thread-specific output filename
        output_suffix = f"_{thread_name}" if len(self.targets) > 1 else ""
        output = f"{user_folder}TK_{recorder.user}_{current_date}{output_suffix}_flv.mp4"
        
        logger.info(f"[{thread_name}] {Colors.success('🔴 Started recording')} to: {Colors.cyan(output)}")
        
        # Update progress tracking safely
        if hasattr(self, 'stream_progress') and thread_name in self.stream_progress:
            self.stream_progress[thread_name]['status'] = '🔴 Recording'
            self._safe_display_dashboard()
        
        # Setup resolution detection
        config_manager = ConfigManager()
        check_interval = config_manager.get_resolution_check_interval(
            user=recorder.user, room_id=recorder.room_id
        )
        
        resolution_detector = ResolutionDetector(
            stream_url=live_url,
            check_interval=check_interval
        )
        
        buffer_size = 512 * 1024  # 512 KB buffer
        buffer = bytearray()
        
        with open(output, "wb") as out_file:
            stop_recording = False
            restart_requested = [False]  # Use list to allow modification in nested function
            start_time = time.time()
            
            def on_resolution_change(old_resolution, new_resolution):
                if config_manager.should_restart_on_resolution_change(user=recorder.user, room_id=recorder.room_id):
                    logger.info(f"[{thread_name}] Resolution change detected: {old_resolution[0]}x{old_resolution[1]} → {new_resolution[0]}x{new_resolution[1]}")
                    logger.warning(f"[{thread_name}] {Colors.warning('🔄 Auto-restart enabled. Stopping current recording to restart with new resolution.')}")
                    restart_requested[0] = True
            
            # Start resolution monitoring
            resolution_detector.start_monitoring(on_resolution_change)
            
            while not stop_recording and not self.stop_event.is_set():
                try:
                    if not recorder.tiktok.is_room_alive(recorder.room_id):
                        logger.info(f"[{thread_name}] User is no longer live. Stopping recording.")
                        break
                    
                    for chunk in recorder.tiktok.download_live_stream(live_url):
                        if self.stop_event.is_set():
                            stop_recording = True
                            break
                            
                        buffer.extend(chunk)
                        if len(buffer) >= buffer_size:
                            out_file.write(buffer)
                            buffer.clear()
                            
                            # Update progress tracking safely
                            if (hasattr(self, 'stream_progress') and 
                                thread_name in self.stream_progress and 
                                os.path.exists(output)):
                                try:
                                    elapsed = time.time() - start_time
                                    file_size_mb = os.path.getsize(output) / (1024 * 1024)
                                    
                                    progress_percent = 0
                                    if recorder.duration:
                                        progress_percent = min(100, int((elapsed / recorder.duration) * 100))
                                    else:
                                        # For unlimited duration, show elapsed minutes
                                        progress_percent = min(100, int(elapsed / 60))
                                    
                                    self.stream_progress[thread_name].update({
                                        'duration': int(elapsed),
                                        'file_size': file_size_mb,
                                        'progress': progress_percent
                                    })
                                    
                                    # Update dashboard every 10 seconds
                                    if int(elapsed) % 10 == 0:
                                        self._safe_display_dashboard()
                                except (OSError, AttributeError) as e:
                                    # File doesn't exist yet or other error, skip update
                                    pass
                        
                        elapsed_time = time.time() - start_time
                        if recorder.duration and elapsed_time >= recorder.duration:
                            stop_recording = True
                            break
                        
                        # Check if restart was requested due to resolution change
                        if restart_requested[0]:
                            logger.info(f"[{thread_name}] Stopping current recording due to resolution change...")
                            stop_recording = True
                            break
                
                except Exception as ex:
                    logger.error(f"[{thread_name}] Recording error: {ex}")
                    stop_recording = True
                
                finally:
                    if buffer:
                        out_file.write(buffer)
                        buffer.clear()
                    out_file.flush()
        
        # Stop resolution monitoring
        resolution_detector.stop_monitoring()
        
        logger.info(f"[{thread_name}] {Colors.success('⏹️ Recording finished')}: {Colors.cyan(output)}")
        
        # Update final status safely
        if hasattr(self, 'stream_progress') and thread_name in self.stream_progress:
            self.stream_progress[thread_name]['status'] = '✅ Completed'
            self._safe_display_dashboard()
        
        # Convert FLV to MP4
        try:
            from utils.video_management import VideoManagement
            VideoManagement.convert_flv_to_mp4(output)
            
            if recorder.use_telegram:
                from upload.telegram import Telegram
                Telegram().upload(output.replace('_flv.mp4', '.mp4'))
        except Exception as ex:
            logger.error(f"[{thread_name}] Post-processing error: {ex}")
        
        # Check if restart was requested due to resolution change
        if restart_requested[0] and not self.stop_event.is_set() and recorder.tiktok.is_room_alive(recorder.room_id):
            logger.info(f"[{thread_name}] " + "="*50)
            logger.info(f"[{thread_name}] 🔄 AUTO-RESTART: Starting new recording with updated resolution...")
            logger.info(f"[{thread_name}] " + "="*50)
            time.sleep(2)  # Brief pause before restarting
            
            # Update the recorder's live URL for the new recording
            try:
                new_live_url = recorder.tiktok.get_live_url(recorder.room_id)
                if new_live_url:
                    # Recursively restart recording with new URL
                    self._start_recording_with_stop_event(recorder, thread_name)
                else:
                    logger.warning(f"[{thread_name}] Unable to get new live URL for restart. User may no longer be live.")
            except Exception as ex:
                logger.error(f"[{thread_name}] Error during auto-restart: {ex}")
    
    def _wait_for_completion(self):
        """
        Wait for all recording threads to complete.
        """
        try:
            while any(thread.is_alive() for thread in self.recording_threads):
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received, stopping all recordings...")
            self.stop_all_recordings()
    
    def stop_all_recordings(self):
        """
        Stop all recording threads.
        """
        logger.info("Stopping all recordings...")
        self.stop_event.set()
        
        # Wait for all threads to finish
        for thread in self.recording_threads:
            if thread.is_alive():
                thread.join(timeout=5)
        
        logger.info("All recordings stopped.")
        
        # Display final summary
        try:
            self._display_final_summary()
        except Exception as e:
            # If final summary fails, at least show basic completion message
            logger.info("Multi-stream recording session completed.")
        
    def _display_progress_dashboard(self):
        """
        Display a real-time progress dashboard for all streams in a horizontal grid layout.
        """
        print("\033[H\033[J", end='')  # Clear screen and move cursor to top
        
        logger_manager = LoggerManager()
        logger_manager.print_separator(color=Colors.TIKTOK_BLUE)
        
        # Dashboard header
        header = f"📊 {Colors.tiktok_theme('Multi-Stream Recording Dashboard', use_pink=True)}"
        print(VisualUtils.center_text(header))
        print()
        
        # Choose layout based on number of streams
        if len(self.stream_progress) <= 6:
            self._display_vertical_layout()
        else:
            self._display_grid_layout()
        
        logger_manager.print_separator(color=Colors.TIKTOK_BLUE)
        total_streams = len(self.stream_progress)
        active_streams = sum(1 for data in self.stream_progress.values() if '🔴' in data['status'])
        completed_streams = sum(1 for data in self.stream_progress.values() if '✅' in data['status'])
        
        status_info = f"📊 Total: {total_streams} | 🔴 Active: {active_streams} | ✅ Completed: {completed_streams}"
        print(f"  {Colors.info(status_info)}")
        print(f"  {Colors.info('ℹ️  Press Ctrl+C to stop all recordings')}", end='\r')
        
    def _safe_display_dashboard(self):
        """
        Safely display the progress dashboard with error handling.
        """
        try:
            if hasattr(self, 'stream_progress') and self.stream_progress:
                self._display_progress_dashboard()
        except Exception as e:
            # If dashboard display fails, just log it and continue recording
            # This ensures recording continues even if visual features fail
            pass
        
    def _display_final_summary(self):
        """
        Display a final summary of all recordings.
        """
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
        
    def _display_vertical_layout(self):
        """
        Display streams in vertical layout (for 6 or fewer streams).
        """
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
            
    def _display_grid_layout(self):
        """
        Display streams in horizontal grid layout (for many streams).
        """
        terminal_width = VisualUtils.get_terminal_width()
        
        # Calculate optimal column width and number of columns
        min_column_width = 35  # Minimum width needed for stream info
        max_columns = min(4, terminal_width // min_column_width)  # Max 4 columns
        columns_per_row = max(2, max_columns)  # At least 2 columns
        
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
                        # Remove ANSI codes for width calculation
                        clean_text = self._remove_ansi_codes(display[line_idx])
                        padded_text = display[line_idx].ljust(len(display[line_idx]) + (min_column_width - len(clean_text)))
                        line_parts.append(padded_text)
                    else:
                        line_parts.append(' ' * min_column_width)
                
                print('  ' + '  '.join(line_parts))
            
            print()  # Empty line between rows
            
    def _remove_ansi_codes(self, text):
        """
        Remove ANSI color codes from text for width calculation.
        """
        import re
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)
