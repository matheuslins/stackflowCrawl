import re


def extract_job_id(url):
    job_id = re.findall(r'(?<=https:\/\/stackoverflow\.com\/jobs\/)(\d+)', url)
    return job_id[0] if job_id else ''
