## 하둡 생태계 데이터 수집/저장/처리/적재
데이터 수집 - Kafka - 실시간 분산환경에서 메시지를 송수신하는 메시지 전달 솔루션<br>
분산 데이터 저장 - HDFS - 데이터를 클러스터 환경에 분산 저장하는 솔루션으로 Namenode(리더노드)와 Datanode(컴퓨팅노드)로 관리<br>
분산 클러스터 관리 - YARN - 분산 클러스터의 리소스 관리 솔루션으로 Resourse Manager가 Node Manager를 관리<br>
분산 데이터 배치처리 - Hadoop MapReduce - Map과 Reduce의 2상로 데이터를 처리하는 하둡 기반의 배치 작업 플랫폼<br>
인메모리 데이터 처리 - Apache Spark - 인메모리 상에서의 데이터 처리 플랫폼으로 배치처리, 실시간 스트리밍, SQL 질의와 Graph 처리, 머신러닝 같은 하위 프로젝트를 사용<br>
데이터웨어하우스 연동 - Hive - 하둡 기반의 데이터 웨어하우스 시스템<br>

## 분산 클러스터에서 데이터 검색 방법: ElasticSearch
Restful 프로토콜을 사용하여 정형, 비정형, 데이터 위치정보, 메트릭 등 원하는 방법으로 다양한 유형의 데이터 검색 수행

## 하둡 생태계를 사용하는 이유
1. 하둡의 HDFS는 동일한 저가 리눅스를 분산 클러스터로 사용하여 scale out을 사용 -> 저장소의 비용이 저렴함
2. 정형 데이터 외에도 반정형, 비정형 데이터 모두 다룸
3. YARN으로 메모리, CPU, 디스크 리소스를 효율적으로 저렴하게 관리 가능 -> 운영할때 리소스 관리 포인트에서 좀 자유로움
4. 딥러닝, 인공지능에서 필요한 INPUT 데이터 제공 가능 -> 데이터 모델링을 통한 데이터의 인사이트 추출 가능
5. Schema on Read -> 데이터를 read 하는 시점에 스키마를 지정하여 데이터 추출 -> 데이터가 저장되는 스키마의 위치가 모두 달라서 시간 절약 가능

## 데이터 전처리
정의: 원시 데이터를 비즈니스 요구사항의 분석 및 처리에 적합한 형식으로 데이터를 가공하고 처리하는 작업<br>
기법: 데이터 정제, 데이터 통합, 데이터 변환, 데이터 정리

## ETL 프로세스(Extract/Transformation/Loading)
데이터 수집하고 비즈니스 규칙에 따라 데이터를 변환한 후 대상 데이터를 저장소로 적재하는데 사용되는 데이터 파이프라인

## ELT 프로세스(Extract&Load/Transformation)
일단 데이터를 수집항 적재하고 이후 비즈니스 요구사항에 맞춰 데이터 변환 -> 비즈니스 요구사항이 정해지지 않았어도 데이터 적재 가능

## 하둡파일시스템
- 구성: 마스터 역할의 NameNode와 데이터를 실제로 저장하는 다수의 슬레이브 Datanode
- 구조: 마스터-슬레이브 구조(하나의 마스터에 여러개의 슬레이브 구조)
- 동작원리
  1. 사용자가 데이터를 HDFS에 저장
  2. HDFS Client는 메타데이터(파일명, 폴더구조 등)를 NameNode에 저장
  3. NameNode는 Datanode에게 데이터 관련 명령 지시,  Datanode는 자신의 상태 정보를 NameNode에게 송신
  4. Datanode안의 여러개의 블록으로 나눠져 실데이터가 복제 저장됨
  5. 사용자가 데이터를 읽어올 경우, HDFS Client는 NameNode로부터 파일 블록에 대한 메타 데이터 정보를 수신
  6. HDFS Client가 원하는 데이터가 있는 Datanode의 파일 블록을 찾아서 파일을 읽어옴.
  7. NameNode의 메타 데이터 변경 시, Secondary Namenode의 Edits 파일에 로그 저장
 
## Yarn의 구조
|데몬|기능|
|------|---|
|Resource Manager|Yarn의 마스터 역할 수행(총괄 관리자)|
|Scheduler|Resource Manager 내의 데몬으로 Node Manager와 통신하며, Application Master에 자원 할당|
|Application Manager|Resource Manager 내의 데몬으로 Application Master 실행 및 상태 관리|
|Node Manager|각 노드의 상태 정보를 모니터링 하여 Resource Manager에게 제공|
|Application Master|각각의 Application을 관리하는 마스터의 역할|
|Container|Application Master가 관리하는 태스크를 수행, Node Manager에 의해 생성|

## 하둡파일시스템의 장점
- 스케일 아웃 분산 시스템(병렬로 스케일 아웃됨으로 데이터 양에 따라서 서버 필요)
- 장애복구(마스터 서버가 슬레이브 서버의 장애를 실시간으로 감지하여 서비스 우회 OR 다른 노드에 복제된 데이터 사용)
- 대용량데이터(한번 저장된 데이터는 only read = 데이터 업데이트 X)

## 하둡파일시스템 페이지 접속(구동확인)
- 네임노드 정보
![image](https://github.com/seeheee/data_pipeline/assets/53335160/6e62f13c-7703-449d-ba88-ae82c55e8d47)

- 데이터노드 정보
![image](https://github.com/seeheee/data_pipeline/assets/53335160/b8931cee-34af-453c-93e7-cdd4f34a2206)

- yarn 정보
![image](https://github.com/seeheee/data_pipeline/assets/53335160/ca0a651c-1a25-40d7-8ca1-60ad761cc262)

## 카프카
KSQL: 스트리밍이 되는 데이터를 카프카가 제공하는 유사 SQL을 사용하여 로직을 구현하여 분석하는 프로젝트

