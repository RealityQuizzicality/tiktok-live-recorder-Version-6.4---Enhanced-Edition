import json
import os
from typing import Dict, Any, Optional
from utils.logger_manager import logger


class ConfigManager:
    """
    Manages per-user and per-room configuration settings.
    """
    
    def __init__(self, config_file_path: str = None):
        if config_file_path is None:
            config_file_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                'config', 
                'user_settings.json'
            )
        
        self.config_file_path = config_file_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        try:
            if os.path.exists(self.config_file_path):
                with open(self.config_file_path, 'r') as f:
                    return json.load(f)
            else:
                # Create default config if file doesn't exist
                os.makedirs(os.path.dirname(self.config_file_path), exist_ok=True)
                default_config = {
                    "default": {
                        "restart_on_resolution_change": False,
                        "resolution_check_interval": 5
                    },
                    "users": {},
                    "rooms": {}
                }
                self._save_config(default_config)
                return default_config
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return {
                "default": {
                    "restart_on_resolution_change": False,
                    "resolution_check_interval": 5
                },
                "users": {},
                "rooms": {}
            }
    
    def _save_config(self, config: Dict[str, Any] = None):
        """Save configuration to file."""
        try:
            config_to_save = config or self.config
            with open(self.config_file_path, 'w') as f:
                json.dump(config_to_save, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving config: {e}")
    
    def get_user_setting(self, user: str, setting: str, default_value: Any = None) -> Any:
        """Get a setting for a specific user."""
        user_config = self.config.get("users", {}).get(user, {})
        if setting in user_config:
            return user_config[setting]
        
        # Fall back to default
        return self.config.get("default", {}).get(setting, default_value)
    
    def get_room_setting(self, room_id: str, setting: str, default_value: Any = None) -> Any:
        """Get a setting for a specific room."""
        room_config = self.config.get("rooms", {}).get(room_id, {})
        if setting in room_config:
            return room_config[setting]
        
        # Fall back to default
        return self.config.get("default", {}).get(setting, default_value)
    
    def set_user_setting(self, user: str, setting: str, value: Any):
        """Set a setting for a specific user."""
        if "users" not in self.config:
            self.config["users"] = {}
        if user not in self.config["users"]:
            self.config["users"][user] = {}
        
        self.config["users"][user][setting] = value
        self._save_config()
        logger.info(f"Set {setting}={value} for user @{user}")
    
    def set_room_setting(self, room_id: str, setting: str, value: Any):
        """Set a setting for a specific room."""
        if "rooms" not in self.config:
            self.config["rooms"] = {}
        if room_id not in self.config["rooms"]:
            self.config["rooms"][room_id] = {}
        
        self.config["rooms"][room_id][setting] = value
        self._save_config()
        logger.info(f"Set {setting}={value} for room {room_id}")
    
    def should_restart_on_resolution_change(self, user: str = None, room_id: str = None) -> bool:
        """Check if resolution change restart is enabled for user or room."""
        if user:
            return self.get_user_setting(user, "restart_on_resolution_change", False)
        elif room_id:
            return self.get_room_setting(room_id, "restart_on_resolution_change", False)
        else:
            return self.config.get("default", {}).get("restart_on_resolution_change", False)
    
    def get_resolution_check_interval(self, user: str = None, room_id: str = None) -> int:
        """Get resolution check interval for user or room."""
        if user:
            return self.get_user_setting(user, "resolution_check_interval", 5)
        elif room_id:
            return self.get_room_setting(room_id, "resolution_check_interval", 5)
        else:
            return self.config.get("default", {}).get("resolution_check_interval", 5)
