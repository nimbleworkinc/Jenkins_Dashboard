# Jenkins Dashboard Configuration Guide

## Overview

The Jenkins Dashboard application uses a professional configuration management system with environment variables and sensible defaults. This guide covers all available configuration options.

**💡 Reusability**: This codebase is designed to be reused for different Jenkins instances. Simply update the `.env` file with different credentials and dashboard titles for each Jenkins server.

**🔧 Single Source of Truth**: Default values are defined only in `config.py` to prevent inconsistencies. Environment variables in `.env` override these defaults when needed.

## Quick Setup

1. **Copy the example environment file:**
   ```bash
cp .env.example .env
   ```

2. **Edit your `.env` file** with your Jenkins credentials and preferences

3. **Restart the application** to apply changes

## Required Configuration

```bash
# Jenkins API Credentials
JENKINS_USER=your-jenkins-username
JENKINS_TOKEN=your-jenkins-api-token
JENKINS_BASE_URL=https://your-jenkins-instance.com/
```

## Optional Configuration

### Dashboard Display Settings

```bash
# Days threshold for inactive jobs (default: 60)
INACTIVE_JOB_THRESHOLD_DAYS=60

# Default items per page in data tables (default: 50)
ITEMS_PER_PAGE_DEFAULT=50

# Refresh interval in seconds (default: 300)
REFRESH_INTERVAL_SECONDS=300

# Dashboard title displayed in the UI
DASHBOARD_TITLE=Jenkins Dashboard

# Page layout (default: wide)
PAGE_LAYOUT=wide

# Timezone Settings
TIMEZONE=UTC
TIMEZONE_DISPLAY_FORMAT=%d %b %H:%M %Z
```

### Test Job Detection

```bash
# Words to exclude from test job detection (comma-separated)
# Default values are defined in config.py - only override if needed
# TEST_JOB_EXCLUDE_WORDS=latest,saastest,attest,contest,detest,protest,suggest,request,rest,nest,west,east,best,manifest,testament,testimony,testosterone,testicular,testify,testimonial,testable,tested

# Keywords that indicate test jobs (comma-separated)
# Default values are defined in config.py - only override if needed
# TEST_JOB_KEYWORDS=test,testing,tst,demo,trial,experiment
```

### Database Configuration

```bash
# Database type (default: sqlite)
# Options: sqlite, postgresql
DB_TYPE=sqlite

# Database file path for SQLite (default: db/jenkins_data.db)
DB_FILE=db/jenkins_data.db

# PostgreSQL Configuration (for production)
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=jenkins_dashboard
POSTGRES_USER=jenkins_user
POSTGRES_PASSWORD=jenkins_password_2024
```

## Database Setup

### PostgreSQL (Production)
```bash
# Start PostgreSQL container
docker-compose up -d postgres

# Configure .env for PostgreSQL
DB_TYPE=postgresql
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=jenkins_dashboard
POSTGRES_USER=jenkins_user
POSTGRES_PASSWORD=jenkins_password_2024
```

### SQLite (Development)
```bash
# Configure .env for SQLite
DB_TYPE=sqlite
DB_FILE=db/jenkins_data.db
```

### Database Management
- **pgAdmin**: http://localhost:8080 (admin@jenkins-dashboard.com / admin_password_2024)
- **Direct Access**: `docker exec jenkins_dashboard_db psql -U jenkins_user -d jenkins_dashboard`

## Environment-Specific Examples

### Development Environment
```bash
INACTIVE_JOB_THRESHOLD_DAYS=30
ITEMS_PER_PAGE_DEFAULT=25
DASHBOARD_TITLE=Jenkins Dev Dashboard
TIMEZONE=America/New_York
TIMEZONE_DISPLAY_FORMAT=%d %b %H:%M %Z
```

### Production Environment
```bash
INACTIVE_JOB_THRESHOLD_DAYS=90
ITEMS_PER_PAGE_DEFAULT=100
DASHBOARD_TITLE=Jenkins Production Dashboard
TIMEZONE=UTC
TIMEZONE_DISPLAY_FORMAT=%d %b %H:%M %Z
```

### High-Traffic Jenkins
```bash
INACTIVE_JOB_THRESHOLD_DAYS=120
ITEMS_PER_PAGE_DEFAULT=200
REFRESH_INTERVAL_SECONDS=600
DASHBOARD_TITLE=Jenkins Enterprise Dashboard
TIMEZONE=Europe/London
TIMEZONE_DISPLAY_FORMAT=%d %b %H:%M %Z
```

### Common Timezone Examples
```bash
# Universal Coordinated Time
TIMEZONE=UTC

# North America
TIMEZONE=America/New_York      # Eastern Time
TIMEZONE=America/Chicago       # Central Time
TIMEZONE=America/Denver        # Mountain Time
TIMEZONE=America/Los_Angeles   # Pacific Time

# Europe
TIMEZONE=Europe/London         # British Time
TIMEZONE=Europe/Paris          # Central European Time
TIMEZONE=Europe/Berlin         # Central European Time
TIMEZONE=Europe/Moscow         # Moscow Time

# Asia
TIMEZONE=Asia/Tokyo            # Japan Standard Time
TIMEZONE=Asia/Kolkata          # India Standard Time
TIMEZONE=Asia/Shanghai         # China Standard Time
TIMEZONE=Asia/Singapore        # Singapore Time

# Australia
TIMEZONE=Australia/Sydney      # Australian Eastern Time
TIMEZONE=Australia/Perth       # Australian Western Time
```

## Feature-Specific Configuration

### Cleanup Insights
- **Test Jobs**: Configure `TEST_JOB_KEYWORDS` and `TEST_JOB_EXCLUDE_WORDS`
- **Inactive Jobs**: Adjust `INACTIVE_JOB_THRESHOLD_DAYS` (default: 60 days)
- **Disabled Jobs**: Automatically detected, no configuration needed

### Analytics
- **Build Duration Analysis**: Automatically calculated from Jenkins data
- **Outlier Detection**: Uses statistical analysis, no configuration needed
- **Performance Insights**: Based on historical build data

### UI Customization
- **Dashboard Title**: Set `DASHBOARD_TITLE` for custom branding
- **Page Layout**: Use `PAGE_LAYOUT=wide` for full-width display
- **Items per Page**: Adjust `ITEMS_PER_PAGE_DEFAULT` for table pagination
- **Timezone**: Configure `TIMEZONE` for local time display (e.g., `America/New_York`, `Europe/London`)
- **Time Format**: Customize `TIMEZONE_DISPLAY_FORMAT` for timestamp display

## How to Change Configuration

### Method 1: Environment Variables (Recommended)
1. Edit your `.env` file
2. Add or modify configuration variables
3. Restart the application: `uv run streamlit run main.py`

### Method 2: System Environment Variables
```bash
export INACTIVE_JOB_THRESHOLD_DAYS=90
export ITEMS_PER_PAGE_DEFAULT=100
export DASHBOARD_TITLE="My Jenkins Dashboard"
uv run streamlit run main.py
```

## Configuration Validation

The application automatically validates required configuration on startup. If any required variables are missing, you'll see an error message with details.

## Benefits of This Approach

- ✅ **Environment-specific configuration**
- ✅ **No hardcoded values**
- ✅ **Easy to modify without code changes**
- ✅ **Professional best practices**
- ✅ **Version control friendly**
- ✅ **Team collaboration ready**
- ✅ **Dynamic configuration updates**

## Troubleshooting

### Configuration Error
If you see "Configuration Error", check:
1. `.env` file exists in project root
2. Required variables are set: `JENKINS_USER`, `JENKINS_TOKEN`, `JENKINS_BASE_URL`
3. No typos in variable names
4. No extra spaces around `=` in `.env` file

### Test Job Detection Issues
To adjust test job detection:
1. Add words to `TEST_JOB_EXCLUDE_WORDS` (comma-separated)
2. Modify `TEST_JOB_KEYWORDS` (comma-separated)
3. Clear cache and refresh data using the sync button

### Performance Issues
To improve performance:
1. Increase `ITEMS_PER_PAGE_DEFAULT` for fewer page loads
2. Increase `REFRESH_INTERVAL_SECONDS` to reduce API calls
3. Adjust `INACTIVE_JOB_THRESHOLD_DAYS` based on your cleanup needs

### UI Issues
- **Title not updating**: Ensure `DASHBOARD_TITLE` is set in `.env`
- **Layout problems**: Check `PAGE_LAYOUT` setting
- **Table pagination**: Adjust `ITEMS_PER_PAGE_DEFAULT`

## Reusing for Multiple Jenkins Instances

This codebase is designed to be easily reused for different Jenkins servers:

### Method 1: Separate .env Files
```bash
# For Jenkins Server 1
cp env_template.txt .env.jenkins1
# Edit .env.jenkins1 with server 1 credentials
DASHBOARD_TITLE=Jenkins Server 1 Dashboard
JENKINS_BASE_URL=https://jenkins1.company.com/

# For Jenkins Server 2  
cp env_template.txt .env.jenkins2
# Edit .env.jenkins2 with server 2 credentials
DASHBOARD_TITLE=Jenkins Server 2 Dashboard
JENKINS_BASE_URL=https://jenkins2.company.com/

# Run with specific config
cp .env.jenkins1 .env && uv run streamlit run main.py
```

### Method 2: Environment Variables
```bash
# Set environment variables for different servers
export DASHBOARD_TITLE="Jenkins Dashboard"
export JENKINS_BASE_URL="https://jenkins-cloud.company.com/"
export JENKINS_USER="cloud-user"
export JENKINS_TOKEN="cloud-token"
uv run streamlit run main.py
```

## Advanced Configuration

### Custom Test Job Detection
For complex test job detection rules, you can modify the logic in `src/jenkins_api.py`:

```python
# Current logic in jenkins_api.py
def is_test_job(job_name):
    # Exclude jobs with specific words
    for word in DashboardConfig.TEST_JOB_EXCLUDE_WORDS:
        if word.lower() in job_name.lower():
            return False
    
    # Include jobs with test keywords
    for keyword in DashboardConfig.TEST_JOB_KEYWORDS:
        if keyword.lower() in job_name.lower():
            return True
    
    return False
```

### Database Configuration
The SQLite database is automatically created in the `db/` directory. For production use, consider:
- Using a more robust database (PostgreSQL, MySQL)
- Implementing database migrations
- Adding backup strategies 