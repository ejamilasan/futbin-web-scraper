import sys
from bs4 import BeautifulSoup
from tabulate import tabulate
from urls import get_html

BASE_URL = 'https://www.fut.gg/'

def get_sbc_options():
    """
    Fetches SBC options; ie. players, upgrades, icons, etc.
    """
    url = BASE_URL + 'sbc'
    html_content = get_html(url)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        sbc_links = soup.find_all('a', href=lambda href: href and '/sbc/' in href)
        sbc_options = {link['href'].split('/')[2].strip() for link in sbc_links}
        return list(sbc_options)
    return []

def get_sbc_items(link):
    """
    Parses HTML to get and SBC item's name, price, etc.
    """
    sbc_name = link.find('h2').text.strip()
    sbc_price = link.find('div', class_='self-end').text.replace('New', '').strip()
    sbc_expiration = link.find('span', string='Expires In').find_next_sibling('span').text.strip()
    sbc_challenges = link.find('span', string='Challenges').find_next_sibling('span').text.strip()
    sbc_repeatable = link.find('span', string='Repeatable').find_next_sibling('span').text.strip()
    sbc_refresh = link.find('span', string='Refreshes In').find_next_sibling('span').text.strip()

    new_element = link.find('div', class_='self-end').text.strip()
    new_item = 'yes' if 'new' in new_element.lower() else 'no'

    return [new_item, sbc_name, sbc_price, sbc_expiration, sbc_challenges, sbc_repeatable, sbc_refresh]

def get_sbc(option):
    """
    Fetches SBC items from the given Option
    """
    url = BASE_URL + 'sbc'
    html_content = get_html(url)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        sbc_links = soup.find_all('div', class_='bg-dark-gray')
        sbc_data = []

        for link in sbc_links:
            if f'/sbc/{option}' in link.find('a')['href']:
                sbc_data.append(get_sbc_items(link))

        return sbc_data
    return []

if __name__ == "__main__":
    if len(sys.argv) != 3:
        if len(sys.argv) == 2 and sys.argv[1].lower() == 'sbc':
            sbc_options = get_sbc_options()
            print('\n'.join(sbc_options))
        else:
            print("Usage: python3 fut_scraper.py sbc players")
        sys.exit(1)

    category = sys.argv[1].lower()
    option = sys.argv[2].lower()

    if category == 'sbc':
        sbc_data = get_sbc(option)
        if sbc_data:
            print(tabulate(sbc_data, headers=['New', 'Name', 'Price', 'Expiration', 'Challenges', 'Repeatable', 'Refreshes'], tablefmt='grid'))
        else:
            print("No SBC data available.")

