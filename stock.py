from playwright.sync_api import sync_playwright

from bs4 import BeautifulSoup, NavigableString

import pandas as pd

url = 'https://www.tradingview.com/markets/stocks-india/sectorandindustry-industry/information-technology-services/'

def scrapData(stockpage):

    stockData = stockpage.find('tbody').find_all('tr')
    stockList=[st.find('a').attrs['href'] for st in stockData]
    print("Stock links extracted:", stockList)

    return stockList



def removeExtra_char(items):
    return(list(filter(lambda x : type(x)!= NavigableString,items)))


if __name__ == '__main__':
    with sync_playwright() as sp:
        browser = sp.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_load_state('networkidle')
        page.evaluate('()=> window.scroll(0,document.body.scrollHeight)')
        page.screenshot(path='information tech.png',full_page=True)
        pageData = page.inner_html('body')
        bsoup = BeautifulSoup(pageData, 'html.parser')

        stock_links = scrapData(bsoup)

        if stock_links is None:
            print("No stock links found. Exiting...")
        else:

            stock_base_url = "https://www.tradingview.com"

            for stock_link in stock_links:
                stock_url = stock_base_url + stock_link
                print(f"Visiting: {stock_url}")
                page.goto(stock_url, timeout=30000)
                page.wait_for_load_state('networkidle')

        
                browser.close()