import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import platform
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 설정
if platform.system() == 'Darwin':  # macOS
    plt.rcParams['font.family'] = 'AppleGothic'
elif platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
else:  # Linux
    plt.rcParams['font.family'] = 'NanumGothic'

plt.rcParams['axes.unicode_minus'] = False

# 시각화 스타일 설정
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 8)

# 데이터 로드
print("데이터 로딩 중...")
df = pd.read_excel('data/musinsa_ranking_precise.xlsx')
print(f"데이터 shape: {df.shape}")
print("\n컬럼 정보:")
print(df.columns.tolist())
print("\n데이터 미리보기:")
print(df.head())

# 데이터 전처리
print("\n데이터 전처리 중...")
# 가격 데이터 - NaN 처리
df['현재가격_숫자'] = df['현재가격'].fillna('0원').str.replace('원', '').str.replace(',', '').astype(int)
df['원가_숫자'] = df['원가'].fillna('0원').str.replace('원', '').str.replace(',', '').astype(int)

# 할인율 데이터 - NaN 처리
df['할인율_숫자'] = df['할인율'].fillna('0%').str.replace('%', '').astype(int)

# 리뷰수 데이터
df['리뷰수_숫자'] = df['리뷰수'].str.extract('(\d+(?:,\d+)*)').iloc[:, 0].str.replace(',', '').fillna('0').astype(int)

print("전처리 완료!")

# 1. 브랜드 분석
print("\n1. 브랜드 분석")
brand_counts = df['브랜드명'].value_counts().head(15)

plt.figure(figsize=(12, 8))
brand_counts.plot(kind='bar', color='skyblue')
plt.title('상위 100개 상품 중 브랜드별 상품 수 (Top 15)', fontsize=16, fontweight='bold')
plt.xlabel('브랜드명', fontsize=12)
plt.ylabel('상품 수', fontsize=12)
plt.xticks(rotation=45, ha='right')

for i, v in enumerate(brand_counts.values):
    plt.text(i, v + 0.1, str(v), ha='center', va='bottom')

plt.tight_layout()
plt.savefig('output_brand_analysis.png', dpi=300)
plt.close()
print(f"가장 많은 상품을 보유한 브랜드: {brand_counts.index[0]} ({brand_counts.values[0]}개)")

# 2. 가격 분석
print("\n2. 가격 분석")
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.hist(df['현재가격_숫자'], bins=30, color='lightcoral', edgecolor='black', alpha=0.7)
plt.title('현재 가격 분포', fontsize=14, fontweight='bold')
plt.xlabel('가격 (원)', fontsize=12)
plt.ylabel('상품 수', fontsize=12)

plt.subplot(1, 2, 2)
plt.boxplot(df['현재가격_숫자'])
plt.title('현재 가격 박스플롯', fontsize=14, fontweight='bold')
plt.ylabel('가격 (원)', fontsize=12)

plt.tight_layout()
plt.savefig('output_price_distribution.png', dpi=300)
plt.close()

print(f"평균 가격: {df['현재가격_숫자'].mean():,.0f}원")
print(f"중간값: {df['현재가격_숫자'].median():,.0f}원")
print(f"최저가: {df['현재가격_숫자'].min():,.0f}원")
print(f"최고가: {df['현재가격_숫자'].max():,.0f}원")

# 3. 할인율 분석
print("\n3. 할인율 분석")
plt.figure(figsize=(12, 6))

discounted_items = df[df['할인율_숫자'] > 0]

plt.subplot(1, 2, 1)
plt.hist(discounted_items['할인율_숫자'], bins=20, color='lightgreen', edgecolor='black', alpha=0.7)
plt.title('할인율 분포 (할인 상품만)', fontsize=14, fontweight='bold')
plt.xlabel('할인율 (%)', fontsize=12)
plt.ylabel('상품 수', fontsize=12)

plt.subplot(1, 2, 2)
discount_categories = ['할인 없음', '1-10%', '11-30%', '31-50%', '50% 이상']
discount_counts = pd.cut(df['할인율_숫자'], 
                        bins=[-1, 0, 10, 30, 50, 100],
                        labels=discount_categories).value_counts()

discount_counts.plot(kind='bar', color='lightgreen')
plt.title('할인율 구간별 상품 수', fontsize=14, fontweight='bold')
plt.xlabel('할인율 구간', fontsize=12)
plt.ylabel('상품 수', fontsize=12)
plt.xticks(rotation=45)

for i, v in enumerate(discount_counts.values):
    plt.text(i, v + 0.5, str(v), ha='center', va='bottom')

plt.tight_layout()
plt.savefig('output_discount_analysis.png', dpi=300)
plt.close()

print(f"할인 상품 비율: {(df['할인율_숫자'] > 0).sum() / len(df) * 100:.1f}%")
print(f"평균 할인율 (할인 상품만): {discounted_items['할인율_숫자'].mean():.1f}%")

# 4. 평점 및 리뷰 분석
print("\n4. 평점 및 리뷰 분석")
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
rating_items = df[df['평점'] > 0]
plt.hist(rating_items['평점'], bins=20, color='gold', edgecolor='black', alpha=0.7)
plt.title('평점 분포', fontsize=14, fontweight='bold')
plt.xlabel('평점', fontsize=12)
plt.ylabel('상품 수', fontsize=12)

plt.subplot(1, 2, 2)
# 리뷰 수가 0이 아닌 상품만 필터링
valid_reviews = df[df['리뷰수_숫자'] > 0]
plt.scatter(valid_reviews['리뷰수_숫자'], valid_reviews['평점'], alpha=0.6, color='purple')
plt.title('리뷰 수와 평점의 관계', fontsize=14, fontweight='bold')
plt.xlabel('리뷰 수', fontsize=12)
plt.ylabel('평점', fontsize=12)
plt.xscale('log')

plt.tight_layout()
plt.savefig('output_rating_analysis.png', dpi=300)
plt.close()

print(f"평균 평점: {rating_items['평점'].mean():.2f}")
print(f"평균 리뷰 수: {df['리뷰수_숫자'].mean():.0f}개")

# 5. 주요 인사이트
print("\n=== 무신사 랭킹 데이터 분석 주요 인사이트 ===")
print()
print("1. 브랜드 분석")
print(f"   - 가장 많은 상품을 보유한 브랜드: {df['브랜드명'].value_counts().index[0]}")
print(f"   - 상위 100개 중 {len(df['브랜드명'].unique())}개의 브랜드가 진입")
print()
print("2. 가격 분석")
print(f"   - 평균 가격: {df['현재가격_숫자'].mean():,.0f}원")
print(f"   - 가격 범위: {df['현재가격_숫자'].min():,.0f}원 ~ {df['현재가격_숫자'].max():,.0f}원")
print(f"   - 5만원 이하 상품 비율: {(df['현재가격_숫자'] <= 50000).sum() / len(df) * 100:.1f}%")
print()
print("3. 할인 분석")
print(f"   - 할인 상품 비율: {(df['할인율_숫자'] > 0).sum() / len(df) * 100:.1f}%")
print(f"   - 평균 할인율 (할인 상품만): {df[df['할인율_숫자'] > 0]['할인율_숫자'].mean():.1f}%")
print(f"   - 30% 이상 할인 상품: {(df['할인율_숫자'] >= 30).sum()}개")
print()
print("4. 고객 반응")
print(f"   - 평균 평점: {df[df['평점'] > 0]['평점'].mean():.2f}점")
print(f"   - 평균 리뷰수: {df['리뷰수_숫자'].mean():.0f}개")
print(f"   - 리뷰 1000개 이상 상품: {(df['리뷰수_숫자'] >= 1000).sum()}개")
print()
print("5. 상위 순위 특징")
print(f"   - Top 20 평균 가격: {df.iloc[:20]['현재가격_숫자'].mean():,.0f}원")
print(f"   - Top 20 평균 리뷰수: {df.iloc[:20]['리뷰수_숫자'].mean():,.0f}개")

print("\n분석 완료! 시각화 파일이 저장되었습니다.")