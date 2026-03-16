import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from src.utils.logger import logger

class ConfigManager:
    """
    Handles loading environment variables and managing secrets.
    """
    def __init__(self):
        load_dotenv()
        self._config: Dict[str, str] = dict(os.environ)

    def get_val(self, key: str, default: Optional[str] = None) -> Optional[str]:
        return self._config.get(key, default)

    def set_val(self, key: str, value: str):
        self._config[key] = value
        logger.info(f"Updated configuration for {key} in memory")

    def save_config(self):
        """Persists the current in-memory config back to .env."""
        try:
            with open(".env", "w") as f:
                for k, v in self._config.items():
                    # Only save relevant keys or all if it's a dedicated .env
                    f.write(f"{k}={v}\n")
            logger.info("Persisted physical config to .env")
            return True
        except Exception as e:
            logger.error(f"Failed to save .env: {e}")
            return False

config = ConfigManager()
