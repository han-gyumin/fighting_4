import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from nycflights13 import flights, planes
pd.set_option('display.max_columns', None) 
pd.set_option('display.max_colwidth', None) 


# # merge 사용해서 flights와 planes 병합한 데이터로 
# 각 데이터 변수 최소 하나씩 선택 후 분석할 것
# 날짜 & 시간 전처리 코드 들어갈 것
# 문자열 전처리 코드 들어갈 것
# 시각화 종류 최소 3개 (배우지 않은 것도 할 수 있으면 넣어도 됨)

# 주제1. 규모가 큰 항공사를 찾아보자!
# 1. 3개의 공항에서 다 뜨는 항공사
# 2. 운항 횟수 (항공편 수)
# 3. 비행 거리 합계 : 장거리 노선이 많을수록 수익성이 높을 가능성이 있음
# 4. 사용하는 항공기 수 (보유 항공기 규모) 및 유형
# 5. 사용하는 항공기 좌석 수 -> 시각화 하기 뭔가 좋을거같음

flights.info()
planes.info()

merge_df = pd.merge(flights, planes, on='tailnum', how='left')
pd.set_option('display.max_columns', None)  # 모든 열 표시
pd.set_option('display.max_rows', None)    # 모든 행 표시 (선택)
merge_df.info() # tailnum 결측치 있다 생각해라 

#1. 3개의 공항에서 다 뜨는 항공사
airport_count = merge_df.groupby('carrier')['origin'].nunique(); airport_count # nunique() : number of unique values
airport_count=airport_count.sort_values(ascending=False)
airport_count = pd.DataFrame(airport_count).reset_index()
# 세 공항 모두 운항하는 항공사만 필터링
all_list = airport_count[airport_count == 3].index.tolist()
# 세 공항 모두 운항
airport_all = merge_df[merge_df['carrier'].isin(all_list)]; airport_all


#2. 2013년 항공사 별 운영 횟수
carrier_total_count = merge_df.pivot_table(
    index='carrier',
    values='year_x',
    aggfunc='count'
).reset_index()
carrier_total_count.sort_values(by='year_x',ascending=False)

big_carrier = pd.merge(airport_count, carrier_total_count, on='carrier', how='outer')  #1, 2번 합침

# 3. 비행 거리 합계 : 장거리 노선이 많을수록 수익성이 높을 가능성이 있음
# 항공사별(carrier) 총 비행 거리 계산
total_distance = merge_df.groupby('carrier')['distance'].sum().reset_index()
total_distance
total_distance_sorted = total_distance.sort_values(by="distance", ascending=False)

total_distance_sorted
big_carrier2 = pd.merge(big_carrier,total_distance_sorted, on='carrier', how='outer') #2, 3번 합침

x = total_distance['carrier']
y = total_distance['distance']


plt.bar(x,y,color = 'skyblue', alpha = 0.7, edgecolor = 'black')

#4. 항공사별 사용하는 항공기 수 (보유 항공기 규모) 및 유형
table_sort = merge_df.pivot_table(
    index='carrier', 
    values='tailnum',
    aggfunc='nunique'
).reset_index()
big_carrier3 = pd.merge(big_carrier2,table_sort, on='carrier', how='outer')  #3, 4번 합침


# 5 사용하는 항공기 좌석 수 (고유)
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