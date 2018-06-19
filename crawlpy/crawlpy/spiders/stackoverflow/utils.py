# -*- coding: utf-8 -*-
import re


def extract_job_id(url):
    job_id = re.findall(r'(?<=https:\/\/stackoverflow\.com\/jobs\/)(\d+)', url)
    return job_id[0] if job_id else ''


def clean_url(url):
    cleaned_url = re.findall(
        "https:\/\/stackoverflow\.com\/jobs\/\d+\/.*", url)
    if cleaned_url:
        return cleaned_url[0]
