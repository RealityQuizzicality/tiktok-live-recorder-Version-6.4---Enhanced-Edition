import os
import time
from http.client import HTTPException

from requests import RequestException

from core.tiktok_api import TikTokAPI
from utils.logger_manager import logger, LoggerManager
from utils.video_management import VideoManagement
from upload.telegram import Telegram
from utils.custom_exceptions import LiveNotFound, UserLiveException, \
    TikTokException
from utils.enums import Mode, Error, TimeOut, TikTokError
from utils.colors import Colors, VisualUtils
from utils.config_manager import ConfigManager
from utils.resolution_detector import ResolutionDetector


class TikTokRecorder:

    def __init__(
        self,
        url,
        user,
        room_id,
        mode,
        automatic_interval,
        cookies,
        proxy,
        output,
        duration,
        use_telegram,
    ):
        # Setup TikTok API client
        self.tiktok = TikTokAPI(proxy=proxy, cookies=cookies)

        # TikTok Data
        self.url = url
        self.user = user
        self.room_id = room_id

        # Tool Settings
        self.mode = mode
        self.automatic_interval = automatic_interval
        self.duration = duration
        self.output = output

        # Upload Settings
        self.use_telegram = use_telegram

        # Check if the user's country is blacklisted
        self.check_country_blacklisted()

        # Get live information based on the provided user data
        if self.url:
            self.user, self.room_id = \
                self.tiktok.get_room_and_user_from_url(self.url)

        if not self.user:
            self.user = self.tiktok.get_user_from_room_id(self.room_id)

        if not self.room_id:
            self.room_id = self.tiktok.get_room_id_from_user(self.user)

        # Enhanced user info display
        logger_manager = LoggerManager()
        logger_manager.print_separator(color=Colors.TIKTOK_BLUE)
        logger_manager.print_box(
            f"🎯 Target Information\n\nUsername: {self.user}\nRoom ID:  {self.room_id}",
            padding=2,
            border_color=Colors.TIKTOK_PINK
        )
        
        self.config_manager = ConfigManager()
        self.resolution_detector = ResolutionDetector(
            stream_url=self.tiktok.get_live_url(self.room_id),
            check_interval=self.config_manager.get_resolution_check_interval(
                user=self.user, room_id=self.room_id
            )
        )
        logger_manager.print_separator(color=Colors.TIKTOK_BLUE)

        # If proxy is provided, set up the HTTP client without the proxy
        if proxy:
            self.tiktok = TikTokAPI(proxy=None, cookies=cookies)

    def run(self):
        """
        runs the program in the selected mode. 
        
        If the mode is MANUAL, it checks if the user is currently live and
        if so, starts recording.
        
        If the mode is AUTOMATIC, it continuously checks if the user is live
        and if not, waits for the specified timeout before rechecking.
        If the user is live, it starts recording.
        """
        if self.mode == Mode.MANUAL:
            self.manual_mode()

        if self.mode == Mode.AUTOMATIC:
            self.automatic_mode()

    def manual_mode(self):
        if not self.tiktok.is_room_alive(self.room_id):
            logger_manager = LoggerManager()
            logger_manager.info_red(f"@{self.user}: {TikTokError.USER_NOT_CURRENTLY_LIVE}")
            raise UserLiveException(
                f"@{self.user}: {TikTokError.USER_NOT_CURRENTLY_LIVE}"
            )

        self.start_recording()

    def automatic_mode(self):
        while True:
            try:
                self.room_id = self.tiktok.get_room_id_from_user(self.user)
                self.manual_mode()

            except UserLiveException as ex:
                logger.info(ex)
                # logger.info(f"Waiting {self.automatic_interval} minutes before recheck\n")
                time.sleep(self.automatic_interval * TimeOut.ONE_MINUTE)

            except ConnectionError:
                logger.error(Error.CONNECTION_CLOSED_AUTOMATIC)
                time.sleep(TimeOut.CONNECTION_CLOSED * TimeOut.ONE_MINUTE)

            except Exception as ex:
                logger.error(f"Unexpected error: {ex}\n")

    def start_recording(self):
        """
        Start recording live
        """
        live_url = self.tiktok.get_live_url(self.room_id)
        if not live_url:
            raise LiveNotFound(TikTokError.RETRIEVE_LIVE_URL)

        current_date = time.strftime("%Y.%m.%d_%H-%M-%S", time.localtime())

        # Create user-specific directory
        base_output = self.output if self.output else ''
        if isinstance(base_output, str) and base_output != '':
            if not (base_output.endswith('/') or base_output.endswith('\\')):
                if os.name == 'nt':
                    base_output = base_output + "\\"
                else:
                    base_output = base_output + "/"
        
        user_folder = f"{base_output}{self.user}/"
        
        # Create the user directory if it doesn't exist
        os.makedirs(user_folder, exist_ok=True)
        
        output = f"{user_folder}TK_{self.user}_{current_date}_flv.mp4"

        # Enhanced recording start message
        logger_manager = LoggerManager()
        
        if self.duration:
            record_msg = f"Recording for {self.duration} seconds"
        else:
            record_msg = "Recording live stream"
            
        logger_manager.print_box(
            f"🔴 {record_msg}\n\n📝 Output: {output}\n⏱️ Started: {current_date}",
            padding=2,
            border_color=Colors.SUCCESS
        )
        
        logger_manager.print_status("Press CTRL + C once to stop recording", "WARNING")
        print()

        buffer_size = 512 * 1024 # 512 KB buffer
        buffer = bytearray()
        
        # Progress tracking variables
        recording_start_time = time.time()
        last_update = time.time()
        total_bytes = 0
        update_interval = 2.0  # Update every 2 seconds
        
        with open(output, "wb") as out_file:
            stop_recording = False
            restart_requested = [False]  # Use list to allow modification in nested function
            
            def on_resolution_change(old_resolution, new_resolution):
                if self.config_manager.should_restart_on_resolution_change(user=self.user, room_id=self.room_id):
                    logger.info(f"Resolution change detected: {old_resolution[0]}x{old_resolution[1]} → {new_resolution[0]}x{new_resolution[1]}")
                    logger.info("Auto-restart enabled. Stopping current recording to restart with new resolution.")
                    restart_requested[0] = True
            
            self.resolution_detector.start_monitoring(on_resolution_change)
            
            while not stop_recording:
                try:
                    if not self.tiktok.is_room_alive(self.room_id):
                        print("\n")
                        logger_manager.warning("User is no longer live. Stopping recording.")
                        break

                    start_time = time.time()
                    for chunk in self.tiktok.download_live_stream(live_url):
                        buffer.extend(chunk)
                        total_bytes += len(chunk)
                        
                        if len(buffer) >= buffer_size:
                            out_file.write(buffer)
                            buffer.clear()
                            
                            # Update progress every few seconds
                            current_time = time.time()
                            if current_time - last_update >= update_interval:
                                elapsed_total = current_time - recording_start_time
                                file_size_mb = total_bytes / (1024 * 1024)
                                bitrate_kbps = (total_bytes * 8) / (elapsed_total * 1000) if elapsed_total > 0 else 0
                                
                                # Format duration
                                hours = int(elapsed_total // 3600)
                                minutes = int((elapsed_total % 3600) // 60)
                                seconds = int(elapsed_total % 60)
                                duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                                
                                # Create progress display
                                if self.duration:
                                    progress_pct = min(100, (elapsed_total / self.duration) * 100)
                                    remaining_time = max(0, self.duration - elapsed_total)
                                    rem_hours = int(remaining_time // 3600)
                                    rem_minutes = int((remaining_time % 3600) // 60)
                                    rem_seconds = int(remaining_time % 60)
                                    remaining_str = f"{rem_hours:02d}:{rem_minutes:02d}:{rem_seconds:02d}"
                                    
                                    progress_bar = VisualUtils.create_progress_bar(
                                        int(elapsed_total), int(self.duration), width=25
                                    )
                                    
                                    status_line = (f"\r{Colors.tiktok_theme('🔴 RECORDING', use_pink=True)} "
                                                 f"{progress_bar} "
                                                 f"{Colors.info(duration_str)} "
                                                 f"| {Colors.success(f'{file_size_mb:.1f} MB')} "
                                                 f"| {Colors.cyan(f'{bitrate_kbps:.0f} kbps')} "
                                                 f"| {Colors.warning(f'ETA: {remaining_str}')}")
                                else:
                                    status_line = (f"\r{Colors.tiktok_theme('🔴 RECORDING', use_pink=True)} "
                                                 f"{Colors.info(duration_str)} "
                                                 f"| {Colors.success(f'{file_size_mb:.1f} MB')} "
                                                 f"| {Colors.cyan(f'{bitrate_kbps:.0f} kbps')}")
                                
                                print(status_line, end='', flush=True)
                                last_update = current_time

                        elapsed_time = time.time() - start_time
                        if self.duration and elapsed_time >= self.duration:
                            stop_recording = True
                            break
                        
                        # Check if restart was requested due to resolution change
                        if restart_requested[0]:
                            logger.info("Stopping current recording due to resolution change...")
                            stop_recording = True
                            break

                except ConnectionError:
                    if self.mode == Mode.AUTOMATIC:
                        logger.error(Error.CONNECTION_CLOSED_AUTOMATIC)
                        time.sleep(TimeOut.CONNECTION_CLOSED * TimeOut.ONE_MINUTE)

                except (RequestException, HTTPException):
                    time.sleep(2)

                except KeyboardInterrupt:
                    logger.info("Recording stopped by user.")
                    stop_recording = True

                except Exception as ex:
                    logger.error(f"Unexpected error: {ex}\n")
                    stop_recording = True

                finally:
                    if buffer:
                        out_file.write(buffer)
                        buffer.clear()
                    out_file.flush()

        self.resolution_detector.stop_monitoring()
        
        end_time = time.strftime("%Y.%m.%d_%H-%M-%S", time.localtime())
        file_size = os.path.getsize(output) / (1024 * 1024)  # Size in MB
        
        logger_manager.print_box(
            f"✓ Recording Complete!\n\n📁 File: {output}\n📊 Size: {file_size:.2f} MB\n⏱️ Finished: {end_time}",
            padding=2,
            border_color=Colors.SUCCESS
        )
        
        logger_manager.print_status("Converting FLV to MP4...", "INFO")
        VideoManagement.convert_flv_to_mp4(output)
        logger_manager.success("Video conversion completed!")

        if self.use_telegram:
            logger_manager.print_status("Uploading to Telegram...", "INFO")
            Telegram().upload(output.replace('_flv.mp4', '.mp4'))
            logger_manager.success("Telegram upload completed!")
        
        # Check if restart was requested due to resolution change
        if restart_requested[0] and self.tiktok.is_room_alive(self.room_id):
            logger.info("\n" + "="*50)
            logger.info("🔄 AUTO-RESTART: Starting new recording with updated resolution...")
            logger.info("="*50 + "\n")
            time.sleep(2)  # Brief pause before restarting
            
            # Update the resolution detector with the new stream URL
            try:
                new_live_url = self.tiktok.get_live_url(self.room_id)
                if new_live_url:
                    self.resolution_detector = ResolutionDetector(
                        stream_url=new_live_url,
                        check_interval=self.config_manager.get_resolution_check_interval(
                            user=self.user, room_id=self.room_id
                        )
                    )
                    # Restart recording
                    self.start_recording()
                else:
                    logger.warning("Unable to get new live URL for restart. User may no longer be live.")
            except Exception as ex:
                logger.error(f"Error during auto-restart: {ex}")

    def check_country_blacklisted(self):
        is_blacklisted = self.tiktok.is_country_blacklisted()
        if not is_blacklisted:
            return False

        if self.room_id is None:
            raise TikTokException(TikTokError.COUNTRY_BLACKLISTED)

        if self.mode == Mode.AUTOMATIC:
            raise TikTokException(TikTokError.COUNTRY_BLACKLISTED_AUTO_MODE)
