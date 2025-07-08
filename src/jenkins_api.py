import requests
from urllib.parse import unquote
import streamlit as st


def extract_folder_from_url(url):
    try:
        path = url.split("/job/")[1:]
        folder_path = "/".join(path[:-1])
        return unquote(folder_path) if folder_path else "/"
    except IndexError:
        return "/"


@st.cache_data
def get_all_jenkins_items(url, _auth):
    items = []
    api_url = (
        f"{url.rstrip('/')}/api/json?tree=jobs[name,url,_class,lastBuild[result,url]]"
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
                if last_build:
                    status = last_build.get("result")
                    if status is None:
                        status = "IN_PROGRESS"
                    build_url = last_build.get("url")
                else:
                    status = "Not Built"
                    build_url = ""

                items.append(
                    {
                        "name": job.get("name"),
                        "url": job_url,
                        "type": job_class,
                        "last_build_status": status,
                        "last_build_url": build_url if build_url else "",
                        "folder": extract_folder_from_url(job_url),
                    }
                )
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from {api_url}: {e}")
    return items
