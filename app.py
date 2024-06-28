import streamlit as st
import pandas as pd

# 데이터 저장소
classes_data = []
registrations = []

# 비밀번호
password = "1234"

# 수강정보 입력 페이지
def input_class_info():
    st.title("수강정보 입력")
    
    if st.text_input("비밀번호", type="password") != password:
        st.error("잘못된 비밀번호입니다.")
        return
    
    st.write("강의 정보를 입력하세요.")
    
    class_date = st.date_input("날짜")
    class_time = st.time_input("시간")
    instructor = st.text_input("강사")
    topic = st.text_input("주제")
    materials = st.text_input("준비물")
    max_participants = st.number_input("참여 가능 인원", min_value=1, step=1)
    
    if st.button("저장"):
        class_info = {
            "날짜": class_date,
            "시간": class_time,
            "강사": instructor,
            "주제": topic,
            "준비물": materials,
            "참여 가능 인원": max_participants,
            "신청자": 0
        }
        classes_data.append(class_info)
        st.success("강의 정보가 저장되었습니다.")
        
    if classes_data:
        st.write("저장된 강의 정보:")
        st.dataframe(pd.DataFrame(classes_data))

# 수강신청 페이지
def register_for_class():
    st.title("수강신청")
    
    selected_class = st.selectbox("강의를 선택하세요", classes_data, format_func=lambda x: f"{x['날짜']} - {x['주제']}")

    if selected_class["신청자"] >= selected_class["참여 가능 인원"]:
        st.error("해당 강의는 신청 인원이 초과되었습니다.")
        return
    
    st.write(f"강의 정보: {selected_class}")
    
    nickname = st.text_input("닉네임")
    name = st.text_input("이름")
    phone = st.text_input("연락처")
    email = st.text_input("이메일 주소")
    agree = st.checkbox("개인정보제공동의")
    
    if st.button("수강신청") and agree:
        registration = {
            "닉네임": nickname,
            "이름": name,
            "연락처": phone,
            "이메일": email,
            "강의": selected_class
        }
        registrations.append(registration)
        selected_class["신청자"] += 1
        st.success("수강신청이 완료되었습니다.")
        
# 수강신청 결과 페이지
def view_registration_results():
    st.title("수강신청 결과")
    
    grouped_registrations = {}
    for reg in registrations:
        class_topic = reg["강의"]["주제"]
        if class_topic not in grouped_registrations:
            grouped_registrations[class_topic] = []
        grouped_registrations[class_topic].append(reg["닉네임"])
    
    for topic, nicknames in grouped_registrations.items():
        st.write(f"### {topic}")
        for nickname in nicknames:
            st.write(nickname)

# 네비게이션
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["수강정보 입력", "수강신청", "수강신청 결과"])

if page == "수강정보 입력":
    input_class_info()
elif page == "수강신청":
    register_for_class()
elif page == "수강신청 결과":
    view_registration_results()
