# import thư viện 
import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, OrdinalEncoder,StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Ghi tiêu đề cho wedsite 
st.title("📊 Dashboard Phân Tích Dữ Liệu")

# Thu thập dữ liệu
data = pd.read_csv('C:\DATA\laptop_prices.csv')
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

# Tiền sử lý dữ liệu

# + xử lý các giá trị thiếu
cot_co_gia_tri_null = data.columns[data.isnull().any()]
for i in range(len(cot_co_gia_tri_null)):
    if(data[cot_co_gia_tri_null[i]].dtype == 'O'):
        data[cot_co_gia_tri_null[i]].fillna(data[cot_co_gia_tri_null[i]].mode()[0],inplace=True)
    elif(data[cot_co_gia_tri_null[i]].dtype == 'float'):
        data[cot_co_gia_tri_null[i]].fillna(data[cot_co_gia_tri_null[i]].mean(),inplace=True)

# + Xử lý các giá trị trùng lặp
data = data.drop_duplicates(keep='first')
data.duplicated().sum()

# + Chuyển đổi kiểu dữ liệu
data['RAM (GB)'] = data['RAM (GB)'].astype('int')
data.info()

# + Chuẩn hóa dữ liệu


# + Tạo các biến mới nếu cần


# Khám phá dữ liệu

# + Khám phá dữ liệu định lượng
st.header("Biểu đồ dữ liệu định lượng")
cot_dinh_luong = data.select_dtypes(include=['int','float']).columns.to_list()  

# vẽ các biểu đồ phân phối của biến định lượng
fig,ax=plt.subplots(ncols=3,nrows=2,figsize=(30,20))
colors=['red','green','blue','yellow','brown','pink','maron','black']
index = 0
for i in range(2):
    for j in range(3):
        try:
            sns.histplot(data[cot_dinh_luong[index]],bins=20,ax=ax[i,j],color=colors[index])
        except:
            print(1)
        index+=1
fig.suptitle("Biểu đồ phân phối của các biến định lượng")
fig.supxlabel("Tên của biểu đồ")
fig.supylabel("Giá trị phân phối")
st.pyplot(fig)

# vẽ biểu đồ tương quan của các biến định lượng
plt.figure(figsize=(8, 5))
sns.heatmap(data.select_dtypes(include=['int','float']).corr(),annot=True,cmap='coolwarm')
plt.title("Biểu đồ tương quan giưa các biến định lượng")
st.pyplot(plt)

# Biểu đồ mối tương quan của tất cả các biến định lượng
plt.figure(figsize=(8, 5))
sns.pairplot(data,hue='Brand')
st.pyplot(plt)

# thống kê cơ bản của các biến định lượng
thong_ke = data.describe()
st.write("Thống kê cơ bản")
st.dataframe(thong_ke)


# + Khám phá dữ liệu định tính
st.header("Biểu đồ của dữ liệu định tính")

# lấy ra các cột có kiểu dữ liệu là oject
cot_dinh_tinh = data.select_dtypes(include=['O']).columns.to_list()

# vẽ biểu đồ tổng số lượng của máy tính theo từng mục
fig,ax=plt.subplots(ncols=2,nrows=3,figsize=(30,10))
index=0
for i in range(3):
    for j in range(2):
        try:
            sns.countplot(x=cot_dinh_tinh[index],data=data,ax=ax[i,j],color=colors[index])
            ax[index].title(cot_dinh_tinh[index])
        except:
            print(1)
        index+=1
fig.suptitle(" Biểu đồ sản lương bán máy tính theo từng danh mục")
st.pyplot(fig)

# + Khám phá mối quan hệ giữa biến định tính và biến định lượng

# biểu đồ Boxplot của các biến định tính
box_columns = ['Brand','Processor','Storage','Operating System','GPU','Resolution']
index=0
fig,ax = plt.subplots(ncols=2,nrows=3,figsize=(22,10))
for i in range(3):
    for j in range(2):
        try:
            sns.boxplot(x=box_columns[index],y='Price ($)',data=data,hue=box_columns[index],ax=ax[i,j],color=colors[index]);
            index+=1
        except:
            print(123)
fig.suptitle("Biểu đồ so sánh giá của máy tính theo từng mục")
st.pyplot(fig)

# biểu đồ cột của các biến định tính
bar_columns = ['Brand','Processor','Storage','Operating System','GPU','Resolution']
index=0
fig,ax = plt.subplots(ncols=2,nrows=3,figsize=(22,10))
for i in range(3):
    for j in range(2):
        try:
            sns.barplot(x=box_columns[index],y='Price ($)',data=data,hue=box_columns[index],ax=ax[i,j],color=colors[index]);
            index+=1
        except:
            print(123)
fig.suptitle("Biểu đồ so sánh doanh thu của máy tính quý 4 theo từng mục")
st.pyplot(fig)

# giá trung bình và khoảng tin cậy của máy tính theo từng cột 
poin_columns = ['Brand','Processor','Storage','Operating System','GPU','Resolution']
index=0
fig,ax = plt.subplots(ncols=2,nrows=3,figsize=(22,20))
for i in range(3):
    for j in range(2):
        try:
            sns.pointplot(x=poin_columns[index],y='Price ($)',data=data,hue=poin_columns[index],ax=ax[i,j],color=colors[index]);
            index+=1
        except:
            print(123)
fig.suptitle("Biểu đồ so sánh giá của máy tính  theo từng mục")
st.pyplot(fig)

# biểu đồ tương quan giữa ram và price
plt.figure(figsize=(20,10))
sns.lineplot(x='RAM (GB)',y='Price ($)',data=data)
plt.title("biểu đồ xu hướng giá của máy tính theo RAM")
st.pyplot(plt)

# biểu đồ hồi quy của ram và price
plt.figure(figsize=(20,10))
sns.regplot(x='RAM (GB)',y='Price ($)',data=data)
plt.title("biểu đồ hồi quy giá của máy tính theo RAM")
st.pyplot(plt)

# biểu đồ tương quan  giữa màn hình và giá máy tính
plt.figure(figsize=(20,10))
sns.lineplot(x='Screen Size (inch)',y='Price ($)',data=data)
plt.title("biểu đồ xu hướng giá của máy tính theo kích thước màn hình")
st.pyplot(plt)

# biểu đồ hồi quy giữa màn hình và giá
plt.figure(figsize=(20,10))
sns.regplot(x='Screen Size (inch)',y='Price ($)',data=data)
plt.title("biểu đồ hồi quy giá của máy tính theo kích thước màn hình")
st.pyplot(plt)


plt.figure(figsize=(20,10))
sns.lineplot(x='Battery Life (hours)',y='Price ($)',data=data)
plt.title("biểu đồ xu hướng giá của máy tính theo tuổi đời bin")
st.pyplot(plt)


plt.figure(figsize=(20,10))
sns.regplot(x='Battery Life (hours)',y='Price ($)',data=data)
plt.title("biểu đồ hồi quy giá của máy tính theo tuổi đời bin")
st.pyplot(plt)


plt.figure(figsize=(20,10))
sns.lineplot(x='Weight (kg)',y='Price ($)',data=data)
plt.title("biểu đồ xu hướng giá của máy tính theo cân nặng")
st.pyplot(plt)


plt.figure(figsize=(20,10))
sns.regplot(x='Weight (kg)',y='Price ($)',data=data)
plt.title("biểu đồ hồi quy giá của máy tính theo cân nặng")
st.pyplot(plt)

# : Phân tích chuyên sâu và mô hình hóa dữ liệu
#  + Phân tích nâng cao
# + Kiểm định giải thuyết

# + Phân tích hồi quy

# feature Ram screen ing Brand  Processer Resolution
data_new = data[['Brand','Processor','RAM (GB)','Screen Size (inch)','Resolution','Price ($)']]

# + xử lý dữ liệu danh mục

# One-Hot Encoding cho cột đầu tiên (Brand)
# Label Encoding cho cột thứ hai (Category) -> Dùng OrdinalEncoder để tương tự LabelEncoder
ct = ColumnTransformer(
    transformers=[
        ('one', OneHotEncoder(), [0]),   # One-Hot Encoding cho cột 0 (Brand)
        ('label', OrdinalEncoder(), [1]),    # Label Encoding cho cột 1 (Category)
        ('two', OneHotEncoder(), [4])
    ],
    remainder="passthrough"  # Giữ nguyên các cột còn lại (Price)
)

# Áp dụng biến đổi
data_transformed = ct.fit_transform(data_new)

# Chuyển kết quả về DataFrame
columns = (
    list(ct.named_transformers_['one'].get_feature_names_out(['Brand'])) + ['Processor']  + list(ct.named_transformers_['two'].get_feature_names_out(['Resolution'])) + ['RAM (GB)'] + ['Screen Size (inch)'] + ['Price ($)']
)
data_transformed = pd.DataFrame(data_transformed, columns=columns)


# + xử lý nomalization và standardzation
scaler_standard = StandardScaler()
data_transformed[['RAM (GB)','Screen Size (inch)','Price ($)']] = scaler_standard.fit_transform(data_transformed[['RAM (GB)','Screen Size (inch)','Price ($)']])

# + chia ra thành x train y train x test y test

# lấy ra các biến độc lập x
x = data_transformed.iloc[:,:17]

# lấy ra biến phụ thuộc y
y = data_transformed.iloc[:,17:18]

# chia tập dữ liệu thành tập test và tập train
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2)

# + Xây dựng model hồi quy dự đoán giá của máy tính
model = LinearRegression()
model.fit(x_train,y_train)

# xây dựng form nhập dữ liệu từ người sử dụng để dự đoán giá của máy tính
st.write("### 🤖 Dự đoán giá của máy tính")
ram = st.number_input("Máy của bạn có bao nhiêu RAM: ", min_value=0)
brand = st.text_input("Máy của bạn hãng gì")
processer = st.text_input("Máy của bạn sử dụng spu gì")
screen_ing = st.text_input("máy tính của bạn bao nhiêu ing")
Resolution = st.text_input(" độ phân giải màn hỉnh của bạn là bao nhiêu")


if st.button("Dự đoán"):
    pred = model.predict([[brand, processer, ram,screen_ing,Resolution]])[0]
    st.success(f"📌 Hành vi dự đoán: {pred}")


st.image("hung.jpg", caption="content", use_column_width=True)