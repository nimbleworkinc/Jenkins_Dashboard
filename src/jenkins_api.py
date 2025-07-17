import requests
from urllib.parse import unquote
import streamlit as st
from datetime import datetime, timezone
from src.config import DashboardConfig


def extract_folder_from_url(url):
    try:
        path = url.split("/job/")[1:]
        folder_path = "/".join(path[:-1])
        return unquote(folder_path) if folder_path else "/"
    except IndexError:
        return "/"


def is_test_job(job_name):
    """
    Professional test job detection using configuration.
    Uses environment variables for exclude words and keywords.
    """
    if not job_name:
        return False
    
    job_name_lower = job_name.lower()
    
    # Check if job name contains any excluded words from config
    for word in DashboardConfig.TEST_JOB_EXCLUDE_WORDS:
        if word.strip() and word.strip() in job_name_lower:
            return False
    
    # Check if job name contains any test keywords from config
    for keyword in DashboardConfig.TEST_JOB_KEYWORDS:
        if keyword.strip() and keyword.strip() in job_name_lower:
            return True
    
    return False


@st.cache_data
def get_all_jenkins_items(url, _auth):
    items = []
    # Enhanced API call to get more detailed information including build duration
    api_url = (
        f"{url.rstrip('/')}/api/json?tree=jobs[name,url,_class,lastBuild[result,url,timestamp,duration],"
        f"lastSuccessfulBuild[timestamp,duration],lastFailedBuild[timestamp,duration],"
        f"builds[timestamp,result,duration],property[parameterDefinitions[name,defaultParameterValue[value]]],buildable,color]"
    )
    try:
        response = requests.get(api_url, auth=_auth)
        response.raise_for_status()
        data = response.json()
        for job in data.get("jobs", []):
            job_url = job.get("url")
            job_class = job.get("_class")
            if "folder" in job_class.lower():
                items.extend(get_all_jenkins_items(job_url, _auth))
            else:
                last_build = job.get("lastBuild")
                last_successful = job.get("lastSuccessfulBuild")
                last_failed = job.get("lastFailedBuild")
                builds = job.get("builds", [])
                
                # Determine if job is disabled (not buildable)
                is_disabled = not job.get("buildable", True)
                
                # Get last build info
                if last_build:
                    status = last_build.get("result")
                    if status is None:
                        status = "IN_PROGRESS"
                    build_url = last_build.get("url")
                    last_build_timestamp = last_build.get("timestamp")
                    last_build_duration = last_build.get("duration", 0)  # Duration in milliseconds
                    last_build_date = None
                    if last_build_timestamp:
                        last_build_date = datetime.fromtimestamp(last_build_timestamp/1000, tz=timezone.utc)
                else:
                    status = "Not Built"
                    build_url = ""
                    last_build_date = None
                    last_build_duration = 0
                
                # Get last successful build info
                last_successful_date = None
                last_successful_duration = 0
                if last_successful and last_successful.get("timestamp"):
                    last_successful_date = datetime.fromtimestamp(last_successful.get("timestamp")/1000, tz=timezone.utc)
                    last_successful_duration = last_successful.get("duration", 0)
                
                # Get last failed build info
                last_failed_date = None
                last_failed_duration = 0
                if last_failed and last_failed.get("timestamp"):
                    last_failed_date = datetime.fromtimestamp(last_failed.get("timestamp")/1000, tz=timezone.utc)
                    last_failed_duration = last_failed.get("duration", 0)
                
                # Calculate days since last build
                days_since_last_build = None
                if last_build_date:
                    days_since_last_build = (datetime.now(timezone.utc) - last_build_date).days
                
                # Get total build count and calculate success rate
                total_builds = len(builds) if builds else 0
                
                # Calculate success/failure rates and duration statistics from build history
                success_count = 0
                failure_count = 0
                success_rate = 0.0
                build_durations = []
                successful_durations = []
                failed_durations = []
                
                if builds:
                    for build in builds:
                        build_result = build.get("result")
                        build_duration = build.get("duration", 0)
                        
                        if build_duration > 0:  # Only include builds with valid duration
                            build_durations.append(build_duration)
                            
                            if build_result == "SUCCESS":
                                success_count += 1
                                successful_durations.append(build_duration)
                            elif build_result in ["FAILURE", "UNSTABLE", "ABORTED"]:
                                failure_count += 1
                                failed_durations.append(build_duration)
                    
                    # Calculate success rate (only if there are builds)
                    if total_builds > 0:
                        success_rate = (success_count / total_builds) * 100
                
                # Calculate duration statistics
                avg_build_duration = sum(build_durations) / len(build_durations) if build_durations else 0
                avg_successful_duration = sum(successful_durations) / len(successful_durations) if successful_durations else 0
                avg_failed_duration = sum(failed_durations) / len(failed_durations) if failed_durations else 0
                min_build_duration = min(build_durations) if build_durations else 0
                max_build_duration = max(build_durations) if build_durations else 0
                
                # Use simple test job detection with exclusion list
                job_name = job.get("name", "")
                is_test_job_result = is_test_job(job_name)

                items.append(
                    {
                        "name": job_name,
                        "url": job_url,
                        "type": job_class,
                        "last_build_status": status,
                        "last_build_url": build_url if build_url else "",
                        "folder": extract_folder_from_url(job_url),
                        "is_disabled": is_disabled,
                        "last_build_date": last_build_date,
                        "last_successful_date": last_successful_date,
                        "last_failed_date": last_failed_date,
                        "days_since_last_build": days_since_last_build,
                        "total_builds": total_builds,
                        "success_count": success_count,
                        "failure_count": failure_count,
                        "success_rate": success_rate,
                        "is_test_job": is_test_job_result,
                        # Duration data
                        "last_build_duration": last_build_duration,
                        "last_successful_duration": last_successful_duration,
                        "last_failed_duration": last_failed_duration,
                        "avg_build_duration": avg_build_duration,
                        "avg_successful_duration": avg_successful_duration,
                        "avg_failed_duration": avg_failed_duration,
                        "min_build_duration": min_build_duration,
                        "max_build_duration": max_build_duration,
                        "total_build_duration": sum(build_durations) if build_durations else 0,
                    }
                )
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from {api_url}: {e}")
    return items
