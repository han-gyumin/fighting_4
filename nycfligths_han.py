from nycflights13 import flights, planes
import pandas as pd
import matplotlib.pyplot as plt
"""
merge 사용해서 flights와 planes 병합한 데이터로
각 데이터 변수 최소 하나씩 선택 후 분석할 것.
날짜&시간 전처리 코드 들어갈 것
문자열 전처리 코드 들어갈 것
시각화 종류 최소 3개
(배우지 않은 것도 할 수 있으면 넣어도 됨)

주제1. 규모가 큰 항공사를 찾아보자! 
1. 3개의 공항에서 다 뜨는 항공사
2. 운항 횟수 (항공편 수)
3. 비행 거리 합계 : 장거리 노선이 많을수록 수익성이 높을 가능성이 있음
4. 사용하는 항공기 수 (보유 항공기 규모) 및 유형
5. 사용하는 항공기 좌석 수 -> 시각화 하기 뭔가 좋을거같음

# 주제2. 규모가 큰 항공사는 지연률이 낮을까, 아니면 높을까?
# 1. 각 항공사별 평균 지연 시간, 지연 편수 비율(정시운항 비율) 비교
# 2. 항공사 규모에 따른 지연률 상관 또는 추세 살펴보기
# 규모가 큰 항공사가 많은 자본으로 인력, 관리가 좋아 지연이 적을지, 아니면 반대로 규모때문에 관리가 더 어려워 지연이 잦을지 유추
"""


merge_df = pd.merge(flights, planes, on='tailnum', how='left')


#1. 3개의 공항에서 다 뜨는 항공사
airport_count = merge_df.groupby('carrier')['origin'].nunique(); 
airport_count # nunique() : number of unique values
# 세 공항 모두 운항하는 항공사만 필터링
all_list = airport_count[airport_count == 3].index.tolist()

all_list
# 세 공항 모두 운항
airport_all = merge_df[merge_df['carrier'].isin(all_list)]
airport_all

#  8개의 항공사가 세 공항 모두 운항
# '9E', 'AA', 'B6', 'DL', 'EV', 'MQ', 'UA', 'US'

lst=['9E', 'AA', 'B6', 'DL', 'EV', 'MQ', 'UA', 'US']
#2. 2013년 항공사 별 운항 횟수
carrier_total_count = merge_df.pivot_table(
    index='carrier',
    values='year_x',
    aggfunc='count'
).reset_index()

carrier_total_count.sort_values(by='year_x',ascending=False)

# 항공사별 운항 횟수(상위 8개)
"""
	UA	58,665
	B6	54,635
	EV	54,173
	DL	48,110
	AA	32,729
	MQ	26,397
	US	20,536
	9E	18,460
"""

# 3. 비행 거리 합계 : 장거리 노선이 많을수록 수익성이 높을 가능성이 있음


# 항공사별(carrier) 총 비행 거리 계산
total_distance = merge_df.groupby('carrier')['distance'].sum().reset_index()
total_distance
total_distance_sorted = total_distance.sort_values(by="distance", ascending=False)

total_distance_sorted

x = total_distance['carrier']
y = total_distance['distance']


plt.bar(x,y,color = 'skyblue', alpha = 0.7, edgecolor = 'black')
"""
UA	89705524
DL	59507317
B6	58384137
AA	43864584
EV	30498951
MQ	15033955
VX	12902327
WN	12229203
"""
#4. 항공사별 사용하는 항공기 수 (보유 항공기 규모) 및 유형
merge_df_count=merge_df.pivot_table(
    index='carrier', 
    values='tailnum',
    aggfunc='nunique'
).reset_index()
merge_df_count.sort_values(by='tailnum',ascending=False)

"""
DL	629
UA	620
AA	600
WN	582
EV	316
US	289
MQ	237
9E	203
"""


# 항공사별 고유 항공기만 남기기 (tailnum 기준 중복 제거)
unique_planes = merge_df[['carrier', 'tailnum', 'seats']].drop_duplicates()
# 항공사별 좌석 수 합계 구하기
total_seat_unique = unique_planes.groupby('carrier')['seats'].sum().reset_index()
# 정렬해서 보기 좋게
total_seat_unique_sorted = total_seat_unique.sort_values(by='seats', ascending=False)
# 결과 확인
total_seat_unique_sorted

# ※ 기존에 구했던 것에서 중복 제거하는게 타당할 것 같아 위에 수식으로 갑니다! 이견 받음(규민이가..)

# 6. 항공사별 비행기 타입 별 보유 개수
# Fixed wing multi engine 젤 큰 비행기
# Fixed wing single engine 그 다음으로 큰 비행기
# Rotorcraft 젤 작은 비행기
carrier_type = merge_df.groupby(['carrier', 'type'])['tailnum'].nunique().reset_index()
carrier_type .rename(columns={'tailnum': 'plane_count'}, inplace=True)
carrier_type 