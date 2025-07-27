# 무신사 랭킹 분석 프로젝트

무신사 전체 카테고리 상위 100개 상품의 데이터를 정밀 크롤링하고 분석하는 프로젝트입니다.

## 프로젝트 구조

```
MUSINSA_Ranking_Analysis/
├── data/                           # 크롤링된 데이터 저장 디렉토리
│   ├── musinsa_ranking_precise.xlsx
│   └── musinsa_ranking_precise.pkl
├── notebooks/                      # Jupyter Notebook 분석 파일
│   └── musinsa_analysis.ipynb      # 데이터 분석 및 시각화 노트북
├── musinsa_precise_crawler.py      # 정밀 크롤링 스크립트 (병렬 처리)
├── setup_chromedriver.py           # ChromeDriver 자동 설치 스크립트
├── data_preprocessing.py           # 데이터 전처리 모듈
├── marketing_analysis.py           # 마케팅 분석 클래스 및 메서드
├── app.py                          # Streamlit 대시보드 애플리케이션
├── run_dashboard.sh                # 대시보드 실행 스크립트
├── run_notebook.py                 # 분석 결과 실행 파일 (CLI용)
├── requirements.txt                # 필요한 패키지 목록
└── README.md                       # 프로젝트 설명서
```

## 파일별 역할

### 1. 데이터 수집
- **`musinsa_precise_crawler.py`**: 무신사 전체 카테고리 상위 100개 상품 정보를 병렬 처리로 크롤링
- **`setup_chromedriver.py`**: Chrome 버전에 맞는 ChromeDriver 자동 설치 (M1/M2 Mac 지원)

### 2. 데이터 처리 및 분석
- **`data_preprocessing.py`**: 크롤링된 데이터의 전처리 (가격/할인율/리뷰수 정제, 구간 분류)
- **`marketing_analysis.py`**: 마케팅 인사이트 도출을 위한 분석 클래스
  - 가격/할인 전략 분석
  - 브랜드/카테고리 인사이트
  - 고객 반응 분석
  - 경쟁 포지셔닝 분석

### 3. 시각화 및 대시보드
- **`app.py`**: Streamlit 기반 인터랙티브 마케팅 분석 대시보드
- **`notebooks/musinsa_analysis.ipynb`**: Jupyter Notebook 형태의 상세 분석
- **`run_notebook.py`**: CLI에서 분석 결과를 실행하고 시각화 파일 생성

### 4. 유틸리티
- **`run_dashboard.sh`**: 대시보드를 간편하게 실행하는 쉘 스크립트

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

#### 방법 1: Jupyter Notebook 사용
```bash
jupyter notebook notebooks/musinsa_analysis.ipynb
```

#### 방법 2: Streamlit 대시보드 사용
```bash
./run_dashboard.sh
# 또는
python -m streamlit run app.py
```

#### 방법 3: CLI에서 직접 실행
```bash
python run_notebook.py
```

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
- 대시보드 실행 시 기본 포트는 8501입니다.

## 라이선스

이 프로젝트는 교육 및 연구 목적으로 제작되었습니다.
