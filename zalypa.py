import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

uploaded_file = st.file_uploader("Загрузите CSV файл", type=["csv"])
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
else:
    st.write("Пожалуйста, загрузите CSV файл.")

if 'data' in locals():
    st.sidebar.header("Настройки")
    
    x_variable = st.sidebar.selectbox("Выберите первую переменную", data.columns)
    y_variable = st.sidebar.selectbox("Выберите вторую переменную", data.columns)

    st.header("Визуализация распределения переменных")
    
    if data[x_variable].dtype == 'object':
        x_counts = data[x_variable].value_counts()
        st.subheader(f"Распределение {x_variable}")
        st.write(x_counts)
        plt.figure(figsize=(8, 8))
        plt.pie(x_counts, labels=x_counts.index, autopct='%1.1f%%', startangle=140)
        st.pyplot()
    else:
        st.subheader(f"Распределение {x_variable}")
        plt.figure(figsize=(12, 6))
        sns.histplot(data[x_variable], kde=True)
        st.pyplot()

    if data[y_variable].dtype == 'object':
        y_counts = data[y_variable].value_counts()
        st.subheader(f"Распределение {y_variable}")
        st.write(y_counts)
        plt.figure(figsize=(8, 8))
        plt.pie(y_counts, labels=y_counts.index, autopct='%1.1f%%', startangle=140)
        st.pyplot()
    else:
        st.subheader(f"Распределение {y_variable}")
        plt.figure(figsize=(12, 6))
        sns.histplot(data[y_variable], kde=True)
        st.pyplot()

    st.header("Проверка гипотез")
    test_type = st.sidebar.selectbox("Выберите проверочный алгоритм", ("t-test", "Mann-Whitney U test"))
    
    if test_type == "t-test":
        st.subheader("t-test")
        result = stats.ttest_ind(data[x_variable], data[y_variable])
        st.write("p-value:", result.pvalue)
        if result.pvalue < 0.05:
            st.write("Результаты статистически значимы!")
        else:
            st.write("Нет статистически значимых различий.")
    elif test_type == "Mann-Whitney U test":
        st.subheader("Mann-Whitney U test")
        result = stats.mannwhitneyu(data[x_variable], data[y_variable])
        st.write("p-value:", result.pvalue)
        if result.pvalue < 0.05:
            st.write("Результаты статистически значимы!")
        else:
            st.write("Нет статистически значимых различий.")

