import subprocess
import json
import threading
import time
from typing import Optional, Tuple, Callable
from utils.logger_manager import logger


class ResolutionDetector:
    """
    Detects video resolution changes in live streams using ffprobe.
    """
    
    def __init__(self, stream_url: str, check_interval: int = 5):
        self.stream_url = stream_url
        self.check_interval = check_interval
        self.current_resolution = None
        self.is_monitoring = False
        self.monitor_thread = None
        self.resolution_change_callback = None
        self._stop_event = threading.Event()
    
    def get_current_resolution(self) -> Optional[Tuple[int, int]]:
        """
        Get the current resolution of the stream using ffprobe.
        Returns (width, height) or None if detection fails.
        """
        try:
            # Use ffprobe to get stream information
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-select_streams', 'v:0',
                '-show_entries', 'stream=width,height',
                '-of', 'json=compact=1',
                '-analyzeduration', '1000000',  # 1 second analysis
                '-probesize', '1000000',        # 1MB probe size
                self.stream_url
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10  # 10 second timeout
            )
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                streams = data.get('streams', [])
                
                if streams and len(streams) > 0:
                    stream = streams[0]
                    width = stream.get('width')
                    height = stream.get('height')
                    
                    if width and height:
                        return (int(width), int(height))
            
            logger.debug(f"Could not detect resolution: {result.stderr}")
            return None
            
        except subprocess.TimeoutExpired:
            logger.warning("Resolution detection timed out")
            return None
        except Exception as e:
            logger.debug(f"Resolution detection error: {e}")
            return None
    
    def start_monitoring(self, resolution_change_callback: Callable[[Tuple[int, int], Tuple[int, int]], None]):
        """
        Start monitoring resolution changes.
        
        Args:
            resolution_change_callback: Function called when resolution changes.
                                      Takes (old_resolution, new_resolution) as parameters.
        """
        if self.is_monitoring:
            logger.warning("Resolution monitoring is already active")
            return
        
        self.resolution_change_callback = resolution_change_callback
        self.is_monitoring = True
        self._stop_event.clear()
        
        # Get initial resolution
        initial_resolution = self.get_current_resolution()
        if initial_resolution:
            self.current_resolution = initial_resolution
            logger.info(f"Initial resolution detected: {initial_resolution[0]}x{initial_resolution[1]}")
        else:
            logger.warning("Could not detect initial resolution")
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop,
            name="ResolutionMonitor",
            daemon=True
        )
        self.monitor_thread.start()
        logger.info(f"Started resolution monitoring (check interval: {self.check_interval}s)")
    
    def stop_monitoring(self):
        """Stop resolution monitoring."""
        if not self.is_monitoring:
            return
        
        self.is_monitoring = False
        self._stop_event.set()
        
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=5)
        
        logger.info("Stopped resolution monitoring")
    
    def _monitor_loop(self):
        """Main monitoring loop that runs in a separate thread."""
        consecutive_failures = 0
        max_consecutive_failures = 3
        
        while not self._stop_event.is_set():
            try:
                new_resolution = self.get_current_resolution()
                
                if new_resolution:
                    consecutive_failures = 0  # Reset failure counter
                    
                    # Check if resolution has changed
                    if (self.current_resolution and 
                        new_resolution != self.current_resolution):
                        
                        logger.info(f"Resolution change detected: "
                                  f"{self.current_resolution[0]}x{self.current_resolution[1]} → "
                                  f"{new_resolution[0]}x{new_resolution[1]}")
                        
                        old_resolution = self.current_resolution
                        self.current_resolution = new_resolution
                        
                        # Trigger callback
                        if self.resolution_change_callback:
                            try:
                                self.resolution_change_callback(old_resolution, new_resolution)
                            except Exception as e:
                                logger.error(f"Error in resolution change callback: {e}")
                    
                    elif not self.current_resolution:
                        # First successful detection
                        self.current_resolution = new_resolution
                        logger.info(f"Resolution detected: {new_resolution[0]}x{new_resolution[1]}")
                
                else:
                    consecutive_failures += 1
                    logger.debug(f"Resolution detection failed ({consecutive_failures}/{max_consecutive_failures})")
                    
                    # If we have too many consecutive failures, stop monitoring
                    if consecutive_failures >= max_consecutive_failures:
                        logger.warning("Too many consecutive resolution detection failures, stopping monitoring")
                        break
                
                # Wait for next check
                self._stop_event.wait(self.check_interval)
                
            except Exception as e:
                logger.error(f"Error in resolution monitoring loop: {e}")
                break
        
        self.is_monitoring = False
    
    @staticmethod
    def is_ffprobe_available() -> bool:
        """Check if ffprobe is available in the system."""
        try:
            result = subprocess.run(
                ['ffprobe', '-version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False
