import scraping_template

def main():
    try:
        driver = scraping_template.set_driver()
        driver.go_url()
    finally:
        if 'driver' in locals():
            driver.driver.quit()
            del driver
    
    request_class = scraping_template.request_beautiful_soup()
    f = open('output.txt', 'w', encoding='cp932', errors='ignore')
    f.write(str(request_class.get_url('https://finance.yahoo.co.jp/cm/message/1006645/a5aaa5e0a5ma5s')))
    f.close()
    
if __name__ == "__main__":
    main()

