import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

def safe_int_env(env_var, default_value):
    """
    Safely convert environment variable to integer with error handling.
    
    Args:
        env_var (str): Environment variable name
        default_value (int): Default value to use if conversion fails
        
    Returns:
        int: The converted value or default if conversion fails
    """
    try:
        value = os.getenv(env_var)
        if value is None:
            return default_value
        return int(value)
    except (ValueError, TypeError):
        print(f"⚠️ Warning: Invalid value for {env_var}. Using default: {default_value}")
        return default_value

class DashboardConfig:
    """
    Professional configuration management for Jenkins Dashboard.
    Uses environment variables with sensible defaults.
    """
    
    # Jenkins API Settings
    JENKINS_USER = os.getenv("JENKINS_USER")
    JENKINS_TOKEN = os.getenv("JENKINS_TOKEN")
    JENKINS_BASE_URL = os.getenv("JENKINS_BASE_URL")
    
    # Dashboard Display Settings
    INACTIVE_JOB_THRESHOLD_DAYS = safe_int_env("INACTIVE_JOB_THRESHOLD_DAYS", 60)
    ITEMS_PER_PAGE_DEFAULT = safe_int_env("ITEMS_PER_PAGE_DEFAULT", 50)
    REFRESH_INTERVAL_SECONDS = safe_int_env("REFRESH_INTERVAL_SECONDS", 300)
    
    # Test Job Detection Settings
    TEST_JOB_EXCLUDE_WORDS = os.getenv("TEST_JOB_EXCLUDE_WORDS", "").split(",") if os.getenv("TEST_JOB_EXCLUDE_WORDS") else []
    TEST_JOB_KEYWORDS = os.getenv("TEST_JOB_KEYWORDS", "").split(",") if os.getenv("TEST_JOB_KEYWORDS") else []
    
    # Database Settings
    DB_FILE = os.getenv("DB_FILE", "db/jenkins_data.db")
    
    # PostgreSQL Settings (for production)
    DB_TYPE = os.getenv("DB_TYPE", "sqlite")  # "sqlite" or "postgresql"
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = safe_int_env("POSTGRES_PORT", 5432)
    POSTGRES_DB = os.getenv("POSTGRES_DB", "jenkins_dashboard")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "jenkins_user")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "jenkins_password_2024")
    
    # UI Settings
    DASHBOARD_TITLE = os.getenv("DASHBOARD_TITLE", "Jenkins Dashboard")
    PAGE_LAYOUT = os.getenv("PAGE_LAYOUT", "wide")
    
    # Timezone Settings
    TIMEZONE = os.getenv("TIMEZONE", "UTC")
    TIMEZONE_DISPLAY_FORMAT = os.getenv("TIMEZONE_DISPLAY_FORMAT", "%d %b %H:%M %Z")
    
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present"""
        missing_configs = []
        
        if not cls.JENKINS_USER:
            missing_configs.append("JENKINS_USER")
        if not cls.JENKINS_TOKEN:
            missing_configs.append("JENKINS_TOKEN")
        if not cls.JENKINS_BASE_URL:
            missing_configs.append("JENKINS_BASE_URL")
            
        if missing_configs:
            raise ValueError(f"Missing required configuration: {', '.join(missing_configs)}")
        
        return True
    
    @classmethod
    def get_config_summary(cls):
        """Get a summary of current configuration for debugging"""
        return {
            "jenkins_configured": bool(cls.JENKINS_USER and cls.JENKINS_TOKEN and cls.JENKINS_BASE_URL),
            "inactive_threshold_days": cls.INACTIVE_JOB_THRESHOLD_DAYS,
            "items_per_page": cls.ITEMS_PER_PAGE_DEFAULT,
            "test_exclude_words_count": len(cls.TEST_JOB_EXCLUDE_WORDS),
            "test_keywords_count": len(cls.TEST_JOB_KEYWORDS),
            "db_file": cls.DB_FILE
        } 