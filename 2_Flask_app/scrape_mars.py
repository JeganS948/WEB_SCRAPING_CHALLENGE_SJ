# import dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import time

mission_to_mars_data = {}

def scrape_mars_info():

    # Set Executable Path & Initialize Chrome Browser (Windows path)
    executable_path = {"executable_path": "/bin/chromedriver"}
    browser = Browser("chrome", **executable_path)

    # Set Executable Path & Initialize Chrome Browser (MAC path)
    # executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    # browser = Browser("chrome", **executable_path, headless=False)


    # NASA Mars News
    # Visit the NASA Mars News Site
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    # Parse Results HTML with BeautifulSoup
    html = browser.html
    soup = bs(html, 'html.parser')

    # Scrape the Latest News Title
    title_results = soup.find_all('div', class_='content_title')

    # Search for paragraph text under news titles
    p_results = soup.find_all('div', class_='article_teaser_body')

    # Scrape the Latest Paragraph Text
    news_title = title_results[0].text
    news_p = p_results[0].text
    mission_to_mars_data['news_title'] = news_title
    mission_to_mars_data['news_paragraph'] = news_p


    # JPL Mars Space Images - Featured Images
    # Visit the JPL Featured Space Image
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    # Click Button with Class Name full_image
    browser.links.find_by_partial_text('FULL IMAGE')

    # Find "More Info" Button and Click It
    time.sleep(2)
    browser.links.find_by_partial_text('more info')

    # Parse Results HTML with BeautifulSoup
    html = browser.html
    soup1 = bs(html, "html.parser")

    # Retrieve Background Image
    ft_image_url =  soup1.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

    # Website Url 
    image_url = 'https://www.jpl.nasa.gov'

    # Concatenate website url with scrapped route & display
    ft_image_url = image_url + ft_image_url
    mission_to_mars_data['featured_image'] = ft_image_url


    # Mars Facts
    # Visit the Mars Facts Site Using Pandas to scrape data
    mars_table_df = pd.read_html("https://space-facts.com/mars/")[0]
    mars_table_df.columns=["Description", "Value"]
    mars_table_df.set_index("Description", inplace=True)
    mars_table_df

    # Convert table to html
    facts_table = mars_table_df.to_html(justify='left')
    mission_to_mars_data['mars_facts'] = facts_table


    # Mars Hempisphere
    # Visit the USGS Astrogeology Site
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    # hemisphere titles
    hemisphere_image_urls = []

    # Get a List of All the Hemispheres
    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}
    
    # Find Element on Each Loop to Avoid a Stale Element Exception
        browser.find_by_css("a.product-item h3")[item].click()
    
    # Find Sample Image Anchor Tag & Extract <href>
        sample_element = browser.links.find_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]
    
    # Get Hemisphere Title
        hemisphere["title"] = browser.find_by_css("h2.title").text

    # Append Hemisphere Object to List
        hemisphere_image_urls.append(hemisphere)
    
    # Navigate Backwards
        browser.back()
        mission_to_mars_data['mars_hemisphere'] = hemisphere_image_urls

    # Close browser after scraping
    browser.quit()
    print(mission_to_mars_data)
    
    # Return Results to dictionary
    return mission_to_mars_data
