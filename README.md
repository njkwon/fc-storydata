# 7개 프로젝트로 완벽하게 끝내는 AWS데이터 파이프라인 구축

:  [7개 프로젝트로 완벽하게 끝내는 AWS데이터 파이프라인 구축](https://bit.ly/3v7oJuB ) 강의 자료

## 목적 : 
클라우드에서 데이터 수집 분석 시각화 환경을 가격 효율적으로 구축하기 위한 기초 교육
Why, What, How 를 기반한 실습

# 알면 좋은 것들
* Spark 
* Scala , Python 언어
* AWS 환경

# 활용하는 AWS 서비스 
* EC2
* IAM
* API Gateway
* Kinesis data stream
* Kinesis data firehose
* Kinesis analytics
* S3
* EMR
* OpenSearch
* Redshift
* Lambda
* RDS
  

## 이해 했다면 더 했으면 하는것들
* Docker
* Kubernetes
* IaC (infrastructure as code) 개발 : 인프라를 코딩으로 하기 
* 분석가가 어떻게 하면 손쉽게 분석할 수 있을까? 에 대한 고민
* Airflow - Scheduler 
 
## Repository 구조
```
.
├── logs                    # 실습을 위한 App log 데이터
├── notebook                # Spark 실습용 notebook 
├── ods                     # Operation Data Store 로 운영(OLTP)에서 사용하는 상품 Master DB Table 
├── script                  # 실습을 위한 shell script 
├── shell                   # EMR 자동화를 위한 shell
├── test                   # Api Gateway 실습을 위한 Test 프로그램 (Java 로 짜여 있고 Jar형태로 제공됨 
└── README.md
 
```

## 강이가 아니더라도 클라우드에서 데이터 관련된 내용 질의 응답은 아래 게시판에서 

[Q/A](https://fastcampus.co.kr/qna/206742) 문의하기
