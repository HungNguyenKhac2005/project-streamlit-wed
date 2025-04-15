# import thư viện 
import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Ghi tiêu đề cho wedsite 
st.title("📊 Dashboard Phân Tích Dữ Liệu")
st.write("Tên nhóm: Super data")
st.write("Tên thành viên")
st.write("- 2221050493 - Vũ Hoài Nam")
st.write("- 2321050040 - Nguyễn Khắc Hưng")


# Thu thập dữ liệu
data = pd.read_csv('https://raw.githubusercontent.com/nv-thang/DataVisualizationCourse/refs/heads/main/Dataset%20for%20Practice/movies.csv')
st.write("### 🔍 Dữ liệu gốc:")

# Chiếu dataframe lên streamlit
st.dataframe(data)

# chiếu 5 dòng đầu lên streamlit
st.write("5 dòng đầu của dataframe")
st.dataframe(data.head(5))

# chiếu 5 dòng cuối lên streramlit
st.write("5 dòng cuối của dataframe")
st.dataframe(data.tail(5))

data.shape


plt.figure(figsize=(20,5))
genre = data['genre'].value_counts()
the_loai = genre.index.to_list()
total = genre.values.tolist()
sns.barplot(x=the_loai,y=total,palette='coolwarm')
plt.title("Biểu đồ số lượng phim được khác hàng xem")
plt.xticks(rotation=45,ha='right')
st.pyplot(plt)


plt.figure(figsize=(20,5))
runtime = data.groupby("genre")['runtime'].mean()
the_loai = runtime.index.to_list()
gia_tri_trung_binh = runtime.values.tolist()
sns.barplot(x=the_loai,y=gia_tri_trung_binh,palette='viridis')
plt.title("Biểu đồ về thời gian trung bình của bộ phim theo phút")
plt.xticks(rotation=45,ha='right')
st.pyplot(plt)


plt.figure(figsize=(20,5))
plt.scatter(data['votes'],data['score'])
plt.title("Biểu đồ tương quan giữa score và votes")
st.pyplot(plt)


corr = data[data.select_dtypes(include=['int','float']).columns.to_list()].corr()
sns.heatmap(corr,annot=True)
plt.title("Biểu đồ tương quan giữa các biến numeric")
st.pyplot(plt)
