#!/usr/bin/env python
# coding: utf-8

# # Linkedin Scraper 
# 

# ### Requirements

# In[15]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from bs4 import BeautifulSoup 
import re as re
import time
import pandas as pd
from pandas import ExcelWriter


# ### Getting All Pages

# In[2]:


search=input('enter field u want to search for people')
pages=[]
url=f'https://www.linkedin.com/search/results/people/?keywords={search}&origin=SWITCH_SEARCH_VERTICAL&page='
for i in range(1,101):
    pages.append(url+str(i))
# pages


# ### Login to Linkdin and seach

# In[3]:


PATH = r'C:\Users\rohit\Documents\projects\chromedriver.exe'
driver = webdriver.Chrome(PATH)
driver.get("https://www.linkedin.com/uas/login")
time.sleep(3)
email=driver.find_element_by_id("username")
email.send_keys('rohith.muthyala29@gmail.com')
password=driver.find_element_by_id("password")
password.send_keys('Rohith291997')
time.sleep(3)
password.send_keys(Keys.RETURN)
# code=driver.find_element_by_id('input__email_verification_pin').send_keys('enter ur keys')   if ask for code
# submit=driver.find_element_by_id('email-pin-submit-button').click()
# skip=driver.find_element_by_xpath('//*[@id="ember455"]/button').click()
search=driver.find_element_by_id('global-nav-search')
search.click()
enter=driver.find_element_by_xpath('//*[@id="global-nav-typeahead"]/input')
enter.send_keys('python')
enter.send_keys(Keys.ENTER)


# In[4]:


driver.find_element_by_css_selector("button[aria-label='People']").click()


# ### Getting WebPage With Scrole

# In[6]:


def get_webpage(page):
    driver.get(page)
    
    last_height = driver.execute_script('return document.body.scrollHeight')
    for i in range(3):
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(5)
        new_height = driver.execute_script('return document.body.scrollHeight')
        last_height = new_height
        
    soup = BeautifulSoup(driver.page_source, 'lxml')
    return soup


# ### Get People Data From Every Page

# In[12]:


def get_people_data(page):
    datalist={
        'Name':[],
        'Region':[],
        'Job':[],
        'ImgUrl':[],
        'IdLink':[]
    }
    for i in range(3):
        soup=get_webpage(page[i])
        imgs=soup.find_all('li',{'class':'reusable-search__result-container'})
    
        name=soup.find_all('span',{'dir':'ltr'})
    
        job=soup.find_all('div',{'class':'entity-result__primary-subtitle t-14 t-black'})
    
        people_links=soup.find_all('div',{'class':'t-roman t-sans'})
        region=soup.find_all('div',{'class':'entity-result__secondary-subtitle t-14'})
        for j in range(10):
            datalist['Name'].append(name[j].span.text)
            datalist['Region'].append(region[j].text.strip())
            datalist['Job'].append(job[j].text.strip())
            if imgs[j].img != None:
                datalist['ImgUrl'].append(imgs[j].img['src'])
            else:
                datalist['ImgUrl'].append('NO Image Uploaded')
                
            datalist['IdLink'].append(people_links[j].a['href'].split('?')[0])
            
    return datalist


# In[20]:


data=get_people_data(pages)


# ## Make DataFarame

# In[14]:


linkdin_df=pd.DataFrame(data)
linkdin_df=linkdin_df.shift()[1:]
linkdin_df


# ### Save To Excel Sheet

# In[52]:


writer = ExcelWriter('LinkdinPeopleSearchPython.xlsx')
linkdin_df.to_excel(writer,'Sheet5' , index=(1,))
writer.save()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




