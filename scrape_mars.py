#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import time


# In[2]:


# Set Executable Path & Initialize Chrome Browser (Windows path)
executable_path = {"executable_path": "./chromedriver.exe"}
browser = Browser("chrome", **executable_path)


# In[3]:


# Set Executable Path & Initialize Chrome Browser (MAC path)
# executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
# browser = Browser("chrome", **executable_path, headless=False)


# <b>NASA Mars News<b>

# In[4]:


# Visit the NASA Mars News Site
url = "https://mars.nasa.gov/news/"


# In[5]:


browser.visit(url)


# In[6]:


# Parse Results HTML with BeautifulSoup
html = browser.html
soup = bs(html, 'html.parser')


# In[7]:


# Scrape the Latest News Title
title_results = soup.find_all('div', class_='content_title')


# In[8]:


# Search for paragraph text under news titles
p_results = soup.find_all('div', class_='article_teaser_body')


# In[9]:


# Scrape the Latest Paragraph Text
news_title = title_results[0].text
news_p = p_results[0].text
print(news_title)
print(news_p)


# <b>JPL Mars Space Images - Featured Images<b>

# In[10]:


# Visit the JPL Featured Space Image
url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"


# In[11]:


browser.visit(url)


# In[12]:


# Click Button with Class Name full_image
browser.links.find_by_partial_text('FULL IMAGE')


# In[13]:


# Find "More Info" Button and Click It
time.sleep(2)
browser.links.find_by_partial_text('more info')


# In[14]:


# Parse Results HTML with BeautifulSoup
html = browser.html
soup1 = bs(html, "html.parser")


# In[18]:


# Retrieve Background Image
ft_image_url =  soup1.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]


# In[20]:


# Website Url 
image_url = 'https://www.jpl.nasa.gov'

# Concatenate website url with scrapped route & display
ft_image_url = image_url + ft_image_url
ft_image_url


# <b>Mars Facts<b>

# In[21]:


# Visit the Mars Facts Site Using Pandas to scrape data
mars_table_df = pd.read_html("https://space-facts.com/mars/")[0]


# In[22]:


mars_table_df.columns=["Description", "Value"]
mars_table_df.set_index("Description", inplace=True)
mars_table_df


# In[23]:


# Convert table to html
facts_table = [mars_table_df.to_html(classes='data table table-borderless', index=False, header=False, border=0)]
facts_table


# <b>Mars Hempisphere<b>

# In[24]:


# Visit the USGS Astrogeology Site
url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"


# In[25]:


browser.visit(url)


# In[26]:


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


# In[27]:


hemisphere_image_urls

