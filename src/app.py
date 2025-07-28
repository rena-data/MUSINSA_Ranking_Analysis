import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from analysis.marketing_analysis import MusinsaMarketingAnalyzer

# 페이지 설정
st.set_page_config(
    page_title="무신사 마케팅 분석 대시보드",
    page_icon="👔",
    layout="wide"
)

# CSS 스타일
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    h1 {
        color: #1f77b4;
    }
    h2 {
        color: #2ca02c;
        margin-top: 2rem;
    }
    h3 {
        color: #ff7f0e;
    }
</style>
""", unsafe_allow_html=True)

# 타이틀
st.title("🛍️ 무신사 랭킹 데이터 마케팅 분석 대시보드")
st.markdown("---")

# 데이터 로드
@st.cache_data
def load_data():
    analyzer = MusinsaMarketingAnalyzer('data/musinsa_ranking_precise.xlsx')
    return analyzer, analyzer.get_all_insights()

analyzer, insights = load_data()
df = analyzer.df

# 사이드바
st.sidebar.header("📊 분석 메뉴")
analysis_type = st.sidebar.selectbox(
    "분석 유형 선택",
    ["전체 요약", "가격/할인 전략", "브랜드/카테고리", "고객 반응", "경쟁 분석"]
)

# 전체 요약
if analysis_type == "전체 요약":
    st.header("📈 전체 요약 대시보드")
    
    # 주요 지표
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("총 제품 수", f"{len(df)}개")
        st.metric("평균 가격", f"{df['현재가격_정제'].mean():,.0f}원")
    
    with col2:
        st.metric("평균 할인율", f"{df['할인율_정제'].mean():.1f}%")
        st.metric("평균 평점", f"{df['평점'].mean():.2f}")
    
    with col3:
        st.metric("브랜드 수", f"{df['브랜드명'].nunique()}개")
        st.metric("카테고리 수", f"{df['카테고리'].nunique()}개")
    
    with col4:
        st.metric("평균 리뷰 수", f"{df['리뷰수_정제'].mean():,.0f}개")
        st.metric("최다 리뷰", f"{df['리뷰수_정제'].max():,}개")
    
    st.markdown("---")
    
    # 차트들
    col1, col2 = st.columns(2)
    
    with col1:
        # 가격대별 분포
        fig1 = px.bar(
            x=insights['price_discount']['price_range_dist'].index,
            y=insights['price_discount']['price_range_dist'].values,
            title="가격대별 제품 분포",
            labels={'x': '가격대', 'y': '제품 수'}
        )
        fig1.update_traces(marker_color='lightblue')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # 카테고리별 분포
        fig2 = px.pie(
            values=insights['brand_category']['category_dist'].values,
            names=insights['brand_category']['category_dist'].index,
            title="카테고리별 제품 분포"
        )
        st.plotly_chart(fig2, use_container_width=True)

# 가격/할인 전략 분석
elif analysis_type == "가격/할인 전략":
    st.header("💰 가격/할인 전략 분석")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("가격대별 평균 순위")
        price_rank_data = insights['price_discount']['avg_rank_by_price']
        fig = px.bar(
            x=price_rank_data.index,
            y=price_rank_data.values,
            title="가격대별 평균 순위 (낮을수록 좋음)",
            labels={'x': '가격대', 'y': '평균 순위'}
        )
        fig.update_traces(marker_color='coral')
        st.plotly_chart(fig, use_container_width=True)
        
        st.info(f"💡 할인율과 순위의 상관관계: {insights['price_discount']['discount_rank_corr']:.3f}")
    
    with col2:
        st.subheader("할인율별 평균 순위")
        discount_rank_data = insights['price_discount']['avg_rank_by_discount']
        fig = px.bar(
            x=discount_rank_data.index,
            y=discount_rank_data.values,
            title="할인율 구간별 평균 순위",
            labels={'x': '할인율 구간', 'y': '평균 순위'}
        )
        fig.update_traces(marker_color='lightgreen')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # 상위 20위 가격대 분석
    st.subheader("🏆 상위 20위 제품의 가격대 분포")
    top20_price = insights['price_discount']['top20_price_range']
    fig = px.pie(
        values=top20_price.values,
        names=top20_price.index,
        title="TOP 20 제품의 가격대 분포"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # 카테고리별 평균 할인율
    st.subheader("📊 카테고리별 평균 할인율")
    cat_discount = insights['price_discount']['avg_discount_by_category'].head(10)
    fig = px.bar(
        y=cat_discount.index,
        x=cat_discount.values,
        orientation='h',
        title="카테고리별 평균 할인율 TOP 10",
        labels={'x': '평균 할인율 (%)', 'y': '카테고리'}
    )
    st.plotly_chart(fig, use_container_width=True)

# 브랜드/카테고리 분석
elif analysis_type == "브랜드/카테고리":
    st.header("🏢 브랜드/카테고리 인사이트")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("인기 브랜드 TOP 10")
        top_brands = insights['brand_category']['top10_brands']
        fig = px.bar(
            y=top_brands.index,
            x=top_brands.values,
            orientation='h',
            title="브랜드별 제품 수 TOP 10",
            labels={'x': '제품 수', 'y': '브랜드'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("브랜드별 평균 순위 TOP 10")
        brand_rank = insights['brand_category']['brand_avg_rank']
        fig = px.bar(
            y=brand_rank.index,
            x=brand_rank.values,
            orientation='h',
            title="브랜드별 평균 순위 (낮을수록 좋음)",
            labels={'x': '평균 순위', 'y': '브랜드'}
        )
        fig.update_traces(marker_color='purple')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # 상위 브랜드의 카테고리 전략
    st.subheader("🎯 상위 브랜드의 카테고리 전략")
    brand_strategy = insights['brand_category']['brand_category_strategy']
    
    for brand, categories in list(brand_strategy.items())[:3]:
        st.write(f"**{brand}**")
        cat_df = pd.DataFrame(list(categories.items()), columns=['카테고리', '제품 수'])
        fig = px.pie(
            cat_df,
            values='제품 수',
            names='카테고리',
            title=f"{brand}의 카테고리별 제품 분포"
        )
        st.plotly_chart(fig, use_container_width=True)

# 고객 반응 분석
elif analysis_type == "고객 반응":
    st.header("👥 고객 반응 분석")
    
    # 상관관계 정보
    col1, col2 = st.columns(2)
    with col1:
        st.metric("평점-순위 상관관계", f"{insights['customer_response']['rating_rank_corr']:.3f}")
    with col2:
        st.metric("리뷰수-순위 상관관계", f"{insights['customer_response']['review_rank_corr']:.3f}")
    
    st.markdown("---")
    
    # 효율적인 제품 (리뷰 대비 높은 순위)
    st.subheader("💎 리뷰 대비 효율적인 제품 TOP 10")
    efficient_products = insights['customer_response']['efficient_products']
    st.dataframe(efficient_products, use_container_width=True)
    
    # 마케팅 기회 제품
    st.subheader("🎯 마케팅 기회 제품 (평점 높지만 순위 낮음)")
    marketing_opps = insights['customer_response']['marketing_opportunities']
    if len(marketing_opps) > 0:
        st.dataframe(marketing_opps, use_container_width=True)
    else:
        st.info("평점이 높지만 순위가 낮은 제품이 없습니다.")
    
    # 리뷰수 구간별 평균 순위
    st.subheader("📊 리뷰수 구간별 평균 순위")
    review_rank = insights['customer_response']['avg_rank_by_review_range']
    fig = px.bar(
        x=review_rank.index,
        y=review_rank.values,
        title="리뷰수 구간별 평균 순위",
        labels={'x': '리뷰수 구간', 'y': '평균 순위'}
    )
    st.plotly_chart(fig, use_container_width=True)

# 경쟁 분석
else:  # 경쟁 분석
    st.header("⚔️ 경쟁 분석 및 포지셔닝")
    
    # TOP 10 제품 특성
    st.subheader("🏆 상위 10위 제품의 성공 요인")
    top10_chars = insights['competitive_positioning']['top10_characteristics']
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("평균 가격", f"{top10_chars['avg_price']:,.0f}원")
    with col2:
        st.metric("평균 할인율", f"{top10_chars['avg_discount']:.1f}%")
    with col3:
        st.metric("평균 평점", f"{top10_chars['avg_rating']:.2f}")
    with col4:
        st.metric("평균 리뷰수", f"{top10_chars['avg_reviews']:,.0f}개")
    
    # 브랜드 포트폴리오 분석
    st.subheader("📂 주요 브랜드 포트폴리오 분석")
    portfolio = insights['competitive_positioning']['brand_portfolio_analysis']
    
    for brand, data in portfolio.items():
        with st.expander(f"{brand} - 제품 {data['product_count']}개, 평균 순위 {data['avg_rank']:.1f}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**가격대**: {data['price_range']}원")
            with col2:
                st.write("**카테고리 분포**")
                for cat, count in data['categories'].items():
                    st.write(f"- {cat}: {count}개")
    
    # 카테고리별 가격 경쟁력
    st.subheader("💰 카테고리별 가격 경쟁력 분석")
    
    # 가격 통계를 데이터프레임으로 변환
    price_stats = insights['competitive_positioning']['category_price_stats']
    if price_stats:
        price_df = pd.DataFrame(price_stats).T
        price_df = price_df.round(0)
        
        # 가격 범위 시각화
        fig = go.Figure()
        
        categories = list(price_stats.keys())
        min_prices = [stats['min_price'] for stats in price_stats.values()]
        avg_prices = [stats['avg_price'] for stats in price_stats.values()]
        max_prices = [stats['max_price'] for stats in price_stats.values()]
        top3_prices = [stats['top3_avg_price'] for stats in price_stats.values()]
        
        fig.add_trace(go.Scatter(
            x=categories, y=min_prices,
            mode='markers', name='최저가',
            marker=dict(size=10, color='green')
        ))
        fig.add_trace(go.Scatter(
            x=categories, y=avg_prices,
            mode='markers', name='평균가',
            marker=dict(size=12, color='blue')
        ))
        fig.add_trace(go.Scatter(
            x=categories, y=max_prices,
            mode='markers', name='최고가',
            marker=dict(size=10, color='red')
        ))
        fig.add_trace(go.Scatter(
            x=categories, y=top3_prices,
            mode='markers', name='TOP3 평균가',
            marker=dict(size=14, color='gold', symbol='star')
        ))
        
        fig.update_layout(
            title="카테고리별 가격 분포",
            xaxis_title="카테고리",
            yaxis_title="가격 (원)",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)

# 푸터
st.markdown("---")
st.markdown("📊 **무신사 랭킹 데이터 기반 마케팅 인사이트** | 데이터 기준: 상위 100개 제품")