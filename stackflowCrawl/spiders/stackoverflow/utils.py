import re


def clean_url(url):
    cleaned_url = re.findall(
        "https:\/\/stackoverflow\.com\/jobs\/\d+\/.*", url)
    if cleaned_url:
        return cleaned_url[0]
