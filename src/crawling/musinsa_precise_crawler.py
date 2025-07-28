import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from datetime import datetime
import os
from pathlib import Path
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

class MusinsaPreciseCrawler:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.products = []
        self.product_urls = []
        self.lock = threading.Lock()  # 병렬 처리를 위한 lock
        
    def setup_driver(self):
        """크롬 드라이버 설정"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        
        driver_path = Path.home() / ".chromedriver" / "chromedriver"
        service = Service(str(driver_path))
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        print("✓ 크롬 드라이버 설정 완료")
        
    def create_driver(self):
        """병렬 처리용 드라이버 생성"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        
        driver_path = Path.home() / ".chromedriver" / "chromedriver"
        service = Service(str(driver_path))
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
        
    def collect_product_urls(self):
        """랭킹 페이지에서 상품 URL 수집"""
        print("\n[Step 1] 무신사 랭킹 페이지에서 상품 URL 수집 중...")
        
        ranking_url = 'https://www.musinsa.com/main/musinsa/ranking?storeCode=musinsa&sectionId=199&contentsId=&categoryCode=000&gf=A'
        self.driver.get(ranking_url)
        time.sleep(3)
        
        product_urls = []
        seen_urls = set()
        scroll_count = 0
        
        while len(product_urls) < 100 and scroll_count < 50:
            # 현재 화면의 상품 링크 수집
            elements = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/products/']")
            
            for elem in elements:
                href = elem.get_attribute('href')
                if href and '/products/' in href and href not in seen_urls:
                    seen_urls.add(href)
                    product_urls.append(href)
                    
                    if len(product_urls) >= 100:
                        break
            
            print(f"수집된 URL: {len(product_urls)}개", end='\r')
            
            # 스크롤
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(1.5, 2.5))
            scroll_count += 1
            
            # 더 이상 새로운 컨텐츠가 없으면 종료
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if scroll_count > 2 and len(product_urls) == len(seen_urls):
                break
        
        print(f"\n✓ 총 {len(product_urls)}개의 상품 URL 수집 완료!")
        self.product_urls = product_urls[:100]
        return True
    
    def extract_product_data_parallel(self, url_rank_tuple):
        """병렬 처리용 상품 데이터 추출 메서드"""
        url, rank = url_rank_tuple
        driver = self.create_driver()
        
        try:
            print(f"\n[{rank}위] 크롤링 시작...")
            driver.get(url)
            time.sleep(random.uniform(2.0, 3.0))
            
            data = {
                '순위': rank,
                '상품URL': url,
                '크롤링시간': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # CSS 셀렉터를 사용한 데이터 추출
            selectors = {
                '브랜드명': 'div.sc-12cqkwk-0.inPuAw > a > span > span.text-body_14px_med.font-pretendard',
                '상품명': 'div.sc-1omefes-0.kInhhK',
                '카테고리': 'div.sc-1prswe3-1.gUBQCf.text-body_13px_reg.text-gray-600.font-pretendard',
                '현재가격': 'span.text-title_18px_semi.sc-1hw5bl8-7.kXhdZT.text-black.font-pretendard',
                '원가': 'div.sc-1hw5bl8-0.jwTryS > div > div > span',
                '할인율': 'span.text-title_18px_semi.sc-1hw5bl8-6.hROMjI.text-red.font-pretendard',
                '평점': 'span.text-body_13px_med.pl-0\\.5.pr-1.text-black.font-pretendard',
                '리뷰수': '#root > div.sc-3weaze-0.cBNetp > div.sc-1puoja0-0.hbDyXK > div > div.sc-hw7d9p-0.lecuxg.gtm-click-button > span.text-body_13px_reg.underline.text-gray-600.font-pretendard'
            }
            
            # 각 요소 추출
            for key, selector in selectors.items():
                try:
                    element = driver.find_element(By.CSS_SELECTOR, selector)
                    data[key] = element.text.strip()
                except:
                    # 대체 셀렉터 시도
                    if key == '브랜드명':
                        try:
                            element = driver.find_element(By.CSS_SELECTOR, "a[href*='/brands/']")
                            data[key] = element.text.strip()
                        except:
                            data[key] = ''
                    elif key == '상품명':
                        try:
                            element = driver.find_element(By.TAG_NAME, "h1")
                            data[key] = element.text.strip()
                        except:
                            data[key] = ''
                    elif key == '원가':
                        data[key] = data.get('현재가격', '')
                    else:
                        data[key] = ''
            
            # 리뷰수에서 괄호 제거
            if data['리뷰수'] and '(' in data['리뷰수']:
                data['리뷰수'] = data['리뷰수'].strip('()')
            
            # 디버깅용 출력
            print(f"\n[{rank}위] 크롤링 데이터:")
            print(f"  브랜드명: {data['브랜드명']}")
            print(f"  상품명: {data['상품명'][:50]}..." if len(data['상품명']) > 50 else f"  상품명: {data['상품명']}")
            print(f"  카테고리: {data['카테고리']}")
            print(f"  현재가격: {data['현재가격']}")
            print(f"  원가: {data['원가']}")
            print(f"  할인율: {data['할인율']}")
            print(f"  평점: {data['평점']}")
            print(f"  리뷰수: {data['리뷰수']}")
            
            with self.lock:
                self.products.append(data)
                print(f"[{rank}위] ✓ 수집 완료")
            
            return True
            
        except Exception as e:
            print(f"[{rank}위] ✗ 크롤링 실패: {e}")
            with self.lock:
                self.products.append({
                    '순위': rank,
                    '상품URL': url,
                    '크롤링시간': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    '브랜드명': '',
                    '상품명': '',
                    '카테고리': '',
                    '현재가격': '',
                    '원가': '',
                    '할인율': '0%',
                    '평점': '0',
                    '리뷰수': '0'
                })
            return False
            
        finally:
            driver.quit()
    
    def extract_product_data(self, url, rank):
        """제공된 CSS 셀렉터를 사용하여 상품 데이터 추출 (단일 드라이버)"""
        try:
            print(f"\n[{rank}위] 크롤링 중: {url}")
            self.driver.get(url)
            time.sleep(random.uniform(2.0, 3.0))
            
            data = {
                '순위': rank,
                '상품URL': url,
                '크롤링시간': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # CSS 셀렉터를 사용한 데이터 추출
            selectors = {
                '브랜드명': 'div.sc-12cqkwk-0.inPuAw > a > span > span.text-body_14px_med.font-pretendard',
                '상품명': 'div.sc-1omefes-0.kInhhK',
                '카테고리': 'div.sc-1prswe3-1.gUBQCf.text-body_13px_reg.text-gray-600.font-pretendard',
                '현재가격': 'span.text-title_18px_semi.sc-1hw5bl8-7.kXhdZT.text-black.font-pretendard',
                '원가': 'div.sc-1hw5bl8-0.jwTryS > div > div > span',
                '할인율': 'span.text-title_18px_semi.sc-1hw5bl8-6.hROMjI.text-red.font-pretendard',
                '평점': 'span.text-body_13px_med.pl-0\\.5.pr-1.text-black.font-pretendard',
                '리뷰수': '#root > div.sc-3weaze-0.cBNetp > div.sc-1puoja0-0.hbDyXK > div > div.sc-hw7d9p-0.lecuxg.gtm-click-button > span.text-body_13px_reg.underline.text-gray-600.font-pretendard'
            }
            
            # 각 요소 추출
            for key, selector in selectors.items():
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    data[key] = element.text.strip()
                except:
                    # 대체 셀렉터 시도
                    if key == '브랜드명':
                        try:
                            # 더 간단한 셀렉터로 시도
                            element = self.driver.find_element(By.CSS_SELECTOR, "a[href*='/brands/']")
                            data[key] = element.text.strip()
                        except:
                            data[key] = ''
                    elif key == '상품명':
                        try:
                            element = self.driver.find_element(By.TAG_NAME, "h1")
                            data[key] = element.text.strip()
                        except:
                            data[key] = ''
                    elif key == '원가':
                        # 원가가 없으면 현재가격과 동일하게 설정
                        data[key] = data.get('현재가격', '')
                    else:
                        data[key] = ''
            
            # 리뷰수에서 괄호 제거
            if data['리뷰수'] and '(' in data['리뷰수']:
                data['리뷰수'] = data['리뷰수'].strip('()')
            
            # 디버깅용 출력
            print(f"\n[{rank}위] 크롤링 데이터:")
            print(f"  브랜드명: {data['브랜드명']}")
            print(f"  상품명: {data['상품명'][:50]}..." if len(data['상품명']) > 50 else f"  상품명: {data['상품명']}")
            print(f"  카테고리: {data['카테고리']}")
            print(f"  현재가격: {data['현재가격']}")
            print(f"  원가: {data['원가']}")
            print(f"  할인율: {data['할인율']}")
            print(f"  평점: {data['평점']}")
            print(f"  리뷰수: {data['리뷰수']}")
            print(f"  ✓ 수집 완료")
            
            return data
            
        except Exception as e:
            print(f"  ✗ 크롤링 실패: {e}")
            return {
                '순위': rank,
                '상품URL': url,
                '크롤링시간': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                '브랜드명': '',
                '상품명': '',
                '카테고리': '',
                '현재가격': '',
                '원가': '',
                '할인율': '0%',
                '평점': '0',
                '리뷰수': '0'
            }
    
    def crawl_all_products(self):
        """전체 크롤링 프로세스"""
        print("="*60)
        print("무신사 랭킹 TOP 100 정밀 크롤링")
        print("="*60)
        
        # URL 수집
        if not self.collect_product_urls():
            return False
        
        # 각 상품 크롤링
        print(f"\n[Step 2] {len(self.product_urls)}개 상품 상세 정보 크롤링 시작...")
        
        for rank, url in enumerate(self.product_urls, 1):
            product_data = self.extract_product_data(url, rank)
            self.products.append(product_data)
            
            # 진행률 표시
            if rank % 10 == 0:
                print(f"\n진행률: {rank}/{len(self.product_urls)} ({rank/len(self.product_urls)*100:.0f}%)")
            
            # 봇 탐지 회피를 위한 랜덤 대기
            time.sleep(random.uniform(0.5, 1.5))
        
        print(f"\n✓ 크롤링 완료! 총 {len(self.products)}개 상품")
        return True
    
    def crawl_all_products_parallel(self, max_workers=10):
        """병렬 처리를 사용한 전체 크롤링 프로세스"""
        print("="*60)
        print("무신사 랭킹 TOP 100 정밀 크롤링 (병렬 처리)")
        print("="*60)
        
        # URL 수집
        if not self.collect_product_urls():
            return False
        
        # 병렬 크롤링
        print(f"\n[Step 2] {len(self.product_urls)}개 상품 상세 정보 크롤링 시작...")
        print(f"동시 처리 개수: {max_workers}개")
        
        url_rank_tuples = [(url, rank) for rank, url in enumerate(self.product_urls, 1)]
        
        start_time = time.time()
        completed = 0
        failed = 0
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 작업 제출
            future_to_rank = {executor.submit(self.extract_product_data_parallel, url_rank): url_rank[1] 
                             for url_rank in url_rank_tuples}
            
            # 결과 수집
            for future in as_completed(future_to_rank):
                rank = future_to_rank[future]
                try:
                    success = future.result()
                    if success:
                        completed += 1
                    else:
                        failed += 1
                except Exception as exc:
                    print(f'[{rank}위] 예외 발생: {exc}')
                    failed += 1
                
                # 진행 상황 표시
                total_processed = completed + failed
                if total_processed % 10 == 0:
                    elapsed = time.time() - start_time
                    rate = total_processed / elapsed
                    eta = (len(self.product_urls) - total_processed) / rate
                    print(f"\n진행률: {total_processed}/{len(self.product_urls)} ({total_processed/len(self.product_urls)*100:.0f}%)")
                    print(f"처리 속도: {rate:.1f}개/초, 예상 남은 시간: {eta:.0f}초")
                    print(f"성공: {completed}개, 실패: {failed}개")
        
        # 순위별로 정렬
        self.products.sort(key=lambda x: x['순위'])
        
        elapsed_time = time.time() - start_time
        print(f"\n✓ 크롤링 완료! 총 {len(self.products)}개 상품")
        print(f"성공: {completed}개, 실패: {failed}개")
        print(f"병렬 처리 소요 시간: {elapsed_time:.1f}초 ({elapsed_time/60:.1f}분)")
        
        return True
    
    def save_to_excel(self, filename="musinsa_ranking_precise.xlsx"):
        """데이터를 엑셀 파일로 저장"""
        if not self.products:
            print("저장할 데이터가 없습니다.")
            return None
        
        df = pd.DataFrame(self.products)
        
        # 데이터 전처리
        print("\n데이터 전처리 중...")
        
        # 원가가 빈 값인 경우 현재가격으로 설정
        df.loc[df['원가'] == '', '원가'] = df.loc[df['원가'] == '', '현재가격']
        
        # 저장
        os.makedirs('data', exist_ok=True)
        filepath = os.path.join('data', filename)
        
        # 엑셀로 저장
        df.to_excel(filepath, index=False, engine='openpyxl')
        print(f"\n✓ Excel 파일 저장: {filepath}")
        
        # pickle 파일로도 저장
        df.to_pickle('data/musinsa_ranking_precise.pkl')
        print("✓ Pickle 파일도 저장되었습니다.")
        
        # 기본 통계 출력
        print("\n" + "="*60)
        print("데이터 요약")
        print("="*60)
        print(f"총 상품 수: {len(df)}")
        
        valid_df = df[df['상품명'] != '']
        print(f"유효 데이터: {len(valid_df)}개")
        
        if len(valid_df) > 0:
            print(f"\n브랜드 종류: {valid_df['브랜드명'].nunique()}개")
            print("\nTop 10 브랜드:")
            print(valid_df['브랜드명'].value_counts().head(10))
        
        print("\n상위 10개 상품:")
        display_cols = ['순위', '브랜드명', '상품명', '현재가격', '할인율', '평점', '리뷰수']
        print(df[display_cols].head(10).to_string(index=False))
        
        return df
    
    def close(self):
        """드라이버 종료"""
        if self.driver:
            self.driver.quit()
            print("\n크롬 드라이버 종료")

def main():
    crawler = MusinsaPreciseCrawler()
    
    try:
        start_time = time.time()
        
        # 드라이버 설정
        crawler.setup_driver()
        
        # 병렬 크롤링 실행 (최대 10개 동시 처리)
        success = crawler.crawl_all_products_parallel(max_workers=10)
        
        if success:
            # 데이터 저장
            df = crawler.save_to_excel()
            
        elapsed_time = time.time() - start_time
        print(f"\n총 소요 시간: {elapsed_time/60:.1f}분")
        
    except KeyboardInterrupt:
        print("\n\n사용자에 의해 중단되었습니다.")
        
    except Exception as e:
        print(f"\n오류 발생: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        crawler.close()
        print("\n프로그램 종료")

if __name__ == "__main__":
    main()