# body_speed, stride_index 완성

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# CSV 파일 경로 설정
file_path = 'dr_rec003.csv'
# CSV 파일을 'cp949' 또는 'euc-kr' 인코딩으로 읽기
df = pd.read_csv(file_path, encoding='cp949')  # 또는 encoding='euc-kr'

# Streamlit 애플리케이션 시작
st.title('Video analysis results')

# Sidebar에 날짜 선택 옵션 추가
selected_date = st.sidebar.selectbox('Please choose a training date👏', df['date'])

# 선택한 날짜에 해당하는 데이터 추출
selected_data = df[df['date'] == selected_date]

# 선택한 날짜에 대한 데이터 표시
st.write(f"### Analysis results: {selected_date}")
st.table(selected_data[['place', 'company', 'runner_name']])

# 비디오 파일 경로 가져오기
video_file = selected_data['video_file'].values[0]

# 이미지 로딩 및 데이터 값 표시를 같은 행에 배치
col1, col2 = st.columns(2)  # 2개의 컬럼 생성

# 첫 번째 컬럼에 이미지 표시
with col1:
    video_bytes = open(video_file, 'rb').read()
    st.video(video_bytes)

# 두 번째 컬럼에 데이터 값 표시
with col2:
    st.write('Average Speed:', selected_data['avg_speed'].values[0])
    st.write('Current Speed:', selected_data['current_speed'].values[0])
    st.write('Stride:', selected_data['stride'].values[0])
    st.write('Steps:', selected_data['steps'].values[0])

# CSV 파일 로드
csv_file = selected_data['body_speed_csv_file'].values[0]
df_body_speed = pd.read_csv(csv_file)

# 그래프 표시 (동일한 행에 나열)
st.write('## Body Speed Data Trends')

# 데이터프레임 그룹화
grouped = df_body_speed.groupby('video_id')

# 각 그룹에 대한 그래프 그리기
for video_id, group_data in grouped:
    fig, ax = plt.subplots(figsize=(8, 4))  # 1행 1열의 서브플롯 생성

    # body_speed 데이터 그래프
    ax.plot(group_data['index'], group_data['body_speed'], label='body_speed')  # body_speed 그래프 추가
    ax.set_title(f'Body Speed for Video ID {video_id}')  # 그래프 제목 수정

    # 그래프 스타일 및 레이블 설정
    ax.set_xlabel('Index')
    ax.set_ylabel('Body Speed')
    ax.legend()  # 범례 표시

    # 서브플롯 레이아웃 조정
    plt.tight_layout()

    # 그래프를 Streamlit 애플리케이션에 표시
    st.pyplot(fig)

# CSV 파일 로드
csv_file = selected_data['stride_cadence_csv_file'].values[0]
df_stride_cadence = pd.read_csv(csv_file)

# 그래프 표시 (동일한 행에 나열)
st.write('## Stride and Cadence Data Trends')

# 데이터프레임 그룹화
grouped = df_stride_cadence.groupby('video_id')

# 각 그룹에 대한 그래프 그리기
for video_id, group_data in grouped:
    fig, ax = plt.subplots(figsize=(8, 4))  # 1행 1열의 서브플롯 생성

    # stride 데이터 그래프
    ax.plot(group_data['stride_index'], group_data['stride'], label='stride')  # stride 그래프 추가

    # cadence 데이터 그래프
    ax.plot(group_data['stride_index'], group_data['cadence'], label='cadence')  # cadence 그래프 추가

    ax.set_title(f'Stride and Cadence for Video ID {video_id}')  # 그래프 제목 수정

    # 그래프 스타일 및 레이블 설정
    ax.set_xlabel('Index')
    ax.set_ylabel('Stride and Cadence')
    ax.legend()  # 범례 표시

    # 서브플롯 레이아웃 조정
    plt.tight_layout()

    # 그래프를 Streamlit 애플리케이션에 표시
    st.pyplot(fig)

    # 그래프를 사용한 후에는 닫아주기
    plt.close(fig)
