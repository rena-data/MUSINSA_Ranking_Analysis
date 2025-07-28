import pandas as pd
import numpy as np
from preprocessing.data_preprocessing import load_and_preprocess_data

class MusinsaMarketingAnalyzer:
    def __init__(self, data_path):
        self.df = load_and_preprocess_data(data_path)
    
    def price_discount_analysis(self):
        """가격/할인 전략 분석"""
        results = {}
        
        # 1. 가격대별 분포
        results['price_range_dist'] = self.df['가격대'].value_counts().sort_index()
        
        # 2. 가격대별 평균 순위
        results['avg_rank_by_price'] = self.df.groupby('가격대')['순위'].mean().sort_values()
        
        # 3. 할인율과 순위의 상관관계
        results['discount_rank_corr'] = self.df[['할인율_정제', '순위']].corr().iloc[0, 1]
        
        # 4. 할인율 구간별 평균 순위
        results['avg_rank_by_discount'] = self.df.groupby('할인율_구간')['순위'].mean().sort_values()
        
        # 5. 최적 가격대 (상위 20위 기준)
        top20 = self.df[self.df['순위'] <= 20]
        results['top20_price_range'] = top20['가격대'].value_counts()
        
        # 6. 카테고리별 평균 할인율
        results['avg_discount_by_category'] = self.df.groupby('카테고리')['할인율_정제'].mean().sort_values(ascending=False)
        
        return results
    
    def brand_category_insights(self):
        """브랜드/카테고리 인사이트 분석"""
        results = {}
        
        # 1. 인기 브랜드 TOP 10
        brand_counts = self.df['브랜드명'].value_counts().head(10)
        results['top10_brands'] = brand_counts
        
        # 2. 브랜드별 평균 순위
        brand_avg_rank = self.df.groupby('브랜드명')['순위'].mean().sort_values().head(10)
        results['brand_avg_rank'] = brand_avg_rank
        
        # 3. 카테고리별 제품 수
        results['category_dist'] = self.df['카테고리'].value_counts()
        
        # 4. 카테고리별 평균 가격
        results['avg_price_by_category'] = self.df.groupby('카테고리')['현재가격_정제'].mean().sort_values(ascending=False)
        
        # 5. 상위 브랜드의 카테고리 전략
        top_brands = brand_counts.index[:5]
        brand_category_strategy = {}
        for brand in top_brands:
            brand_data = self.df[self.df['브랜드명'] == brand]
            brand_category_strategy[brand] = brand_data['카테고리'].value_counts().to_dict()
        results['brand_category_strategy'] = brand_category_strategy
        
        return results
    
    def customer_response_analysis(self):
        """고객 반응 분석"""
        results = {}
        
        # 1. 평점과 순위의 상관관계
        results['rating_rank_corr'] = self.df[['평점', '순위']].corr().iloc[0, 1]
        
        # 2. 리뷰수와 순위의 상관관계
        results['review_rank_corr'] = self.df[['리뷰수_정제', '순위']].corr().iloc[0, 1]
        
        # 3. 리뷰당 순위 점수 TOP 10 (효율적인 제품)
        efficient_products = self.df.nsmallest(10, '리뷰당_순위점수')[['브랜드명', '상품명', '순위', '리뷰수_정제', '리뷰당_순위점수']]
        results['efficient_products'] = efficient_products
        
        # 4. 평점 높지만 순위 낮은 제품 (마케팅 기회)
        high_rating_low_rank = self.df[(self.df['평점'] >= 4.8) & (self.df['순위'] > 50)][['브랜드명', '상품명', '평점', '순위', '리뷰수_정제']]
        results['marketing_opportunities'] = high_rating_low_rank
        
        # 5. 리뷰수 구간별 평균 순위
        review_bins = [0, 100, 500, 1000, 5000, float('inf')]
        review_labels = ['100개 미만', '100-500개', '500-1000개', '1000-5000개', '5000개 이상']
        self.df['리뷰수_구간'] = pd.cut(self.df['리뷰수_정제'], bins=review_bins, labels=review_labels)
        results['avg_rank_by_review_range'] = self.df.groupby('리뷰수_구간')['순위'].mean().sort_values()
        
        return results
    
    def competitive_positioning_analysis(self):
        """경쟁 분석 및 포지셔닝"""
        results = {}
        
        # 1. 카테고리별 가격 경쟁력 분석
        category_price_stats = {}
        for category in self.df['카테고리'].unique():
            cat_data = self.df[self.df['카테고리'] == category]
            if len(cat_data) >= 3:  # 최소 3개 이상 제품이 있는 카테고리만
                category_price_stats[category] = {
                    'min_price': cat_data['현재가격_정제'].min(),
                    'avg_price': cat_data['현재가격_정제'].mean(),
                    'max_price': cat_data['현재가격_정제'].max(),
                    'top3_avg_price': cat_data.nsmallest(3, '순위')['현재가격_정제'].mean()
                }
        results['category_price_stats'] = category_price_stats
        
        # 2. 성공 제품의 특성 (상위 10위)
        top10 = self.df[self.df['순위'] <= 10]
        results['top10_characteristics'] = {
            'avg_price': top10['현재가격_정제'].mean(),
            'avg_discount': top10['할인율_정제'].mean(),
            'avg_rating': top10['평점'].mean(),
            'avg_reviews': top10['리뷰수_정제'].mean(),
            'dominant_category': top10['카테고리'].value_counts().to_dict(),
            'price_range_dist': top10['가격대'].value_counts().to_dict()
        }
        
        # 3. 브랜드 포트폴리오 분석 (제품 수가 많은 브랜드)
        multi_product_brands = self.df['브랜드명'].value_counts()
        multi_product_brands = multi_product_brands[multi_product_brands >= 2].index[:5]
        
        brand_portfolio = {}
        for brand in multi_product_brands:
            brand_data = self.df[self.df['브랜드명'] == brand]
            brand_portfolio[brand] = {
                'product_count': len(brand_data),
                'avg_rank': brand_data['순위'].mean(),
                'price_range': f"{brand_data['현재가격_정제'].min():,} - {brand_data['현재가격_정제'].max():,}",
                'categories': brand_data['카테고리'].value_counts().to_dict()
            }
        results['brand_portfolio_analysis'] = brand_portfolio
        
        return results
    
    def get_all_insights(self):
        """모든 분석 결과 종합"""
        return {
            'price_discount': self.price_discount_analysis(),
            'brand_category': self.brand_category_insights(),
            'customer_response': self.customer_response_analysis(),
            'competitive_positioning': self.competitive_positioning_analysis()
        }

if __name__ == "__main__":
    analyzer = MusinsaMarketingAnalyzer('data/musinsa_ranking_precise.xlsx')
    insights = analyzer.get_all_insights()
    print("분석 완료!")
    print(f"분석 카테고리: {list(insights.keys())}")