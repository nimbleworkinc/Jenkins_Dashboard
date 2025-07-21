# Jenkins Dashboard

A comprehensive Streamlit application for monitoring and analyzing Jenkins jobs and pipelines with advanced insights and cleanup recommendations.

## Features

- **📊 Dashboard Overview**: Real-time monitoring of all Jenkins jobs and pipelines with success/failure rates
- **🧹 Cleanup Insights**: Identify test jobs, inactive jobs (>60 days), and disabled pipelines for cleanup
- **📈 Advanced Analytics**: Build duration analysis, performance insights, and outlier detection
- **🔍 Smart Filtering**: Search by job name, folder, or status with multi-select filters
- **📱 Modern UI**: Clean, professional interface with responsive design
- **💾 Local Caching**: SQLite database for fast data access and offline viewing
- **🔄 Data Sync**: Manual refresh capability with confirmation modal
- **📊 Visualizations**: Interactive charts and graphs for data analysis
- **📋 Export Functionality**: Download data in CSV format

## Project Structure

```
Jenkins_Dashboard/
├── src/
│   ├── config.py         # Configuration management with environment variables
│   ├── data_manager.py   # SQLite database operations and caching
│   ├── jenkins_api.py    # Jenkins API communication and data fetching
│   └── ui.py             # Streamlit UI components and visualizations
├── db/
│   └── jenkins_data.db   # SQLite database for cached Jenkins data
├── .env                  # Environment variables (not in git)
├── env_template.txt      # Environment variables template
├── main.py               # Application entry point
├── pyproject.toml        # Project dependencies and metadata
├── README.md             # This file
├── CONFIGURATION.md      # Detailed configuration guide
└── .gitignore           # Git ignore rules
```

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Jenkins_Dashboard
   ```

2. **Create virtual environment and install dependencies:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e .
   ```

3. **Set up environment variables:**
   ```bash
   cp env_template.txt .env
   # Edit .env with your Jenkins credentials and other configuration as mentioned in CONFIGURATION.md file
   ```

4. **Run the application:**
   ```bash
   streamlit run main.py
   ```

```

## Key Features Explained

### 📊 Dashboard Overview
- **KPI Cards**: Total jobs, success rate, failure rate, average build duration
- **Build Status Distribution**: Visual breakdown of job statuses
- **Jobs by Folder**: Distribution of jobs across folders
- **Interactive Data Table**: Sortable, filterable job list with pagination

### 🧹 Cleanup Insights
- **Test Jobs**: Identifies jobs with test-related keywords (excluding common words)
- **Inactive Jobs**: Shows jobs not triggered for configurable days (default: 60)
- **Disabled Jobs**: Lists all disabled pipelines
- **Cleanup Recommendations**: Actionable suggestions for each job type

### 📈 Advanced Analytics
- **Build Duration Analysis**: Statistical analysis of build times
- **Outlier Detection**: Identifies jobs with unrealistic build durations
- **Performance Insights**: Success rate trends and build frequency analysis

## Dependencies

- **Streamlit** (>=1.46.1): Web application framework
- **Pandas** (>=2.3.1): Data manipulation and analysis
- **Plotly** (>=6.2.0): Interactive visualizations
- **Requests** (>=2.32.4): HTTP requests for Jenkins API
- **Python-dotenv** (>=1.1.1): Environment variable management

## Reusability

This codebase is designed to be reused for different Jenkins instances. Simply update the `.env` file with different credentials and dashboard titles for each Jenkins server. See [CONFIGURATION.md](CONFIGURATION.md) for detailed examples.

## Support

For detailed configuration options and troubleshooting, see [CONFIGURATION.md](CONFIGURATION.md).
