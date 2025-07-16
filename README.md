# Jenkins Dashboard

This Streamlit application provides a dashboard to view and analyze Jenkins jobs and pipelines.

## Features

- Fetches all jobs and pipelines from a Jenkins instance, including those in sub-folders.
- Caches the data locally in a SQLite database to speed up subsequent loads.
- Provides a web interface to view the data in a sortable and filterable table.
- Includes visualizations to show the distribution of last build statuses.
- Allows for quick navigation to jobs and their last builds via clickable links.

## Project Structure

```
.devops/
├── src/
│   ├── data_manager.py   # Handles database interactions
│   ├── jenkins_api.py    # Manages Jenkins API communication
│   └── ui.py             # Defines the Streamlit UI components
├── db/
│   └── jenkins_data.db   # SQLite database for caching
├── .env                # Stores Jenkins credentials and base URL
├── main.py             # Main application entry point
├── pyproject.toml      # Project metadata and dependencies
├── README.md           # This file
└── ...
```

## Setup and Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd devops
    ```

2.  **Create a virtual environment and install dependencies:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    pip install -e . # Or use `uv` if you have it
    ```

3.  **Create a `.env` file:**

    Create a file named `.env` in the root of the project and add your Jenkins credentials and base URL:

    ```
    JENKINS_USER=your-jenkins-username
    JENKINS_TOKEN=your-jenkins-api-token
    JENKINS_BASE_URL=https://your-jenkins-instance.com/
    ```

## How to Run

Once the setup is complete, you can run the Streamlit application with the following command:

```bash
streamlit run main.py
```

This will start the application and open it in your default web browser.
