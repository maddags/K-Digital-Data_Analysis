from urllib import response
import selenium
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
# import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import requests
# from mini_pjt1.models import tour

# slack 설정
SLACK_BOT_TOKEN = "xoxb-3056784928007-3667341064962-PWILLKFdGk94c5sLWrgRhNKC"
# slack_token = WebClient(token=SLACK_BOT_TOKEN)
slack_channel = "korea_visit_info_scraping"

# driver 오류
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

url = "https://korean.visitkorea.or.kr/search/search_list.do?keyword="
keyword = "강원도"
search_url = url + keyword
driver = webdriver.Chrome("../chromedriver.exe",options=options)
driver.get(search_url)

driver.find_element_by_css_selector(".search_menu li#tabView2").click()
driver.find_element_by_xpath('//*[@id="2"]').click()
time.sleep(2)
article_list = driver.find_elements_by_css_selector(".search_body ul li div.area_txt div.tit a")

## javascript 제거하고 url 가져오기
url_list = []
for article in article_list:
    try :
        article_url = article.get_attribute("href")
        article_url = article_url[27::]
        article_url = article_url[0:36]
        url_list.append(article_url)
    except : 
        continue


# 기사 url로 들어가기
article_url = "https://korean.visitkorea.or.kr/detail/rem_detail.do?cotid="

for article in url_list:
    driver.get(article_url + article)
    time.sleep(2)

    # 제목
    title = driver.find_element_by_css_selector("#topTitle").text
    loc = driver.find_element_by_css_selector("#topAddr span:nth-child(1)").text
    date = driver.find_element_by_css_selector("#topAddr span:nth-child(2)").text[6::]
    likeCnt = driver.find_element_by_css_selector("#conLike").text
    shareCnt = driver.find_element_by_css_selector("#conShare").text
    readCnt = driver.find_element_by_css_selector("#conRead").text
    
    
    # slack으로 메세지 보내기
    message = f"{title}{date}"
    def post_message(token,channel,message):
        response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": message}
        )
        print(response)
    
    post_message(SLACK_BOT_TOKEN,slack_channel,message)
    # tour(title = title, loc = loc, date = date, likeCnt=likeCnt, shareCnt= shareCnt,readCnt=readCnt).save()
    try:
            cards = driver.find_elements_by_css_selector('.summary_info .card')
            i = 0
            img_urls = ""
            summary_info = ""
            for card in cards:
                i=i+1
                #img링크 가져오기
                select1 = '.swiper-wrapper li:nth-child({i})'
                select1 = select1.format(i=i)
        
                img_url = driver.find_element_by_css_selector(select1).get_attribute('style')
                img_url = img_url[22:-2]
                img_urls = img_urls + img_url
                
                #요약 글 가져오기
                #mouse hover 코드 : webdriver.ActionChains(driver).move_to_element(element).perform()
                webdriver.ActionChains(driver).move_to_element(card).perform() 
                time.sleep(2)
                select = 'li:nth-child({i}) .card .view_cont p'
                select = select.format(i=i)
                sumText = driver.find_element_by_css_selector(select)
                summary_info = summary_info + sumText.text
                # print(img_urls)
                # print(summary_info)
            
        
    except:
        print("X")