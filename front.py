import streamlit as st
import requests

st.title('Bank Project')

api_url = 'http://127.0.0.1:8002/predict/'

person_age = st.number_input('Возраст', min_value=0.0,
                             max_value=100.0, step=1.0)

person_gender = st.selectbox('Пол', ['male', 'female'])

person_education = st.selectbox('Образование', ['Bachelor', 'Doctorate', 'High School', 'Master', 'Associate'])


person_incom = st.number_input('Доход', min_value=0.0, step=100.0, )

person_emp_exp = st.number_input('Стаж', min_value=0, step=1)

person_home_ownership = st.selectbox('Жильё', ['OTHER', 'OWN', 'RENT', 'MORTGAGE'])

loan_amnt = st.number_input('Сумма кредита', min_value=0.0, step=100.0)

loan_intent = st.selectbox('Цель крелита', ['EDUCATION', 'HOMEIMPROVEMENT',
                                'MEDICAL', 'PERSONAL', 'VENTURE', 'DEBTCONSOLIDATION'])

loan_int_rate = st.number_input('Процентная ставка', min_value=0.0)

loan_percent_income = st.number_input('Доход и кредит', min_value=0.0, max_value=1.0)

credit_score = st.number_input('Кредитный балл', min_value=0, step=10)

previous_loan_defaults_on_file = st.selectbox('Дефолт',['Yes', 'No'])

bank_data = {
    'person_age': person_age,
    'person_gender': person_gender,
    'person_education': person_education,
    'person_incom': person_incom,
    'person_emp_exp': person_emp_exp,
    'person_home_ownership': person_home_ownership,
    'loan_amnt': loan_amnt,
    'loan_intent': loan_intent,
    'loan_int_rate': loan_int_rate,
    'loan_percent_income': loan_percent_income,
    'credit_score': credit_score,
    'previous_loan_defaults_on_file': previous_loan_defaults_on_file
}


if st.button('Проверка'):
    try:
        answer = requests.post(api_url, json=bank_data, timeout=10)
        if answer.status_code == 200:
            result = answer.json()
            st.json(result)
            # st.success(f'Результат: {result.get('answer')}')
        else:
            st.error(f'Ошибка: {answer.status_code}')
    except requests.exceptions.RequestException:
        st.error('Не удалось  подкличится к API')






