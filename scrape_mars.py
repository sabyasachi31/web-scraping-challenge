import pandas as pd
import requests
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    url='https://redplanetscience.com'
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    browser.visit(url)
    html=browser.html
    soup=bs(html,'html.parser')
    results=soup.find_all('div',class_='list_text')

    serial=1
    for result in results:
        news_title=result.find('div', class_='content_title').text
        news_p=result.find('div',class_='article_teaser_body').text
        serial=serial+1
        if serial==2:
            break

    jpl_url='https://spaceimages-mars.com'
    browser.visit(jpl_url)
    html=browser.html
    soup=bs(html,'html.parser')
    results=soup.find('div',class_='floating_text_area')

    link=results.find('a',class_='showimg fancybox-thumbs')
    featured_image_url=link['href']
    featured_image_url=jpl_url+'/'+featured_image_url

    facts_url='https://galaxyfacts-mars.com'

    tables=pd.read_html(facts_url)
    mars_df=tables[0]
    mars_df=mars_df.rename(columns={0: 'Description', 1: 'Mars',2:'Earth'})
    mars_df=mars_df.set_index(['Description'])


    mars_table=mars_df.to_html(classes=["table", "table-bordered"])
    
    #mars_df.to_html('mars_table.html',classes=["table", "table-bordered"])

    hem_url='https://marshemispheres.com'
    browser.visit(hem_url)
    html=browser.html
    soup=bs(html,'html.parser')

    browser.visit(hem_url)
    img_url=[]
    title=[]

    html=browser.html
    soup=bs(html,'html.parser')
    results=soup.find_all('div', class_='description')

    for result in results:
        link=result.find('a', class_='itemLink product-item')
        x=hem_url+'/'+link['href']
        img_url.append(x)
        
        y=result.find('h3').text
        title.append(y)

    full_url=[]
    for url in img_url:
        browser.visit(url)
        html=browser.html
        soup=bs(html,'html.parser')
        result=soup.find('img',class_='wide-image')
        x=hem_url+'/'+result['src']
        full_url.append(x)
    
    l=len(title)
    dict_hem={}
    hemisphere_image_urls=[]
    for i in range(l):
        dict_hem={"title":title[i],
                "img_url":full_url[i]}
        hemisphere_image_urls.append(dict_hem)
    
    final_dict={}

    final_dict["news_title"]=news_title
    final_dict["news_p"]=news_p
    final_dict["featured_image_url"]=featured_image_url
    final_dict["mars_facts"]=mars_table
    final_dict["mars_hemispheres"]=hemisphere_image_urls

    browser.quit()

    return final_dict










