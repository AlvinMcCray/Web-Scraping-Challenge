# Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup

# Function to choose the executable path to driver
def init_browser():
    executable_path = {"executable_path": "C:/chromedriver/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

# Full Scrape function.
def scrape():

    """ NASA Mars News """

    # Run init_browser/driver.
    browser = init_browser()

    # Visit Nasa news url.
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)

    # HTML Object.
    html = browser.html

    # Parse HTML with Beautiful Soup
    news_soup = BeautifulSoup(html, "html.parser")

    # Retrieve the most recent article's title and paragraph.
    # Store in news variables.
    news_title = news_soup.find("div", class_="content_title").find('a').text
    news_paragraph = news_soup.find("div", class_="article_teaser_body").get_text()

    # Exit Browser.
    browser.quit()

    # Print Title and Text.
    print(f'Title: {news_title}\nText: {news_paragraph}')

    """ JPL Mars Space Images - Featured Image """

    # Run init_browser/driver.
    browser = init_browser()

    # Visit the url for JPL Featured Space Image.
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

    # Select "FULL IMAGE".
    browser.click_link_by_partial_text("FULL IMAGE")

    # Find "more info" for first image, set to variable, and command click.
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_element = browser.find_link_by_partial_text("more info")
    more_info_element.click()

    # HTML Object.
    html = browser.html

    # Parse HTML with Beautiful Soup
    image_soup = BeautifulSoup(html, "html.parser")

    # Scrape image URL.
    image_url = image_soup.find("figure", class_="lede").a["href"]

    # Concatentate https://www.jpl.nasa.gov with image_url.
    featured_image_url = f'https://www.jpl.nasa.gov{image_url}'

    # Exit Browser.
    browser.quit()

    # Print Faetured Image URL.
    print(featured_image_url)

    """ Mars Weather """

    # Run init_browser/driver.
    browser = init_browser()

    # Visit the url for Mars Weather twitter account.
    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)

    # HTML Object.
    html = browser.html

    # Parse HTML with Beautiful Soup
    weather_soup = BeautifulSoup(html, "html.parser")

    # Retrieve ALL 'ol' tags and save to variable 'tweets'.
    tweets = weather_soup.find_all('ol', class_='stream-items')
    # Iterate through all 'tweets' and find text in 'p' tag.
    # Break for most recent tweet if keyword 'InSight' in text.
    # Otherwise move onto next tweet.
    for tweet in tweets:
        mars_weather = tweet.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
        if 'InSight' in tweet:
            break
        else:
            continue

    # Exit Browser.
    browser.quit()

    # Remove 'anchor' tag text from "mars_weather" via split on 'pic'.
    mars_weather = mars_weather.split('pic')[0]

    # Replace '\n' with ' '.
    mars_weather = mars_weather.replace('\n', ' ')

    # Print most recent Mars Weather.
    print(mars_weather)

    """ Mars Facts """

    # URL for Mars Facts.
    facts_url = "https://space-facts.com/mars/"

    # Use Panda's `read_html` to parse the URL.
    facts_tables = pd.read_html(facts_url)

    # Required table stored in index "1".
    # Save as DF.
    df_mars_facts = facts_tables[1]

    # Rename columns.
    df_mars_facts.columns = ['Description', 'Value']

    # Set index to 'Description'.
    df_mars_facts.set_index('Description', inplace=True)

    # # Convert DF to html and save in Resources Folder.
    # df_mars_facts.to_html('Resources/mars_facts.html')

    # Convert DF to HTML string.
    mars_facts = df_mars_facts.to_html(header=True, index=True)

    """ Mars Hemispheres """

    # Run init_browser/driver.
    browser = init_browser()

    # Visit the url for USGS Astrogeology.
    astrogeo_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(astrogeo_url)

    # HTML Object.
    html = browser.html

    # Parse HTML with Beautiful Soup
    astrogeo_soup = BeautifulSoup(html, "html.parser")

    # Store main URL in a variable so that 'href' can be appended to it after each iteration.
    main_astrogeo_url = "https://astrogeology.usgs.gov"

    # Each link is located in 'div' tag, class "item".
    # Locate all 4 and store in variable.
    hems_url = astrogeo_soup.find_all("div", class_="item")

    # Create empty list for each Hemisphere URL.
    hemis_url = []

    for hem in hems_url:
        hem_url = hem.find('a')['href']
        hemis_url.append(hem_url)

    browser.quit()

    # Create list of dictionaries called hemisphere_image_urls.
    # Iterate through all URLs saved in hemis_url.
    # Concatenate each with the main_astrogeo_url.
    # Confirm the concat worked properly: confirmed.
    # Visit each URL.

    hemisphere_image_urls = []
    for hemi in hemis_url:
        hem_astrogeo_url = main_astrogeo_url + hemi
        print(hem_astrogeo_url)
        
        # Run init_browser/driver.
        browser = init_browser()
        browser.visit(hem_astrogeo_url)
        
        # HTML Object.
        html = browser.html

        # Parse HTML with Beautiful Soup
        hemi_soup = BeautifulSoup(html, "html.parser")

        # Locate each title and save to raw_title, to be cleaned.
        raw_title = hemi_soup.find("h2", class_="title").text
        
        # Remove ' Enhanced' tag text from each "title" via split on ' Enhanced'.
        title = raw_title.split(' Enhanced')[0]
        
        # Locate each 'full.jpg' for all 4 Hemisphere URLs.
        img_url = hemi_soup.find("li").a['href']
        
        # Append both title and img_url to 'hemisphere_image_url'.
        hemisphere_image_urls.append({'title': title, 'img_url': img_url})
        
        browser.quit()

    print(hemisphere_image_urls)

    """ Mars Data Dictionary - MongoDB """

    # Create empty dictionary for all Mars Data.
    mars_data = {}

    # Append news_title and news_paragraph to mars_data.
    mars_data['news_title'] = news_title
    mars_data['news_paragraph'] = news_paragraph

    # Append featured_image_url to mars_data.
    mars_data['featured_image_url'] = featured_image_url

    # Append mars_weather to mars_data.
    mars_data['mars_weather'] = mars_weather

    # Append mars_facts to mars_data.
    mars_data['mars_facts'] = mars_facts

    # Append hemisphere_image_urls to mars_data.
    mars_data['hemisphere_image_urls'] = hemisphere_image_urls

    print("Scrape Complete!!!")

    return mars_data