from requests_html import HTMLSession
from bs4 import BeautifulSoup
from datetime import datetime
import sys

def get_data(url):
    r = session.get(url)
    r.html.render(sleep=1)
    soup = BeautifulSoup(r.html.html, 'html.parser')
    return soup

def get_deals(soup):
    results = []
    products = soup.find_all("div", {"data-component-type": "s-search-result"})
    for product in products:
        title = product.find("a", class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal").text.strip()
        short_title = title[:30]
        
        link = product.find("a", class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")["href"]
        link = "https://www.amazon.com.au" + link
        
        try:
            price = product.find("span", class_="a-offscreen").text.strip()
        except:
            price = "No featured offers available"
        
        try:
            reviews = product.find("span", class_="a-size-base s-underline-text").text.strip()
        except:
            reviews = "No reviews..."
        
        try:
            rating = product.find("span", class_="a-icon-alt").text.strip()
        except:
            rating = "No ratings..."
        
        results.append({
            "title": title,
            "short_title": short_title,
            "link": link,
            "price": price,
            "reviews": reviews,
            "rating": rating
        })
    return results    

def get_next_page(soup):
    pages = soup.find(class_="s-pagination-strip")
    try:
        url = "https://www.amazon.com.au" + str(pages.find("a", class_="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator")["href"])
        return url
    except:
        return

def sort_results(results, sort_by):
    match sort_by:
        case "-p":
            sorted_results = sorted(results, key=lambda d: d["price"])
        case "-pr":
            sorted_results = sorted(results, key=lambda d: d["price"], reverse=True)
        case "-r":
            results = filter((lambda d: d["rating"] != "No ratings..."), results)
            sorted_results = sorted(results, key=lambda d: d["rating"], reverse=True)
        case "-n":
            results = filter((lambda d: d["rating"] != "No reviews..."), results)
            sorted_results = sorted(results, key=lambda d: d["reviews"], reverse=True)
    return sorted_results

if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise Exception("Usage: python3 amazon_deals.py [-p[r] | -r | -n] req1 req2")
    
    if sys.argv[1] in ["-p", "-pr", "-r", "-n"]:
        sort_by = sys.argv[1]
        no_of_results = int(sys.argv[2])
        search_term = "+".join(sys.argv[3:])
    else:
        sort_by = "-r"
        no_of_results = sys.argv[1]
        search_term = "+".join(sys.argv[2:])

    session = HTMLSession()
    url = f"https://www.amazon.com.au/s?k={search_term}"
    all_products = []

    while True:
        soup = get_data(url)
        all_products.extend(get_deals(soup))
        url = get_next_page(soup)
        if not url:
            break

    sorted_products = sort_results(all_products, sort_by)

    if no_of_results > len(all_products):
        no_of_results = len(all_products)

    for product in range(no_of_results):
        for _ in sorted_products[product].items():
            print(f"{_[0]}: {_[1]}")
        print("\n")