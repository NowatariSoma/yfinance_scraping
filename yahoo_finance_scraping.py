import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import pandas as pd

def setup_driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    
    # ウェブドライバのプロパティを削除するためのスクリプト
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    driver = webdriver.Chrome(service=service, options=options)
    
    # webdriverプロパティを削除
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def load_page(driver, url):
    driver.get(url)
    last_height = driver.execute_script("return document.body.scrollHeight")
    tmp = 0 # テスト用
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # 必要に応じて調整
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        tmp += 1 # テスト用
        if tmp == 1: # テスト用
            break # テスト用
    return driver.page_source

# def check_headless_chrome(driver):
#     script = """
#     return new Promise(resolve => {
#         navigator.permissions.query({name:'notifications'}).then(function(permissionStatus) {
#             if(Notification.permission === 'denied' && permissionStatus.state === 'prompt') {
#                 resolve("Headless Chrome");
#             } else {
#                 resolve("Not Headless Chrome");
#             }
#         });
#     });
#     """
#     return driver.execute_async_script(script)

def extract_comments(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    comment_list = soup.select_one('#cmtlst')
    comment_all = []
    if comment_list:
        comments = comment_list.find_all('li')
        for comment in comments:
            now_comment = {}
            try:
                now_comment["comment_id"] = comment.find('span', {'class': 'comNum'}).get_text(strip=True)
                now_comment["date"] = comment.find('p', {'class': 'comWriter'}).find('span').get_text(strip=True)
                now_comment["name"] = comment.find('p', {'class': 'comWriter'}).find('a').get_text(strip=True)
                now_comment["text"] = comment.find('p', {'class': 'comText'}).get_text(strip=True)
            except AttributeError:
                continue
            comment_all.append(now_comment)
    else:
        print("そもそも、コメントが見つかりませんでした。指定先を間違えている間抜け。")
        return None
    return comment_all

def generate_url(base_url):
    urls = [f"{base_url}/{i+16}" for i in range(10)] # テスト用
    # urls = [f"{base_url}/{i+1}" for i in range(999)]
    urls.insert(0, base_url)
    return urls

def remove_non_shift_jis(text):
    """
    Shift-JISにエンコードできない文字を削除する関数
    """
    try:
        return text.encode('shift_jis', errors='ignore').decode('shift_jis')
    except Exception as e:
        return text

def main():
    base_url = 'https://finance.yahoo.co.jp/cm/message/1006645/a5aaa5e0a5ma5s'
    
    driver = setup_driver()
    urls = generate_url(base_url)
    print(urls)
    all_comments = []
    try:
        for url in urls:
            print(f"Processing URL: {url}")
            page_source = load_page(driver, url)
            comments = extract_comments(page_source)
            if comments is None:
                break  # コメントが取得できなかったらループを抜ける
            all_comments.extend(comments)
    finally:
        driver.quit()
    
    # # 取得したコメントを表示
    # for comment in all_comments:
    #     print(comment)

    # # JSONデータをパースしてデータフレームに変換
    # df = pd.DataFrame(all_comments)
    # # CSVに出力
    # df.to_csv('output.csv', index=False)

    # 各コメントのフィールドに対してShift-JISにエンコードできない文字を削除
    cleaned_comments = []
    for comment in all_comments:
        cleaned_comment = {key: remove_non_shift_jis(value) if isinstance(value, str) else value for key, value in comment.items()}
        cleaned_comments.append(cleaned_comment)

    # cleaned_commentsをデータフレームに変換
    df = pd.DataFrame(cleaned_comments)

    # CSVにShift-JISエンコードで出力
    df.to_csv('output.csv', index=False, encoding='shift_jis')


if __name__ == "__main__":
    main()