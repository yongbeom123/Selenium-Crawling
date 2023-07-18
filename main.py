from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
from multiprocessing import Pool

def initialize_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 창을 띄우지 않고 실행
    options.add_argument('--no-sandbox')  # root 권한 없이 실행
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(executable_path='/path/to/chromedriver', options=options) # chromedriver 경로 설정
    return driver

def crawl_naver_place(place_name):
    try:
        driver = initialize_driver()
        search_url = f'https://map.naver.com/v5/search/{place_name}'
        driver.get(search_url)
        time.sleep(3)  # 페이지가 로드되기 위한 대기 시간

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        place_info = soup.find('div', class_='panel_basic')

        if place_info:
            place_name = place_info.find('h2', class_='search_title').text.strip()
            address = place_info.find('span', class_='address').text.strip()
            phone_number = place_info.find('span', class_='phone').text.strip()
            category = place_info.find('span', class_='category').text.strip()

            return {
                'Place Name': place_name,
                'Address': address,
                'Phone Number': phone_number,
                'Category': category
            }
        else:
            print(f'No information found for {place_name}')
            return None

    finally:
        driver.quit()

if __name__ == '__main__':
    places = ['강남역', '명동', '홍대입구', '서울역']  # 크롤링하고자 하는 장소들

    # 멀티프로세싱을 사용하여 크롤링 작업 병렬 처리
    with Pool(processes=len(places)) as pool:
        results = pool.map(crawl_naver_place, places)

    # 크롤링 결과를 DataFrame으로 변환하여 저장
    df = pd.DataFrame(results)
    df.to_csv('naver_place_info.csv', index=False)

