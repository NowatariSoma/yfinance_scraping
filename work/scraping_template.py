import random, requests, time
from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent

def wait_random(second):
    second = second + random.random()
    time.sleep(second)
    
class set_driver:
    def __init__(self):
        download_path = '/home/seluser/Downloads'
        user_agent = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',\
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',\
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',\
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.3112.113 Safari/537.36'\
            ] 
        opts = webdriver.ChromeOptions()
        opts.add_argument("--disable-popup-blocking") 
        opts.add_experimental_option("prefs", {"download.default_directory": download_path, "download.prompt_for_download": False, 'profile.default_content_setting_values.automatic_downloads': 1})
        opts.add_argument('--user-agent=' + user_agent[random.randrange(0, len(user_agent), 1)])
        opts.add_argument('--lang=ja-JP')
        self.driver = webdriver.Remote(command_executor = 'http://selenium:4444/wd/hub', options = opts)
        self.driver.implicitly_wait(10)

    
    def go_url(self, url="https://www.yahoo.co.jp/", second=5):
        self.driver.get(url)
        wait_random(second)
        

class request_beautiful_soup:
    def __init__(self):
        self.ua = UserAgent()
        self.headers = {'user-agent':self.ua.chrome}
    
    def get_url(self,url):
        res = requests.get(url,headers=self.headers)
        return BeautifulSoup(res.text, "html.parser")
    
    def get_url_mojibake(self,url):
        res = requests.get(url,headers=self.headers)
        return BeautifulSoup(res.content, "html.parser")
    def return_response(self,url):
        return requests.get(url,headers=self.headers)

