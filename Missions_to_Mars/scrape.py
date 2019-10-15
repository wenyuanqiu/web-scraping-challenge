# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd


def scrape():
    # Make Results Dict
    results_dict = {}

    # Executable Path For Splinter
    executable_path = {'executable_path': r'C:\Users\wenyu\Documents\GitHub\web-scraping-challenge\Missions_to_Mars\chromedriver.exe'}

    # NASA Mars News ------------------------------------------------------------
    # This website is Javascript-Rendered.  Thus it requires splinter, not just requests
    url = 'https://mars.nasa.gov/news/'
    # If Error From Page Not Rendering- Keep Trying 
    keep_trying = True
    tries = 0

    while (keep_trying) & (tries < 20):
        
        # Visit url, get html, close
        browser = Browser('chrome', **executable_path, headless=False)
        browser.visit(url)
        html = browser.html
        browser.quit()
        
        # Create BeautifulSoup object; parse with 'html.parser'
        soup = BeautifulSoup(html, 'html.parser')
        
        try:
            # Get Title
            results = soup.find_all('div', class_="content_title")
            news_title = results[0].get_text()

            # Get Body
            results = soup.find_all('div', class_="article_teaser_body")
            news_p = results[0].get_text()

            keep_trying = False
        except:
            keep_trying = True
            tries += 1

    if keep_trying:
        print('Tries Exceeded- Failure')
        news_title = 'Nasa Website Sucks'
        news_p = 'Why Does NASA Website HTML Structure Change With Same URL?'

    results_dict['news_title'] = news_title
    results_dict['news_p'] = news_p

    # JPL Mars Space Images - Featured Image ------------------------------------------------------------
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    # Visit url, get html, close
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)
    html = browser.html
    browser.quit()
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')
    # Get Image Link
    results = soup.find_all('a', class_="button fancybox")
    featured_image_url  = 'https://www.jpl.nasa.gov/' + results[0]['data-fancybox-href']

    results_dict['featured_image_url'] = featured_image_url

    # Mars Weather------------------------------------------------------------
    url = 'https://twitter.com/marswxreport?lang=en'
    # Visit url, get html, close
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)
    html = browser.html
    browser.quit()
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')
    # Drop Unneeded Tags
    for a in soup("a"):
        a.decompose()
    # Get Tweet Contents
    results = soup.find_all('p', class_= 'tweet-text')
    mars_weather = results[0].get_text()
    results_dict['mars_weather'] = mars_weather

    # Mars Facts------------------------------------------------------------
    url = 'https://space-facts.com/mars/'
    mars_df_list = pd.read_html(url)
    # Get Second Table
    mars_df = mars_df_list[1]
    mars_df = mars_df.rename(columns={0:'Attribute',1:'Mars Fact'})
    path = 'mars_facts.html'
    mars_df.to_html(path, index=False)
    mars_df_html = mars_df.to_html(index=False)

    results_dict['mars_df_html'] = mars_df_html

    # Mars Hemispheres------------------------------------------------------------
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    # Visit url, get html, close
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(url)
    html = browser.html   
    browser.quit()

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    # Retrieve all Links
    results = soup.find_all('a', {'class', 'itemLink product-item'})

    # Get List of Unique Links To Visit
    links = []
    for result in results:
        link = result.get('href')
        links.append('https://astrogeology.usgs.gov/' + link)
    # Filter For Unique URLs
    links = list(set(links))

    hemisphere_image_urls = [None]*len(links)

    visits = 0
    # Visit Each URL
    for link in links:
        url = link
        hemisphere = link.split('/')
        hemisphere = hemisphere[len(hemisphere)-1]
        hemisphere = hemisphere.split('_')
        hemisphere_name = hemisphere[0]
        if len(hemisphere) > 2:
            hemisphere_name = hemisphere_name + ' ' + hemisphere[1]
        
        # Visit url, get html, close
        browser = Browser('chrome', **executable_path, headless=False)
        browser.visit(url)
        html = browser.html   
        browser.quit()
        
        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')

        # Retrieve all Jpg Links
        results = soup.find_all('div', {'class', 'downloads'})
        
        # Within Results, Filter Until a Jpg Link
        for result in results:
            sub_result = result.find_all('li')[0]
            jpg_link = sub_result.find('a').get('href')
            
        # Create New Dictionary Entry
        hemisphere_image_url = {'title': hemisphere_name.capitalize() + ' Hemisphere',
                            'img_url': jpg_link}
        
        # Extend List
        hemisphere_image_urls[visits] = hemisphere_image_url
        visits += 1

    results_dict['hemisphere_image_urls'] = hemisphere_image_urls

    return results_dict
