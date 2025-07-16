# Jenkins Dashboard Configuration Guide

## Overview

The Jenkins Dashboard now uses a professional configuration management system with environment variables and sensible defaults.

## Quick Setup

1. **Copy your existing `.env` file** (if you have one)
2. **Add new configuration options** as needed
3. **Restart the application**

## Required Configuration

```bash
# .env file
JENKINS_USER=your-jenkins-username
JENKINS_TOKEN=your-jenkins-api-token
JENKINS_BASE_URL=https://your-jenkins-instance.com/
```

## Optional Configuration

### Dashboard Display Settings

```bash
# Days threshold for inactive jobs (default: 60)
INACTIVE_JOB_THRESHOLD_DAYS=60

# Default items per page (default: 50)
ITEMS_PER_PAGE_DEFAULT=50

# Refresh interval in seconds (default: 300)
REFRESH_INTERVAL_SECONDS=300
```

### Test Job Detection

```bash
# Words to exclude from test job detection
TEST_JOB_EXCLUDE_WORDS=latest,saastest,attest,contest,detest,protest,suggest,request,rest,nest,west,east,best,manifest,testament,testimony,testosterone,testicular,testify,testimonial,testable,tested

# Keywords that indicate test jobs
TEST_JOB_KEYWORDS=test,testing,tst,demo,trial,experiment
```

### Database and UI Settings

```bash
# Database file path (default: db/jenkins_data.db)
DB_FILE=db/jenkins_data.db

# Dashboard title
DASHBOARD_TITLE=Jenkins Jobs and Pipelines Dashboard

# Page layout (default: wide)
PAGE_LAYOUT=wide
```

## Environment-Specific Examples

### Development Environment
```bash
INACTIVE_JOB_THRESHOLD_DAYS=30
ITEMS_PER_PAGE_DEFAULT=25
```

### Production Environment
```bash
INACTIVE_JOB_THRESHOLD_DAYS=90
ITEMS_PER_PAGE_DEFAULT=100
```

### High-Traffic Jenkins
```bash
INACTIVE_JOB_THRESHOLD_DAYS=120
ITEMS_PER_PAGE_DEFAULT=200
REFRESH_INTERVAL_SECONDS=600
```

## How to Change Configuration

### Method 1: Environment Variables (Recommended)
1. Edit your `.env` file
2. Add or modify configuration variables
3. Restart the application

### Method 2: System Environment Variables
```bash
export INACTIVE_JOB_THRESHOLD_DAYS=90
export ITEMS_PER_PAGE_DEFAULT=100
streamlit run main.py
```

## Configuration Validation

The application automatically validates required configuration on startup. If any required variables are missing, you'll see an error message.

## Benefits of This Approach

- ✅ **Environment-specific configuration**
- ✅ **No hardcoded values**
- ✅ **Easy to modify without code changes**
- ✅ **Professional best practices**
- ✅ **Version control friendly**
- ✅ **Team collaboration ready**

## Troubleshooting

### Configuration Error
If you see "Configuration Error", check:
1. `.env` file exists in project root
2. Required variables are set
3. No typos in variable names

### Test Job Detection Issues
To adjust test job detection:
1. Add words to `TEST_JOB_EXCLUDE_WORDS`
2. Modify `TEST_JOB_KEYWORDS`
3. Clear cache and refresh data

### Performance Issues
To improve performance:
1. Increase `ITEMS_PER_PAGE_DEFAULT`
2. Increase `REFRESH_INTERVAL_SECONDS`
3. Adjust `INACTIVE_JOB_THRESHOLD_DAYS` 