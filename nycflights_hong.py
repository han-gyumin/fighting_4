import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)  # 긴 문자열도 모두 표시

from nycflights13 import flights, planes

flights.head(3)
planes.head(3)

flights.info()
planes.info()

# 주제 자유:
# merge 사용해서 flights와 planes 병합한 데이터로
# 각 데이터 변수최소 하나씩 선택 후 분석할 것
# 날짜&시간 전처리 코드 들어갈 것
# 시각화 종류 최소 3개
# (배우지 않은 것도 할 수 있으면 넣어도 됨)

# 주제1. 규모가 큰 항공사를 찾아보자! 
# 1. 3개의 공항에서 다 뜨는 항공사
# 2. 운항 횟수 (항공편 수)
# 3. 비행 거리 합계 : 장거리 노선이 많을수록 수익성이 높을 가능성이 있음
# 4. 사용하는 항공기 수 (보유 항공기 규모) 및 유형
# 5. 사용하는 항공기 좌석 수

merge_df = pd.merge(flights, planes, on='tailnum', how='left'); merge_df
merge_df['seats'] = merge_df['seats'].astype('Int64')


## 주제 1. 규모가 큰 항공사를 찾아보자
#1. 몇 개 공항에서 뜨는지 확인
carrier_airport_count = merge_df.groupby('carrier')['origin'] \
    .nunique() \
    .reset_index() \
    .rename(columns={'origin': 'airport_count'})
carrier_airport_count

carrier_airport_count[carrier_airport_count['airport_count'] == 3] # 세 공항 모두 뜨는 항공사만 확인

# 2. 운항 횟수 (항공편 수)
carrier_total_count = merge_df.pivot_table(
    index='carrier',
    values='year_x',
    aggfunc='count'
).reset_index().rename(columns={'year_x': 'flight_count'})
carrier_total_count.sort_values(by='flight_count',ascending=False)

# 3. 비행 거리 합계 : 장거리 노선이 많을수록 수익성이 높을 가능성이 있음

# 항공사별(carrier) 총 비행 거리 계산
total_distance = merge_df.groupby('carrier')['distance'].sum().reset_index()
total_distance
total_distance_sorted = total_distance.sort_values(by="distance", ascending=False)
total_distance_sorted

#4. 항공사별 사용하는 항공기 수 (보유 항공기 규모)
tailnum_no_duplication = merge_df.groupby(['carrier', 'tailnum'], as_index=False).first()
tailnum_no_duplication_value = tailnum_no_duplication.pivot_table(
    index='carrier', 
    values='tailnum',
    aggfunc='count'
).reset_index().sort_values(by='tailnum', ascending=False)
tailnum_no_duplication_value

type_info = tailnum_no_duplication.groupby('carrier').agg(
    aircraft_types=('type', lambda x: list(x.dropna().unique())),  # 사용하는 항공기 유형 (중복제거)
).reset_index()
type_info

# 5. 사용하는 항공기 좌석 수
# 5번 항공사별 좌석수(중복되는 항공기 제외함)
# 항공사별 고유 항공기만 남기기 (tailnum 기준 중복 제거)
unique_planes = merge_df[['carrier', 'tailnum', 'seats']].drop_duplicates()
# 항공사별 좌석 수 합계 구하기
total_seat_unique = unique_planes.groupby('carrier')['seats'].sum().reset_index()
# 정렬해서 보기 좋게
total_seat_unique_sorted = total_seat_unique.sort_values(by='seats', ascending=False)
# 결과 확인
total_seat_unique_sorted

# 6. 항공사별 비행기 타입 별 보유 개수
carrier_type = merge_df.groupby(['carrier', 'type'])['tailnum'].nunique().reset_index()
carrier_type .rename(columns={'tailnum': 'plane_count'}, inplace=True)
carrier_type 


carrier_summary = pd.merge(carrier_airport_count, carrier_total_count, on='carrier')
carrier_summary = pd.merge(carrier_summary, total_distance, on='carrier')
carrier_summary = pd.merge(carrier_summary, tailnum_no_duplication_value, on='carrier')
carrier_summary = pd.merge(carrier_summary, type_info, on='carrier')
carrier_summary = pd.merge(carrier_summary, total_seat_unique, on='carrier')
carrier_summary
























''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# 아직 미정
# 주제2. 규모가 큰 항공사는 지연률이 낮을까, 아니면 높을까?
# 1. 각 항공사별 평균 지연 시간, 지연 편수 비율(정시운항 비율) 비교
# 2. 항공사 규모에 따른 지연률 상관 또는 추세 살펴보기
# 규모가 큰 항공사가 많은 자본으로 인력, 관리가 좋아 지연이 적을지, 아니면 반대로 규모때문에 관리가 더 어려워 지연이 잦을지 유추

# 주제3. 항공사별 운항 패턴 알아보자 (노선 개수, 운항 수가 많은 시간대 등)
# 1. 항공사별 계절 (12~2, 3~5, 6~8, 9~11)별 운항 패턴
# 2. 항공사별 월별 운항 패턴
# 규모가 큰 곳은 여름 휴가시즌(7~8월)이나 연말,연초 시즌(12월,1월)에 더 집중적으로 노선을 늘리는가?
# 규모가 큰 항공사가 운영하는 방식이 아마도 수익적으로 좋은 방식일것 같으니까 한 번 어떻게 하는지 확인해보자.

