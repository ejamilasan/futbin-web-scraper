import sys
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

BASE_URL = 'https://www.fut.gg/'

def get_sbc_options():
    scrape_url = BASE_URL + 'sbc'
    response = requests.get(scrape_url)
    sbc_options = set()

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all <a> tags with href attribute containing "/sbc/"
        sbc_links = soup.find_all('a', href=lambda href: href and '/sbc/' in href)
        
        for link in sbc_links:
            option = link['href'].split('/')[2].strip()
            if option:
                sbc_options.add(option)

    else:
        print('Failed to retrieve the page. Status code:', response.status_code)

    return list(sbc_options)


def get_sbc(option):
    sbc_data = []
    scrape_url = BASE_URL + 'sbc'
    response = requests.get(scrape_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        sbc_links = soup.find_all('div', class_='bg-dark-gray')

        sbc_data = []

        for link in sbc_links:
            if f'/sbc/{option}' in link.find('a')['href']:
                new_element = sbc_price = link.find('div', class_='self-end').text.strip()
                if 'new' in new_element.lower():
                    new_item = 'yes'
                else:
                    new_item = 'no'
                sbc_name = link.find('h2').text.strip()
                sbc_price = link.find('div', class_='self-end').text.replace('New', '').strip()
                sbc_expiration = link.find('span', string='Expires In').find_next_sibling('span').text.strip()
                sbc_challenges = link.find('span', string='Challenges').find_next_sibling('span').text.strip()
                sbc_repeatable = link.find('span', string='Repeatable').find_next_sibling('span').text.strip()
                sbc_refresh = link.find('span', string='Refreshes In').find_next_sibling('span').text.strip()

                sbc_data.append([new_item, sbc_name, sbc_price, sbc_expiration, sbc_challenges, sbc_repeatable, sbc_refresh])

    else:
        print('Failed to retrieve the page. Status code:', response.status_code)

    return sbc_data

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

