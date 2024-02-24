import requests


def get_html(url):
    """
    Fetches HTML content from the given URL.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
