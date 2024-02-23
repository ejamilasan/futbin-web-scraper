import sys
from bs4 import BeautifulSoup
from tabulate import tabulate
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
    evolution_requirements = ""

    for item in evolution_requirements_list_items:
        key = item.find('span', class_='text-lightest-gray').text.strip()
        value = item.find('span', class_='text-lighter-gray').text.strip()
        evolution_requirements += f"{key}: {value}\n"

    evolution_upgrades_h3 = link.find('h3', string='Upgrades').find_next('ul')
    evolution_upgrades_list_items = evolution_upgrades_h3.find_all('li')
    evolution_upgrades = ""

    for item in evolution_upgrades_list_items:
        key = item.find_next('span', class_='text-lightest-gray').text.strip()
        value = item.find_next('span', class_='text-green').text.strip()
        evolution_upgrades += f"{key}: {value}\n"

    return [evolution_name, evolution_price, evolution_requirements, evolution_upgrades]

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
            print(tabulate(evolutions_data, headers=['Name', 'Price', 'Requirements', 'Upgrades'], tablefmt='grid'))
        else:
            print("No Evolutions data available.")
