# import thư viện 
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from random import randint
import streamlit as st
import io

# Ghi tiêu đề cho bài phân tích dữ liệu
st.title("📃 Phân tích doanh số bán máy tính sách tay trong năm 2024") 
st.header("💰 GIẢ SỬ BẠN ĐANG LÀ NHÂN VIÊN PHÂN TÍCH DỮ LIỆU CỦA MỘT CÔNG TY BÁN MÁY TÍNH SÁCH TAY VÀ BẠN ĐANG PHÂN TÍCH VỀ DỮ LIỆU BÁN HÀNG CỦA CÔNG TY TRONG NĂM 2024")

# # load dataset
@st.cache_data
def load_data():
    data = pd.read_csv('C:\DATA\laptop_prices.csv')
    data['LY price'] = data['Price ($)'] - 100
    months = ["January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"]
    months_of_df = []
    for i in range(len(data)):
        months_of_df.append(months[randint(0,len(months)-1)])
    data['months'] = months_of_df
    return data
data = load_data()
st.subheader("Dữ liệu Doanh số bán máy tính và hành vi mua máy tính của khách hàng 2024:")
st.write(data)
st.subheader("5 sample đầu của dữ liệu")
st.write(data.head(5))
st.subheader("5 sample cuối của dữ liệu")
st.write(data.tail(5))
st.subheader("Thông tin tổng quát của dữ liệu")

# hiện thị dữ liệu console 
buffer = io.StringIO()
data.info(buf=buffer)
info_str = buffer.getvalue()

# Dùng st.code() để hiển thị như console (giữ format + xuống dòng)
st.code(info_str, language="text")

# Phân tích tổng quan về dữ liệu
st.markdown("### 📁 ***Tổng quan về dữ liệu***", unsafe_allow_html=True)
st.markdown("""
- *Dữ liệu được thu thập từ cơ sở dữ liệu về doanh số bán hàng của công ty trong năm 2024 bằng SQL*  
- *Tập dữ liệu nói về nhu cầu mua, sử dụng và xu hướng chọn mua máy laptop cá nhân của khách hàng trong 1 năm qua*  
- *Tập dữ liệu bao gồm những thông tin cơ bản sau:*
    + *Dữ liệu có tổng cộng 11771 sample*
    + *Dữ liệu có 13 feature (columns) bao gồm:*
        <div style="margin-left: 40px">
        • <b>Brand</b>: Nói về các hãng máy tính như Apple, MSI, Asus, ...  <br>
        • <b>Processor</b>: chứa thông tin về các bộ xử lý của máy tính như AMD Ryzen, Intel i3, i5, i7...  <br>
        • <b>RAM (GB)</b>: dung lượng RAM mà máy tính có (GB)  <br>
        • <b>Storage</b>: thông tin về dung lượng ổ cứng và loại ổ SSD hoặc HDD  <br>
        • <b>GPU</b>: thông tin GPU như Nvidia RTX 3080, RTX 3198...  <br>
        • <b>Screen Size (inch)</b>: kích thước màn hình (inch)  <br>
        • <b>Resolution</b>: độ phân giải màn hình  <br>
        • <b>Battery Life (hours)</b>: vòng đời pin của laptop  <br>
        • <b>Weight (kg)</b>: trọng lượng của máy  <br>
        • <b>Operating System</b>: hệ điều hành như Windows, macOS, Linux...  <br>
        • <b>Price ($)</b>: giá bán của laptop  <br>
        • <b>LY price</b>: giá của laptop cùng kỳ năm ngoái  <br>
        • <b>months</b>: các tháng trong năm  
        </div>  
    + *Trong đó có 6 feature kiểu dữ liệu `float64` và 7 feature kiểu `object`*  
    + *Tập dữ liệu sử dụng hết ~1.2MB bộ nhớ chính*
""", unsafe_allow_html=True)

# vẽ biểu đồ tổng số lượng null của mỗi cột
total_null_columns = data.isna().sum().reset_index()
plt.figure(figsize=(20,5))
sns.barplot(x='index',y=0,data=total_null_columns,hue='index')
x = [i for i in range(len(total_null_columns))]
for i,j in zip(x,total_null_columns[0]):
    if(j != 0):
        plt.text(i,j,j)
plt.title("Số lượng giá trị null của mỗi cột")
st.pyplot(plt)
st.subheader("Số sample và columns của data")
st.write(data.shape)

# hiện thị lên các cột có giá trị null và tổng số null của mỗi cột
st.subheader("Các column có giá trị null và số lượng null của mỗi cột")
cot_co_gia_tri_null = data.columns[data.isnull().any()]
sum_null = data.isna().sum()
c1,c2 = st.columns(2)
with c1:
    st.write("📊 Số lượng missing value")
    st.dataframe(sum_null)
with c2:
    st.write("📋 Tên các cột có missing value")
    st.dataframe(cot_co_gia_tri_null)

st.markdown("""### ⚠️ ***Dữ liệu thiếu***
 - *Các cột có giá trị thiếu bao gồm :*
     + *Brand: 85 miss , Processer: 44 miss, RAM : 15 miss,Battery Life : 4 miss,Operating System : 5 miss*
 """)

# xử lý các giá trị bị null
for i in range(len(cot_co_gia_tri_null)):
    if(data[cot_co_gia_tri_null[i]].dtype == 'O'):
        data[cot_co_gia_tri_null[i]].fillna(data[cot_co_gia_tri_null[i]].mode()[0],inplace=True)
    elif(data[cot_co_gia_tri_null[i]].dtype == 'float'):
        data[cot_co_gia_tri_null[i]].fillna(data[cot_co_gia_tri_null[i]].mean(),inplace=True)

# xóa đi các giá trị trùng lặp
data = data.drop_duplicates(keep='first')

# chuyển đổi kiểu dữ liệu của các column trong data
data['RAM (GB)'] = data['RAM (GB)'].astype('int')
