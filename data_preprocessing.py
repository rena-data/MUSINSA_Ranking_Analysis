import pandas as pd
import numpy as np
import re

def load_and_preprocess_data(file_path):
    """무신사 랭킹 데이터를 로드하고 전처리"""
    df = pd.read_excel(file_path)
    
    # 가격 데이터 정제 (문자열 -> 숫자)
    def clean_price(price_str):
        if pd.isna(price_str):
            return np.nan
        # 숫자와 쉼표만 추출
        clean_str = re.sub(r'[^\d,]', '', str(price_str))
        clean_str = clean_str.replace(',', '')
        try:
            return int(clean_str)
        except:
            return np.nan
    
    # 리뷰수 정제
    def clean_review_count(review_str):
        if pd.isna(review_str):
            return 0
        # 숫자와 쉼표만 추출
        clean_str = re.sub(r'[^\d,]', '', str(review_str))
        clean_str = clean_str.replace(',', '')
        try:
            return int(clean_str)
        except:
            return 0
    
    # 할인율 정제
    def clean_discount_rate(discount_str):
        if pd.isna(discount_str):
            return 0
        # 숫자만 추출
        clean_str = re.sub(r'[^\d]', '', str(discount_str))
        try:
            return int(clean_str)
        except:
            return 0
    
    # 전처리 적용
    df['현재가격_정제'] = df['현재가격'].apply(clean_price)
    df['원가_정제'] = df['원가'].apply(clean_price)
    df['할인율_정제'] = df['할인율'].apply(clean_discount_rate)
    df['리뷰수_정제'] = df['리뷰수'].apply(clean_review_count)
    
    # 할인액 계산
    df['할인액'] = df['원가_정제'] - df['현재가격_정제']
    
    # 리뷰당 순위 점수 (낮을수록 좋음)
    df['리뷰당_순위점수'] = df['순위'] / (df['리뷰수_정제'] + 1)
    
    # 가격대 구분
    df['가격대'] = pd.cut(df['현재가격_정제'], 
                         bins=[0, 30000, 50000, 100000, 200000, float('inf')],
                         labels=['3만원 이하', '3-5만원', '5-10만원', '10-20만원', '20만원 이상'])
    
    # 할인율 구간
    df['할인율_구간'] = pd.cut(df['할인율_정제'],
                            bins=[-1, 0, 10, 30, 50, 100],
                            labels=['할인없음', '10% 이하', '10-30%', '30-50%', '50% 이상'])
    
    return df

if __name__ == "__main__":
    # 테스트
    df = load_and_preprocess_data('data/musinsa_ranking_precise.xlsx')
    print("전처리 완료!")
    print(f"데이터 shape: {df.shape}")
    print("\n새로운 컬럼:")
    print([col for col in df.columns if '정제' in col or col in ['할인액', '리뷰당_순위점수', '가격대', '할인율_구간']])