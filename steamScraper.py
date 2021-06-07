import requests 
import lxml.html
import json
from bs4 import BeautifulSoup
# from requests_html import HTMLSession
from multiprocessing.pool import ThreadPool
from multiprocessing import Pool
import pandas as pd
def steamScrapper():
    html = requests.get('https://store.steampowered.com/explore/new')
    doc = lxml.html.fromstring(html.content)
    new_releases = doc.xpath('//div[@id="tab_newreleases_content"]')[0]
    games_title = new_releases.xpath('.//div[@class="tab_item_name"]/text()')
    games_prices = new_releases.xpath('.//div[@class="discount_final_price"]/text()')
    test1 = new_releases.xpath('.//div[@class="tab_item_top_tags"]')
    tags= []
    # tags2 =[]
    for tag in test1:
        tags.append(tag.text_content())

    tags = [tag.split(',') for tag in tags ]
    games_os = new_releases.xpath('.//div[@class="tab_item_details"]')
    games_platform = []
    for tag in games_os:
        ## filter all the spans which has platform_img as its class attribute
        temp = tag.xpath('.//span[contains(@class, "platform_img")]')
        ## extract attribute of the tag; class attribute of a span
        platforms = [t.get('class').split(' ')[-1] for t in temp]
        print(platforms)
        if 'hmd_separator' in platforms:
            platforms.remove('hmd_separator')
        games_platform.append(platforms)
    output = []
    for info in zip(games_title, games_prices, tags, games_platform):
        tempInfo = {}
        tempInfo['title'] = info[0]
        tempInfo['price'] = info[1]
        tempInfo['tags'] = info[2]
        tempInfo['platforms'] = info[3]
        output.append(tempInfo)
    
def steamScrapperBS():    
    html = requests.get('https://store.steampowered.com/explore/new')
    soup = BeautifulSoup(html.text, 'lxml')
    target = soup.find('div', id='tab_newreleases_content')
    games_title = [game.text for game in target.findAll('div', class_='tab_item_name')]
    games_price = [price.text for price in target.findAll('div', class_='discount_final_price')]
    test1 = target.findAll('div', class_='tab_item_top_tags')
    tags = [tag.text for tag in test1]
    tags = [tag.split(',') for tag in tags]
    games_os = target.findAll('div', class_='tab_item_details')
    games_platform = []
    for tag in games_os:
        q = tag.findAll('span', class_='platform_img')
        platforms = [temp['class'][-1] for temp in q]
        if 'hmd_separator' in platforms:
            platforms.remove('hmd_separator')
        games_platform.append(platforms)
        
    output = []
    for info in zip(games_title, games_price, tags, games_platform):
        tempInfo = {}
        tempInfo['title'] = info[0]
        tempInfo['price'] = info[1]
        tempInfo['tags'] = info[2]
        tempInfo['platforms'] = info[3]
        output.append(tempInfo)
    print(output)
def scrapeEX1():
    html = requests.get('https://scrapingclub.com/exercise/detail_json/', headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'})
    doc = lxml.html.fromstring(html.content)
    target = doc.xpath('//div[@class="card-body"]')[0]
    target_title = target.xpath('.//h3[@class="card-title"]/text()')
    target_price = target.xpath('.//h4/text()')
    target_description = target.xpath('.//p[@class="card-text"]/text()')
    print(target_title, target_price, target_description)
    
    
def scrapeEX2BS():
    url = 'https://scrapingclub.com/exercise/detail_json/'

    session = HTMLSession()
    r = session.get(url)
    r.html.render()
    # print(r.html.find('.card-body .card-title', first=True).text)
    soup = BeautifulSoup(r.html.raw_html, 'lxml')
    target = soup.find('div', class_='card-body')
    print(target.find('h3', class_='card-title').text)
    print(target.find('h4', class_='card-price').text)
    print(target.find('p', class_='card-description').text)
    pass
def scrapeEX1BS():
    html = requests.get('https://scrapingclub.com/exercise/detail_basic/')
    doc = BeautifulSoup(html.text, 'lxml')
    target = doc.find('div', class_='card-body')
    print(target.find('h3', class_='card-title').text)
    print(target.find('h4').text)
    print(target.find('p', class_='card-text').text)

def scrapefreelancer():
    def scrapeP(item):
        name = item.find('li').find('div', class_='freelancer-details').find('div').find('h3').find('a').text.strip()
        pay_rate = item.find('li').find('div', class_='freelancer-details').find('span', class_='user-hourly-rate').text.strip()
        rating = item.find('li').find('div', class_='freelancer-details').find('div', class_='freelancer-card-stats').span['data-star_rating']
        earnings = item.find('li').find('div', class_='freelancer-details').find('div', class_='freelancer-card-stats').div['data-user_earnings']
        reviews = item.find('li').find('div', class_='freelancer-details').find('div', class_='freelancer-card-stats').find('span', 'Rating-review').a.text.strip()
        skills = [tag.text for tag in item.find('li').find('div', class_='freelancer-details').find('div', class_='top-skills').findAll('a')]
        # description = item.find('li').find('div', class_='freelancer-details').find('div', class_='bio truncProfile').span.text
        itemDict = {}
        itemDict['name'] = name
        # itemDict['description'] = description
        itemDict['skills'] = skills 
        itemDict['rating'] = rating
        itemDict['earnings'] = earnings
        itemDict['reviews'] = reviews   
        itemDict['pay_rate'] = pay_rate
        return itemDict
    def nextPage(url):
        listScrape = []
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'lxml')  
        target = soup.find('div', class_='freelancer-content')
        listFreelancers = target.findAll('div', class_='directory-freelancer-item-container')    
        for freelancer in listFreelancers:
            listScrape.append(scrapeP(freelancer))
        return listScrape
        
        pass
    url = 'https://www.freelancer.com/freelancers/australia'
    absoluteUrl = 'https://www.freelancer.com/freelancers/australia/{}'
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'lxml')
    target = soup.find('div', class_='freelancer-content')
    # target2 = target.findAll('ul', id='freelancer_list')
    listFreelancers = target.findAll('div', class_='directory-freelancer-item-container')
    lists = []
    for freelancer in listFreelancers:
        lists.append(scrapeP(freelancer))
    digits123 = [i for i in soup.find('div', class_='result-amount').text.strip().split(' ') if i.isdigit()]
    totals_result = int(''.join(digits123))
    # print(soup.select('div#display_div div.freelancer-content-inner'))
    for i in range(2, round(totals_result/ 10)+1):
        lists.extend(nextPage(absoluteUrl.format(i)))
    print(lists)

def scrapePagination():
    url = 'https://scrapingclub.com/exercise/list_basic/?page=1'
    absUrl = 'https://scrapingclub.com/exercise/list_basic/?page={}'
    html = requests.get(url)
    soup =BeautifulSoup(html.text, 'lxml')
    target = soup.select('div.row.my-4')[0]
    qqq = soup.findAll('ul', {'class': 'pagination'})[0].findAll('li',class_='page-item')
    scrapeList = []
    for i in range(1, len(qqq)):
        listPage= [ ]
        html = requests.get(absUrl.format(i))
        soup = BeautifulSoup(html.text, 'lxml')
        target = soup.select('div.row.my-4')[0]
        for item in target.select('div.col-lg-4'):
            item_name = item.select('div.card div.card-body')[0].h4.a.text
            item_price = item.select('div.card div.card-body')[0].h5.text
            item_dict = {}
            item_dict['name'] = item_name
            item_dict['price'] = item_price
            listPage.append(item_dict)
        scrapeList.append(listPage)
    print(scrapeList)
def scrapeDetail():
    def steps2(url):
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'lxml')
        target = soup.select('div.col-lg-8')[0]
        item_name = target.select('div.card div.card-body')[0].h3.text
        item_price = target.select('div.card div.card-body')[0].h4.text
        item_description = target.select('div.card div.card-body')[0].p.text
        item_dict ={}
        item_dict['name'] = item_name 
        item_dict['description'] = item_description
        item_dict['price'] = item_price
        return item_dict
    def scrape(url):
        listPage = []
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'lxml')
        target = soup.select('div.row.my-4')[0]
        for item in target.select('div.col-lg-4'):
            listPage.append(steps2(baseUrl.format(item.find('a')['href'])))
        return listPage
    # def multithreading(listUrls):
    #     mylist = []
    #     with ThreadPool(10) as pool:
    #         for result in pool.map(scrape, listUrls):
    #             mylist.append(result)
    #     print(mylist)
        
    
    url = 'https://scrapingclub.com/exercise/list_basic/?page=1'
    absUrl = 'https://scrapingclub.com/exercise/list_basic/?page={}'
    baseUrl = 'https://scrapingclub.com{}'
    html = requests.get(url)
    soup =BeautifulSoup(html.text, 'lxml')
    target = soup.select('div.row.my-4')[0]
    listItems = []
    
    
    # for item in target.select('div.col-lg-4'):
    #     listItems.append(steps2(baseUrl.format(item.find('a')['href'])))
    qqq = soup.findAll('ul', {'class': 'pagination'})[0].findAll('li',class_='page-item')
    listUrls = [absUrl.format(i) for i in range(1,len(qqq))]
    # multithreading(listUrls)
    
    
    ## not Multithreading 40s
    # for i in listUrls:
    #     listItems.extend(scrape(i))
    # print(listItems)
    
    ## Multithreading 9s
    with ThreadPool(10) as pool:
        for result in pool.map(scrape, listUrls):
            listItems.extend(result)
    df = pd.DataFrame(listItems)
    df.to_csv('randomMT.csv', index=False, mode='w+')

def scrapeAjax():
    html = requests.post('https://scrapingclub.com/exercise/ajaxdetail')
    soup = BeautifulSoup(html.text, 'lxml')
    print(json.loads(soup.text))


def scrapeLogin():
    url = 'https://scrapingclub.com/exercise/basic_login/'
    session = requests.Session() 
    tokencsrf = session.get(url).cookies['csrftoken']
    print(tokencsrf)
    headers={ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0',\
        'referer':'https://scrapingclub.com/exercise/basic_login/', 'origin': 'https://scrapingclub.com'}
    payload = {'name' : 'scrapingclub', 'password' : 'scrapingclub',  'csrfmiddlewaretoken' : tokencsrf,}

    response = session.post(url, data=payload, headers=headers)
    print(response)
# scrapeLogin()
def scrapeHead():
    url = 'https://scrapingclub.com/exercise/ajaxdetail_header/'
    session = requests.Session()
    headers={ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0',\
        'referer':'https://scrapingclub.com/exercise/detail_header/', 'origin': 'https://scrapingclub.com','x-requested-with': 'XMLHttpRequest'}
    response = session.get(url, headers=headers)
    print(response.text)

scrapeHead()