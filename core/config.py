"""
Configuration management for Intervals API.
Loads settings from environment variables and .env file.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Get the project root directory (parent of core/)
PROJECT_ROOT = Path(__file__).parent.parent

# Load .env file from project root
env_path = PROJECT_ROOT / '.env'
load_dotenv(dotenv_path=env_path)


def get_api_key():
    """
    Get the Intervals API key from environment.

    Returns:
        str: API key

    Raises:
        ValueError: If API key is not set
    """
    api_key = os.getenv('INTERVALS_API_KEY')

    if not api_key or api_key == 'your_api_key_here':
        raise ValueError(
            "INTERVALS_API_KEY not set!\n\n"
            "Please create a .env file in the project root with your API key:\n"
            "1. Copy .env.example to .env\n"
            "2. Edit .env and add your actual API key\n"
            "3. Get your API key from: https://www.myintervals.com/api/"
        )

    return api_key


def get_default_task_id():
    """Get default task ID from environment or return standard default."""
    return os.getenv('DEFAULT_TASK_ID', '123456789')


def get_default_project_id():
    """Get default project ID from environment or return standard default."""
    return os.getenv('DEFAULT_PROJECT_ID', '123456789')


def get_default_work_type():
    """Get default work type from environment or return standard default."""
    return os.getenv('DEFAULT_WORK_TYPE', 'India-Meeting')


# Export common configuration
class Config:
    """Configuration class with all settings."""
    API_KEY = property(lambda self: get_api_key())
    DEFAULT_TASK_ID = get_default_task_id()
    DEFAULT_PROJECT_ID = get_default_project_id()
    DEFAULT_WORK_TYPE = get_default_work_type()

    @staticmethod
    def get_api_key():
        """Get API key (static method for easy access)."""
        return get_api_key()
