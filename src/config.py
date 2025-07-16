import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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
    INACTIVE_JOB_THRESHOLD_DAYS = int(os.getenv("INACTIVE_JOB_THRESHOLD_DAYS", 60))
    ITEMS_PER_PAGE_DEFAULT = int(os.getenv("ITEMS_PER_PAGE_DEFAULT", 50))
    REFRESH_INTERVAL_SECONDS = int(os.getenv("REFRESH_INTERVAL_SECONDS", 300))
    
    # Test Job Detection Settings
    TEST_JOB_EXCLUDE_WORDS = os.getenv("TEST_JOB_EXCLUDE_WORDS", 
        "latest,saastest,attest,contest,detest,protest,suggest,request,rest,nest,west,east,best,manifest,testament,testimony,testosterone,testicular,testify,testimonial,testable,tested"
    ).split(",")
    
    TEST_JOB_KEYWORDS = os.getenv("TEST_JOB_KEYWORDS", 
        "test,testing,tst,demo,trial,experiment"
    ).split(",")
    
    # Database Settings
    DB_FILE = os.getenv("DB_FILE", "db/jenkins_data.db")
    
    # UI Settings
    DASHBOARD_TITLE = os.getenv("DASHBOARD_TITLE", "Jenkins Jobs and Pipelines Dashboard")
    PAGE_LAYOUT = os.getenv("PAGE_LAYOUT", "wide")
    
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