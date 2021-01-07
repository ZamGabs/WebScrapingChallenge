from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd

def init_browser():
     executable_path = {'executable_path': 'chromedriver.exe'}
     browser = Browser('chrome', **executable_path, headless=False)
     return browser

mars_data= {}
def mars_news_scrape():
     browser = init_browser()

     Nasa_url = 'https://mars.nasa.gov/news/'
     browser.visit(Nasa_url)
  
     html = browser.html

     Nasa_soup = bs(html, 'html.parser')


     nasa_news_title = Nasa_soup.find('div',class_='content_title').find('a').text
     print(f"title {nasa_news_title}")
     mars_data['nasa_news_title']=nasa_news_title
 
     nasa_news_paragraph=Nasa_soup.find('div',class_='article_teaser_body').text
     mars_data['nasa_news_paragraph'] = nasa_news_paragraph
  
     print(f"paragraph {nasa_news_paragraph}")

     return mars_data

def img_scrape():
     browser = init_browser()

     jplNasa_url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
     browser.visit(jplNasa_url)

     html = browser.html
     soup = bs(html, 'html.parser')


     main_url ='https://www.jpl.nasa.gov'

     featured_image_url = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]


     full_image_url=main_url+featured_image_url
     mars_data['full_image_url']= full_image_url
     print(full_image_url )     

     return mars_data

def mars_weather():
     browser = init_browser()

     Tweet_url='https://twitter.com/marswxreport?lang=en'
 
     browser.visit(Tweet_url)

     html=browser.html
     twit_soup=bs(html,'html.parser')

 
     mars_data['mars_weather'] = twit_soup.find('p',class_='TweetTextSize').text
 
     return mars_data

def mars_facts():
  
     mars_facts_url='https://space-facts.com/mars/'
     mars_fact_table=pd.read_html(mars_facts_url)

     df = mars_fact_table[0]
     df.columns = ['Mars-Earth Comparison', 'Mars', 'Earth']
     mars_facts = df.to_html()
     mars_data['mars_facts'] = mars_facts
     return mars_data

def mars_hem():

     browser = init_browser()

     USGS_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
     short_url="https://astrogeology.usgs.gov"

     browser.visit(USGS_url)
     html = browser.html
     soup = bs(html, 'html.parser')
     main_url = soup.find_all('div', class_='item')
     
     hemisphere_img_urls=[]      
     for x in main_url:
          title = x.find('h3').text
          url = x.find('a')['href']
          hem_img_url= short_url+url
      
          browser.visit(hem_img_url)
          html = browser.html
          soup = bs(html, 'html.parser')
          hemisphere_img_original= soup.find('div',class_='downloads')
          hemisphere_img_url=hemisphere_img_original.find('a')['href']
          
          print(hemisphere_img_url)
          img_data=dict({'title':title, 'img_url':hemisphere_img_url})
          hemisphere_img_urls.append(img_data)
     mars_data['hemisphere_img_urls']=hemisphere_img_urls
     return mars_data