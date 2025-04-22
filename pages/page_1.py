# import thư viện 
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from random import randint
import streamlit as st
import io

# ghi tiêu đề cho page1
st.title("📃 Khám Phá dữ liệu định lượng") 

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

# tạo list danh sách của các màu cơ bản
color_list = [
    "red", "blue", "green", "yellow", "purple",
    "orange", "pink", "brown", "gray", "cyan",
    "magenta", "lime", "indigo", "violet", "gold",
    "silver", "navy", "teal", "coral", "maroon"
]

# tạo list danh sách các mầu của biến palette 
palettes = [
# Bộ màu mặc định (Categorical Palettes)
"deep", "muted", "bright", "pastel", "dark", "colorblind",

# Bộ màu Gradient (Sequential Palettes)
"Blues", "Reds", "Greens", "coolwarm", "magma", "viridis"
]

# xây dựng hàm vẽ biểu đồ phân phối cho các biến dữ liệu định lượng
def ve_bieu_do_phan_phoi(so_hang,so_cot,ten_cac_cot,x_label,ten_bieu_do):
    fig,ax = plt.subplots(ncols=so_cot,nrows=so_hang,figsize=(20,10))
    index = 0
    for i in range(so_hang):
        for j in range(so_cot):
            try:
                sns.histplot(data[ten_cac_cot[index]],bins=20,ax=ax[i,j],color=color_list[index],kde=True)
            except:
                print(1)
            index+=1
    fig.suptitle(ten_bieu_do)
    fig.supxlabel(x_label)
    st.pyplot(fig)

# Xây dựng hàm vẽ biểu đồ cột về sản lượng bán theo từng hãng
def ve_bieu_do_cot_tong_so_luon_ban(ten_cot,ten_bieu_do):
    df_cot = data[ten_cot].value_counts().reset_index().sort_values(by='count')
    ten = df_cot[ten_cot]
    values = df_cot['count']
    x_coordinate = [i for i in range(len(ten))]
    plt.figure(figsize=(20,5))
    sns.barplot(x=ten_cot,y='count',data=df_cot,palette=palettes[randint(0,len(palettes)-1)])
    plt.title(ten_bieu_do + "\n")
    plt.xticks(rotation=45,ha='right');
    for x,y in zip(x_coordinate,values):
        plt.text(x-0.1,y+13,y)

# xây dựng hàm vẽ biểu đồ tròn thể hiện phần trăm số lượng bán hàng và doanh thu theo từng hãng
def ve_bieu_do_tron(ten_cot,ten_bieu_do):
    df_cot = data[ten_cot].value_counts().reset_index().sort_values(by='count')
    ten = df_cot[ten_cot]
    values = df_cot['count']
    percents = []
    for i in range(len(ten)):
        percent = (values[i]/(values.sum()))*100
        percents.append(float(percent))
    percents = sorted(percents,reverse=False)
    plt.pie(percents,labels=ten,autopct="%1.1f%%",colors=color_list[0:len(ten)]);
    plt.legend(loc="center left",bbox_to_anchor=(1.1,0.5))
    plt.title(ten_bieu_do)

# xây dựng hàm vẽ biểu đồ cột tổng doanh thu theo từng loại
def ve_bieu_do_cot_tong_doanh_thu(ten_cot,ten_bieu_do):
    df_cot = data.groupby(ten_cot)["Price ($)"].sum().reset_index().sort_values(by="Price ($)")
    ten = df_cot[ten_cot]
    values = df_cot['Price ($)']
    x_coordinate = [i for i in range(len(ten))]
    plt.figure(figsize=(20,5))
    sns.barplot(x=ten_cot,y="Price ($)",data=df_cot,palette=palettes[randint(0,len(palettes)-1)])
    plt.xticks(rotation=45,ha='right');
    plt.title("Biểu đồ tổng doanh thu theo Brand")
    for x,y in zip(x_coordinate,values):
        plt.text(x-0.25,y+100,str(round(y/1000000,2)) + " triệu đô")
    plt.title(ten_bieu_do)

# xây dựng hàm vẽ biểu đồ tròn thể hiện phần trăm tổng doanh thu theo loại
def ve_bieu_do_phan_tram_tong_doanh_so(ten_cot,ten_bieu_do):    
    df_cot = data.groupby(ten_cot)["Price ($)"].sum().reset_index().sort_values(by="Price ($)")
    ten = df_cot[ten_cot]
    values = df_cot['Price ($)']
    percents = []
    for i in range(len(ten)):
        percent = (values[i]/(values.sum()))*100
        percents.append(float(percent))
    percents = sorted(percents,reverse=False)
    plt.pie(percents,labels=ten,autopct="%1.1f%%",colors=color_list[0:len(ten)]);
    plt.title(ten_bieu_do)
    plt.legend(loc="center left",bbox_to_anchor=(1.1,0.5))

# xây dựng hàm để vẽ biểu đồ cột với nhiều giá trị cung một lúc ( 1 x và nhiều y)
def ve_nhieu_bieu_do_cot(danh_sach_ten_cot,ten_bieu_do,ten_cot_can_ve_theo,ds_gia_tri_ve_theo_cot):
    df_new = data[danh_sach_ten_cot]
    df_melted = df_new.melt(id_vars=[ten_cot_can_ve_theo], var_name="Loại", value_name="Giá trị")
    df_melted = df_melted.sort_values(by='Giá trị')
    plt.figure(figsize=(20, 5))
    loai = df_melted["Loại"].value_counts().index.to_list()
    sns.barplot(x=ten_cot_can_ve_theo, y="Giá trị", hue="Loại", data=df_melted,palette=palettes[randint(0,len(palettes)-1)],estimator=sum)
    plt.xticks(rotation=45,ha='right')
    plt.title(ten_bieu_do)
    ds_df_tra_ve = []
    for i in range(len(ds_gia_tri_ve_theo_cot)):
        loc_theo_loai = df_melted[df_melted["Loại"] ==  loai[i]]
        values_count = loc_theo_loai.groupby(ten_cot_can_ve_theo)['Giá trị'].sum().reset_index().sort_values(by='Giá trị')
        ds_df_tra_ve.append(values_count)
    return ds_df_tra_ve

# xây dựng hàm để vẽ biểu đồ đường trong nhiều trường hợp 
def ve_bieu_do_duong(danh_sach_ten_cot,ten_cot_can_ve_theo,ten_bieu_do,dk):
    if(dk == "%"):
        df_new = data[danh_sach_ten_cot]
        df_melted = df_new.melt(id_vars=[ten_cot_can_ve_theo], var_name="Loại", value_name="Giá trị")
        plt.figure(figsize=(20, 5))
        df_melted
        loai = df_melted["Loại"].value_counts().index.to_list()
        ds_marker = ['o','p','s','D','X']
        ds_loai = []
        for i in range(2):
            df_loai = df_melted[df_melted['Loại'] == loai[i]]
            group_theo_giaTri = df_loai.groupby(ten_cot_can_ve_theo)["Giá trị"].sum()
            ten = group_theo_giaTri.index.tolist()
            values = group_theo_giaTri.values.tolist()
            ds_loai.append(values)
            plt.plot(ten,values,marker=ds_marker[i],ms=10,label=loai[i])
        x = [i for i in range(len(ten))]
        percent = ((np.array(ds_loai[0]) - np.array(ds_loai[1]))/np.array(ds_loai[1]))*100
        index=0
        for x,y in zip(x,percent):
            plt.text(x,values[index]+100,str(round(abs(y),2))+"%")
            index+=1
        plt.title(ten_bieu_do)
        plt.legend()
        print(loai)
        return ten,percent
    elif(dk=="1"):
        plt.figure(figsize=(20, 5))
        df_new = data[danh_sach_ten_cot]
        sns.lineplot(x=ten_cot_can_ve_theo,y=danh_sach_ten_cot[1],data=df_new)
        plt.title(ten_bieu_do)
        plt.legend()
    elif(int(dk) > 1):
        df_new = data[danh_sach_ten_cot]
        df_melted = df_new.melt(id_vars=[ten_cot_can_ve_theo], var_name="Loại", value_name="Giá trị")
        plt.figure(figsize=(20, 5))
        df_melted
        loai = df_melted["Loại"].value_counts().index.to_list()
        sns.lineplot(x=ten_cot_can_ve_theo,y="Giá trị",data=df_melted,hue='Loại',markers='D')
        plt.title(ten_bieu_do)

# Hàm vẽ biểu đồ boxplot 
def ve_bieu_do_box_plot(danh_sach_ten_cot,ten_bieu_do,hue):
    df = data[danh_sach_ten_cot]
    plt.figure(figsize=(20,5))
    sns.boxplot(x=df[danh_sach_ten_cot[0]],y=df[danh_sach_ten_cot[1]],data=df,hue=hue,palette=palettes[randint(0,len(palettes)-1)])
    plt.title(ten_bieu_do)    
    plt.xticks(rotation=45,ha='right')
    plt.legend()

# Hàm vẽ bểu đồ violin plot
def ve_bieu_do_violin_plot(danh_sach_ten_cot,ten_bieu_do,hue):
    df = data[danh_sach_ten_cot]
    plt.figure(figsize=(20,5))
    sns.violinplot(x=df[danh_sach_ten_cot[0]],y=df[danh_sach_ten_cot[1]],data=df,hue=hue,palette=palettes[randint(0,len(palettes)-1)],split=True)
    plt.title(ten_bieu_do)    
    plt.xticks(rotation=45,ha='right')
    plt.legend()

# Hàm để vẽ biểu đồ poinplot
def ve_bieu_do_poinplot(danh_sach_ten_cot,ten_bieu_do,hue):
    df = data[danh_sach_ten_cot]
    means = df.groupby(danh_sach_ten_cot[0])[danh_sach_ten_cot[1]].mean().sort_values()
    order = means.sort_values().index
    plt.figure(figsize=(20,5))
    sns.pointplot(x=danh_sach_ten_cot[0],y=danh_sach_ten_cot[1],data=df,hue=hue, capsize=0.2,order=order)
    for ten,mean in enumerate(means):
        plt.text(ten,mean,round(mean,2))
    plt.title(ten_bieu_do)
    print(means)


# # lấy ra các cột có kiểu dữ liệu là int và float
cot_dinh_luong = data.select_dtypes(include=['int','float']).columns
st.subheader("Các cột định lượng trong data")
st.write(cot_dinh_luong)
st.header("Phân Tích Dữ Liệu Định Lượng")

# # vẽ biểu đồ phân phối của các biến định lượng
ve_bieu_do_phan_phoi(2,3,cot_dinh_luong,"Tên của biểu đồ","Biểu đồ phân phối của các biến định lương")
st.write("========================================================================================")

st.markdown(""" 
### 📊 ***Phân tích biểu đồ phân phối của các biến numeric***
 - *Các biến numeric bao gôm 'RAM (GB)','Screen Size (inch)','Battery Life (hours)','Weight (kg)','Price ($)','LY price'*
 - *Phân tích:*  
         <div style="margin-left: 40px">
         + ta thấy đôi với hai biến đầu tiên là RAM và screen size thì biểu đồ phân phối là biểu đồ lệch chúng chỉ tập chung vào một số điểm nhất dịnh như 8,16,32,64   
         đối với ram và 13,14,16,17 đối với screen size , nhưng trên thực tế ta thấy rằng đối với ram và screen size thì các hãng chỉ sản xuất tập trung vào một   
         số mốc nhát định như ở trên vì vậy khi chúng ta chỉ quan sát đến những điểm đó ta thấy dữ liệu phân bố khá đều không chỗ nào cao quá và cũng   
         không chỗ nào thấp quá   
         ====>> : ta thấy rằng nhu cầu sử dụng của khách hàng với screen size và ram đều khá đều , không có một loại nào mà khách hàng có sự lựa chọn ưu tiên đặc biệt   
         đa phân họ sẽ chọn theo nhu cầu sử dụng của bản thân   
         + đối với weight và battery thì thay thấy biểu đồ phân phối của chúng là biểu đồ phân phối đều trải dài từ đầu đến cuối không lệch ở dâu cả tuy nhiên đây lại  
         là thông tin không có giá trị vì trên thực tế thì battery còn dựa vào thời gian sử dụng của các nhân và weight thì vô cùng đa dạng đến từ nhà sản suất  
         =====>> : trên thực tế người ta thường không quan tâm đến những thông tin này khi mua máy   
         + LY price và price : thấy thấy hai biểu đồ phân phối của hai feature này đều là hai biểu đồ lệch trái từ đó thấy  
         =====>> : nhu cầu sử dụng máy tính và giá của năm 2024 so với năm 2023 không thay đổi , khách hàng vẫn tập trung chủ yếu vào sử dụng những laptop   
         giá tầm vừa và rẻ , khôn nhiều khách hàng chịu bỏ số tiền lớn để mua lap top , Ta thấy được sự ổn định của thị trường       
         </div>""")

st.write("========================================================================================")

# # biểu đồ heapmap tương quan của các biến định lượng
plt.figure(figsize=(15,10))
sns.heatmap(data.select_dtypes(include=['int','float']).corr(),annot=True,cmap='coolwarm')
plt.title("Biểu đồ tương quan giưa các biến định lượng")
st.pyplot(plt)

st.markdown("""
### 📊 ***Phân tích biểu đồ tương quan giữa các biến định lượng (Phục cho cho Machine learning và AI)***  
 - *Ta thấy biểu đồ heapmap có sự tương quan rất là thấp đa phần chỉ là 0.06 .. , mức tương quan cao nhất cũng chỉ là 0.62*  
 - *từ đó ta thấy dữ liệu sẽ phù hợp hơn với những model phi tuyến như SVM , randomforest , ...*
""")

st.write("========================================================================================")

# viết phân tích bằng st.markdown
st.subheader("Thống kê các cột numeric dữ liệu")
st.markdown("""
### 📊 Phân tích thống kê mô tả (Descriptive Statistics)
 
 Dưới đây là bảng thống kê mô tả cho tập dữ liệu laptop với 6 thuộc tính quan trọng:
 
 | Thuộc tính             | Trung bình | Độ lệch chuẩn | Min   | 25%   | 50% (Median) | 75%   | Max     |
 |------------------------|------------|----------------|--------|--------|---------------|--------|-----------|
 | **RAM (GB)**           | 24.84      | 21.75          | 4.0    | 8.0    | 16.0          | 32.0   | 64.0      |
 | **Screen Size (inch)** | 15.21      | 1.44           | 13.3   | 14.0   | 15.6          | 16.0   | 17.3      |
 | **Battery Life (hrs)** | 8.03       | 2.30           | 4.0    | 6.0    | 8.0           | 10.0   | 12.0      |
 | **Weight (kg)**        | 2.34       | 0.67           | 1.2    | 1.76   | 2.34          | 2.91   | 3.5       |
 | **Price ($)**          | 2183.42    | 1316.75        | 279.6  | 1272.2 | 1839.97       | 2698.0 | 10807.9   |
 | **LY Price ($)**       | 2083.42    | 1316.75        | 179.6  | 1172.2 | 1739.97       | 2598.0 | 10707.9   |
 
 ---
 
#### 🧪 Phân tích dạng phân phối dữ liệu
 
 - **RAM, Price, LY Price** có độ lệch lớn giữa mean và median, và max rất cao → phân phối **lệch phải** (right-skewed). Dữ liệu có thể chứa nhiều giá trị ngoại lai (outliers).
 - **Screen Size** có mean ≈ median và std nhỏ → có xu hướng gần **phân phối chuẩn**.
 - **Battery Life** và **Weight** cũng có phân phối tương đối cân đối, với độ lệch chuẩn thấp → có thể gần **phân phối chuẩn**.
 
#### 📌 Gợi ý: nên trực quan hóa với biểu đồ Histogram hoặc Boxplot để kiểm tra trực tiếp dạng phân phối.
 
 ---
 
#### 📈 Mức độ phân tán (Coefficient of Variation)
 
 Hệ số biến thiên (CV = std / mean) giúp đánh giá mức độ phân tán tương đối:
 
 | Thuộc tính            | CV        | Đánh giá                      |
 |------------------------|-----------|-------------------------------|
 | **RAM**                | ≈ 0.87    | 🔴 Phân tán mạnh              |
 | **Screen Size**        | ≈ 0.095   | 🟢 Rất đồng đều               |
 | **Battery Life**       | ≈ 0.29    | 🟡 Phân tán trung bình        |
 | **Weight**             | ≈ 0.29    | 🟡 Phân tán trung bình        |
 | **Price**              | ≈ 0.60    | 🔴 Phân tán mạnh              |
 | **LY Price**           | ≈ 0.63    | 🔴 Phân tán mạnh              |
 
 ---
 
#### ⚖️ So sánh giữa các cột
 
 - **RAM** và **Price**: Có khả năng tương quan dương. Máy RAM cao thường đi kèm giá cao.
 - **Battery Life** và **Weight**: Có thể có quan hệ nghịch chiều – thiết bị nhẹ có thể ít pin hơn.
 - **Price** và **LY Price**: Hai cột giá gần nhau và rất có thể có tương quan tuyến tính mạnh.
 - **Screen Size** và **Weight**: Có thể màn hình to → máy nặng hơn. Nên kiểm tra qua biểu đồ scatter.
 
#### 📌 Gợi ý:
 - Dùng biểu đồ scatter để kiểm tra tương quan giữa các cặp biến liên tục.
 - Có thể tạo ma trận tương quan bằng `.corr()` để xem tổng quan các mối quan hệ.
 
 ---
 
#### 🧠 Kết luận
 
 - Các thuộc tính như **RAM**, **Price**, **LY Price** có độ phân tán lớn, chứa nhiều outlier → cần xử lý trước khi modeling.
 - **Screen Size**, **Battery Life**, **Weight** có phân phối khá ổn định, phù hợp để đưa vào mô hình mà không cần biến đổi phức tạp.
 - Nên tiếp tục phân tích tương quan và trực quan hóa để phát hiện mối quan hệ tiềm năng giữa các biến.
 
 


""")


