# 무신사 랭킹 분석 프로젝트

무신사 전체 카테고리 상위 100개 상품의 데이터를 정밀 크롤링하고 분석하는 프로젝트입니다.

## 프로젝트 구조

```
MUSINSA_Ranking_Analysis/
├── data/                           # 크롤링된 데이터 저장 디렉토리
├── notebooks/                      # Jupyter Notebook 분석 파일
│   └── musinsa_analysis.ipynb
├── musinsa_precise_crawler.py      # 정밀 크롤링 스크립트 (병렬 처리)
├── setup_chromedriver.py           # ChromeDriver 자동 설치 스크립트
├── requirements.txt                # 필요한 패키지 목록
└── README.md                       # 프로젝트 설명서
```

## 설치 방법

1. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

2. ChromeDriver 자동 설치:
```bash
python setup_chromedriver.py
```

## 사용 방법

### 1. 데이터 크롤링

```bash
python musinsa_precise_crawler.py
```

크롤링된 데이터는 다음 파일들로 저장됩니다:
- `data/musinsa_ranking_precise.xlsx` (Excel 파일)
- `data/musinsa_ranking_precise.pkl` (Pickle 파일)

### 2. 데이터 분석

```bash
jupyter notebook notebooks/musinsa_analysis.ipynb
```

Jupyter Notebook을 실행하여 데이터 분석 결과를 확인할 수 있습니다.

## 수집 데이터

- 순위
- 브랜드명
- 상품명
- 카테고리
- 현재 가격
- 원가
- 할인율
- 평점
- 리뷰 수
- 상품 URL
- 크롤링 시간

## 분석 내용

1. **브랜드 분석**: 상위 브랜드 분포
2. **가격 분석**: 가격대별 분포 및 통계
3. **할인율 분석**: 할인 상품 비율 및 할인율 분포
4. **평점 및 리뷰 분석**: 고객 반응 분석
5. **상위 순위 특성**: Top 20 vs 나머지 비교
6. **브랜드별 상세 분석**: 브랜드별 평균 가격, 할인율, 평점 등

## 주요 기능

- **병렬 처리**: 최대 10개의 스레드로 동시 크롤링하여 속도 향상
- **정밀 셀렉터**: CSS 셀렉터를 사용한 정확한 데이터 추출
- **자동 재시도**: 크롤링 실패 시 대체 셀렉터 적용
- **진행 상황 표시**: 실시간 진행률 및 예상 소요 시간 표시
- **데이터 검증**: 크롤링 시 모든 항목 출력으로 데이터 확인

## 주의사항

- 크롤링 시 과도한 요청을 방지하기 위해 적절한 딜레이를 적용했습니다.
- 웹사이트 구조가 변경되면 크롤링 코드 수정이 필요할 수 있습니다.
- ChromeDriver는 Chrome 브라우저 버전과 호환되어야 합니다.