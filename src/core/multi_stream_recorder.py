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
        
    def run(self):
        """
        Start recording all streams.
        """
        logger_manager = LoggerManager()
        
        # Enhanced multi-stream startup display
        logger_manager.print_separator(color=Colors.TIKTOK_BLUE)
        logger_manager.print_box(
            f"🎯 Multi-Stream Recording Setup\n\nTotal Streams: {len(self.targets)}\nMode: {self.mode.name}\nDuration: {self.duration or 'Unlimited'}",
            padding=2,
            border_color=Colors.TIKTOK_PINK
        )
        
        # Show target list
        target_info = []
        for i, (url, user, room_id) in enumerate(self.targets):
            if user:
                target_info.append(f"Stream {i+1}: @{user}")
            elif url:
                target_info.append(f"Stream {i+1}: {url}")
            elif room_id:
                target_info.append(f"Stream {i+1}: Room {room_id}")
        
        logger_manager.print_box(
            "📋 Target Streams:\n\n" + "\n".join(target_info),
            padding=2,
            border_color=Colors.INFO
        )
        logger_manager.print_separator(color=Colors.TIKTOK_BLUE)
        
        try:
            # Create and start a thread for each stream
            for i, (url, user, room_id) in enumerate(self.targets):
                thread_name = f"Stream-{i+1}"
                if user:
                    thread_name += f"-{user}"
                elif url:
                    thread_name += f"-{url.split('/')[-1]}"
                elif room_id:
                    thread_name += f"-{room_id}"
                
                thread = threading.Thread(
                    target=self._record_stream,
                    args=(url, user, room_id, thread_name),
                    name=thread_name,
                    daemon=True
                )
                
                self.recording_threads.append(thread)
                thread.start()
                logger_manager.success(f"Started recording thread: {thread_name}")
                
                # Small delay between starting threads to avoid overwhelming the API
                time.sleep(1)
            
            # Wait for all threads to complete or handle keyboard interrupt
            self._wait_for_completion()
            
        except KeyboardInterrupt:
            logger.info("Received interrupt signal, stopping all recordings...")
            self.stop_all_recordings()
        except Exception as ex:
            logger.error(f"Unexpected error in multi-stream recorder: {ex}")
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
        Start recording with stop event support.
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
        
        logger.info(f"[{thread_name}] \033[32mStarted recording\033[0m to: {output}")
        
        buffer_size = 512 * 1024  # 512 KB buffer
        buffer = bytearray()
        
        with open(output, "wb") as out_file:
            stop_recording = False
            start_time = time.time()
            
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
                        
                        elapsed_time = time.time() - start_time
                        if recorder.duration and elapsed_time >= recorder.duration:
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
        
        logger.info(f"[{thread_name}] \033[36mRecording finished\033[0m: {output}")
        
        # Convert FLV to MP4
        try:
            from utils.video_management import VideoManagement
            VideoManagement.convert_flv_to_mp4(output)
            
            if recorder.use_telegram:
                from upload.telegram import Telegram
                Telegram().upload(output.replace('_flv.mp4', '.mp4'))
        except Exception as ex:
            logger.error(f"[{thread_name}] Post-processing error: {ex}")
    
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
