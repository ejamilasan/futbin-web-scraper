import sys
import json
from datetime import datetime
from bs4 import BeautifulSoup
from urls import get_html

BASE_URL = 'https://www.fut.gg/'

def get_evolution_items(link):
    """
    Parses HTML to get the Evolution item's properties.
    """
    evolution_name = link.find('h2').text.strip()

    evolution_price_elem = link.find('div', class_='text-sm').text.strip() if link.find('div', class_='text-sm').text.strip() else 'FREE'
    evolution_price = '\n'.join(line.strip() for line in evolution_price_elem.split('\n') if line.strip())

    evolution_requirements_h3 = link.find('h3', string='Requirements').find_next('ul')
    evolution_requirements_list_items = evolution_requirements_h3.find_all('li')
    evolution_requirements = {item.find('span', class_='text-lightest-gray').text.strip(): item.find('span', class_='text-lighter-gray').text.strip() for item in evolution_requirements_list_items}

    evolution_upgrades_h3 = link.find('h3', string='Upgrades').find_next('ul')
    evolution_upgrades_list_items = evolution_upgrades_h3.find_all('li')
    evolution_upgrades = {item.find_next('span', class_='text-lightest-gray').text.strip(): item.find_next('span', class_='text-green').text.strip() for item in evolution_upgrades_list_items}
    
    evolution_expires_h3 = link.find('h3', string='Expires').find_next('time')
    evolution_expires_dt_str = evolution_expires_h3['datetime']
    evolution_expires = datetime.strptime(evolution_expires_dt_str, "%Y-%m-%dT%H:%M:%S.%f%z").strftime("%Y-%m-%d %H:%M:%S")

    evolution_levels = link.find('h3', string='Levels').find_next('div').text.strip()

    evolution_players = link.find('h3', string='# Players').find_next('div').text.strip()
    
    return {
        'Name': evolution_name,
        'Price': evolution_price,
        'Requirements': evolution_requirements,
        'Upgrades': evolution_upgrades,
        'Expiration': evolution_expires,
        'Levels': evolution_levels,
        'Players': evolution_players
    }

def get_evolutions():
    """
    Fetches Evolution items.
    """
    url = BASE_URL + 'evolutions'
    html_content = get_html(url)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        evolutions_links=soup.find_all('a', class_="rounded")
        evolutions_data = []

        for link in evolutions_links:
            evolutions_data.append(get_evolution_items(link))

        return evolutions_data
    return []

if __name__ == "__main__":
    category = sys.argv[1].lower()

    if category == 'evolutions':
        evolutions_data = get_evolutions()
        if evolutions_data:
            print(json.dumps(evolutions_data, indent=4))
        else:
            print("No Evolutions data available.")