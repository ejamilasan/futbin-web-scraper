from bs4 import BeautifulSoup

from .urls import get_html

scraperUrl = "https://www.fut.gg/sbc"
htmlContent = get_html(scraperUrl)


def get_sbc_types():
    """Extract SBC types from HTML content."""
    if htmlContent:
        soup = BeautifulSoup(htmlContent, "html.parser")
        sbc_links = soup.find_all("a", href=lambda href: href and "/sbc/" in href)
        sbc_options = {link["href"].split("/")[2].strip() for link in sbc_links}
        sbc_options_list = [option for option in sbc_options if option]
        return sbc_options_list
    return []


def get_sbc_item_properties(link):
    """Extract properties of an SBC item from HTML."""
    sbc_name = link.find("h2").text.strip()
    new_element = link.find("div", class_="self-end").text.strip()
    new_item = "yes" if "new" in new_element.lower() else "no"
    sbc_price = link.find("div", class_="self-end").text.replace("New", "").strip()
    sbc_expiration = (
        link.find("span", string="Expires In").find_next_sibling("span").text.strip()
    )
    sbc_challenges = (
        link.find("span", string="Challenges").find_next_sibling("span").text.strip()
    )
    sbc_repeatable = (
        link.find("span", string="Repeatable").find_next_sibling("span").text.strip()
    )
    sbc_refresh = (
        link.find("span", string="Refreshes In").find_next_sibling("span").text.strip()
    )

    return {
        "Name": sbc_name,
        "New": new_item,
        "Price": sbc_price,
        "Expiration": sbc_expiration,
        "Challenges": sbc_challenges,
        "Repeatable": sbc_repeatable,
        "Refreshes": sbc_refresh,
    }


def get_sbc_items():
    """Extract SBC items and their properties."""
    if htmlContent:
        soup = BeautifulSoup(htmlContent, "html.parser")
        sbc_links = soup.find_all("div", class_="bg-dark-gray")
        sbc_data = {}

        for link in sbc_links:
            for sbc_type in get_sbc_types():
                if f"/sbc/{sbc_type}" in link.find("a")["href"]:
                    sbc_data.setdefault(sbc_type, []).append(
                        get_sbc_item_properties(link)
                    )

        return sbc_data
    return {}
