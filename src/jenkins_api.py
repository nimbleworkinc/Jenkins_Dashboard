import requests
from urllib.parse import unquote
import streamlit as st
from datetime import datetime, timezone


def extract_folder_from_url(url):
    try:
        path = url.split("/job/")[1:]
        folder_path = "/".join(path[:-1])
        return unquote(folder_path) if folder_path else "/"
    except IndexError:
        return "/"


def is_test_job(job_name):
    """
    Simple test job detection with exclusion list.
    Add words to exclude_list to ignore them in test job detection.
    """
    if not job_name:
        return False
    
    job_name_lower = job_name.lower()
    
    # Add words here that should be ignored (not detected as test jobs)
    exclude_list = [
        "latest",
        "nightly-test",
        "nightly-test-delete",
        "nightly-test-deploy",
        "nightly-tests",
        "saastest",
        "attest",
        "contest",
        "detest",
        "protest",
        "suggest",
        "request",
        "rest",
        "nest",
        "west",
        "east",
        "best",
        "manifest",
        "testament",
        "testimony",
        "testosterone",
        "testicular",
        "testify",
        "testimonial",
        "testable",
        "tested"
    ]
    
    # Check if job name contains any excluded words
    for word in exclude_list:
        if word in job_name_lower:
            return False
    
    # Test job keywords to detect
    test_keywords = ["test", "testing", "tst", "demo", "trial", "experiment"] # "temp", "tmp", "poc"
    
    # Check if job name contains any test keywords
    for keyword in test_keywords:
        if keyword in job_name_lower:
            return True
    
    return False


@st.cache_data
def get_all_jenkins_items(url, _auth):
    items = []
    # Enhanced API call to get more detailed information
    api_url = (
        f"{url.rstrip('/')}/api/json?tree=jobs[name,url,_class,lastBuild[result,url,timestamp],"
        f"lastSuccessfulBuild[timestamp],lastFailedBuild[timestamp],builds[timestamp,result],"
        f"property[parameterDefinitions[name,defaultParameterValue[value]]],buildable,color]"
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
                    last_build_date = None
                    if last_build_timestamp:
                        last_build_date = datetime.fromtimestamp(last_build_timestamp/1000, tz=timezone.utc)
                else:
                    status = "Not Built"
                    build_url = ""
                    last_build_date = None
                
                # Get last successful build date
                last_successful_date = None
                if last_successful and last_successful.get("timestamp"):
                    last_successful_date = datetime.fromtimestamp(last_successful.get("timestamp")/1000, tz=timezone.utc)
                
                # Get last failed build date
                last_failed_date = None
                if last_failed and last_failed.get("timestamp"):
                    last_failed_date = datetime.fromtimestamp(last_failed.get("timestamp")/1000, tz=timezone.utc)
                
                # Calculate days since last build
                days_since_last_build = None
                if last_build_date:
                    days_since_last_build = (datetime.now(timezone.utc) - last_build_date).days
                
                # Get total build count and calculate success rate
                total_builds = len(builds) if builds else 0
                
                # Calculate success/failure rates from build history
                success_count = 0
                failure_count = 0
                success_rate = 0.0
                
                if builds:
                    for build in builds:
                        build_result = build.get("result")
                        if build_result == "SUCCESS":
                            success_count += 1
                        elif build_result in ["FAILURE", "UNSTABLE", "ABORTED"]:
                            failure_count += 1
                    
                    # Calculate success rate (only if there are builds)
                    if total_builds > 0:
                        success_rate = (success_count / total_builds) * 100
                
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
                    }
                )
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from {api_url}: {e}")
    return items
