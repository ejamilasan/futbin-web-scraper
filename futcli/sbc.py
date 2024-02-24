import json
import sys
from bs4 import BeautifulSoup
from urls import get_html

scraperUrl = 'https://www.fut.gg/sbc'
htmlContent = get_html(scraperUrl)

def get_sbc_catalog():
    """
    Fetches the available SBC (Squad Building Challenges) catalog options such as 
    players, upgrades, icons, etc.
    
    Returns:
        list: A list of SBC catalog options.
    """

    if htmlContent:
        soup = BeautifulSoup(htmlContent, 'html.parser')
        sbc_links = soup.find_all('a', href=lambda href: href and '/sbc/' in href)
        sbc_options = {link['href'].split('/')[2].strip() for link in sbc_links}
        sbc_options_list = [option for option in sbc_options if option]
        return sbc_options_list
    return []

def get_sbc_items(link):
    """
    Extracts properties of an SBC (Squad Building Challenge) item from HTML.

    Args:
        link (BeautifulSoup Tag): A BeautifulSoup Tag representing an SBC item.

    Returns:
        dict: A dictionary containing properties of the SBC item including its 
        name, whether it's new, price, expiration, challenges, repeatable status, and refresh time.
    """

    sbc_name = link.find('h2').text.strip()
    new_element = link.find('div', class_='self-end').text.strip()
    new_item = 'yes' if 'new' in new_element.lower() else 'no'
    sbc_price = link.find('div', class_='self-end').text.replace('New', '').strip()
    sbc_expiration = link.find('span', string='Expires In').find_next_sibling('span').text.strip()
    sbc_challenges = link.find('span', string='Challenges').find_next_sibling('span').text.strip()
    sbc_repeatable = link.find('span', string='Repeatable').find_next_sibling('span').text.strip()
    sbc_refresh = link.find('span', string='Refreshes In').find_next_sibling('span').text.strip()

    return {
        "Name": sbc_name, 
        "New": new_item, 
        "Price": sbc_price, 
        "Expiration": sbc_expiration, 
        "Challenges": sbc_challenges, 
        "Repeatable": sbc_repeatable, 
        "Refreshes": sbc_refresh
    }

def get_sbc_data():
    """
    Fetches data for various SBC (Squad Building Challenge) items including their properties.

    Returns:
        dict: A dictionary where keys represent the SBC catalog options and values contain lists of 
        SBC items with their respective properties.
    """

    if htmlContent:
        soup = BeautifulSoup(htmlContent, 'html.parser')
        sbc_links = soup.find_all('div', class_='bg-dark-gray')
        sbc_data = {}

        for link in sbc_links:
            for catalog in get_sbc_catalog():
                if f'/sbc/{catalog}' in link.find('a')['href']:
                    sbc_data.setdefault(catalog, []).append(get_sbc_items(link))

        return sbc_data
    return {}
