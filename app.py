import streamlit as st
import pandas as pd
import pickle

st.title("تطبيق توقعات الذكاء الاصطناعي")

# محاولة تحميل الموديل
try:
    with open('model.pkl', 'rb') as file:
        model = pickle.load(file)
    st.success("تم تحميل الموديل بنجاح! جاهز لاستقبال البيانات.")
except Exception as e:
    st.error(f"حدث خطأ أثناء تحميل الموديل: {e}")

st.write("جاري تجهيز واجهة إدخال البيانات...")
