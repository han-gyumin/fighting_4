# pip install nycflights13
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from nycflights13 import flights, planes

flights.info()
planes.info()

flights.head()
planes.head()

# 주제 : 자유
# merge 사용해서 flights와 planes 병합한 데이터로
# 각 데이터 변수 최소 하나씩 선택 후 분석할 것. 
# 날짜&시간 전처리 코드 들어갈 것
# 문자열 전처리 코드 들어갈것.
# 시각화 종류 최소 3개

merge_df = pd.merge(flights, planes, on ='tailnum', how = 'left')
merge_df
merge_df.head()
merge_df.info()

#  항공사별 운항 패턴 알아보자 (노선 개수, 운항 수가 많은 시간대 등)

# 3. 비행 거리 합계 : 장거리 노선이 많을수록 수익성이 높을 가능성이 있음


# 항공사별(carrier) 총 비행 거리 계산
total_distance = merge_df.groupby('carrier')['distance'].sum().reset_index()
total_distance
total_distance_sorted = total_distance.sort_values(by="distance", ascending=False)

total_distance_sorted

x = total_distance['carrier']
y = total_distance['distance']


plt.bar(x,y,color = 'skyblue', alpha = 0.7, edgecolor = 'black')

# 'UA'가 가장 많은 비행 거리를 가지고 있어!

# 5. 사용하는 항공기 좌석 수

total_seat = merge_df.groupby('carrier')['seats'].sum().reset_index()
total_seat
total_seat_sorted = total_seat.sort_values(by='seats',ascending = False)
total_seat_sorted

x = total_seat['carrier']
y = total_seat['seats']
plt.bar(x,y,color = 'skyblue', alpha = 0.7, edgecolor = 'black')
