# import thư viện 
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from random import randint
import streamlit as st
import io

# ghi tiêu đề cho page2
st.title("📃 Khám Phá dữ liệu định tính") 

# # load dataset
@st.cache_data
def load_data():
    data = pd.read_csv('laptop_prices.csv')
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

# tạo list các danh sách màu cơ bản
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
    st.pyplot(plt)

# xây dựng hàm vẽ biểu đồ tròn thể hiện phần trăm số lượng bán hàng và doanh thu theo từng hãng
def ve_bieu_do_tron(ten_cot,ten_bieu_do):
    plt.figure(figsize=(5,5))
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
    st.pyplot(plt)

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

# # lấy ra các cột có kiểu dữ liệu oject
st.subheader("các cột có kiểu dữ liệu categorical trong data")
cot_dinh_tinh = data.select_dtypes(include=['O']).columns
st.write(cot_dinh_tinh)
st.header("Phân Tích Dữ Liệu Định Tính")
st.write("========================================================================================")

# # vẽ biểu đồ sản lượng bán hàng theo Brand 
ve_bieu_do_cot_tong_so_luon_ban("Brand","Biểu đồ số lương bán theo từng hãng")

# # vẽ biểu đồ tròn thể hiện phần trăm số lượng hàng bán được theo Brand
ve_bieu_do_tron("Brand",'Phần trăm số lương hàng bán được theo Brand')

st.markdown("""
### 📊 Sản lượng bán máy tính theo Brand
 - *Ta thấy sản lượng bán máy tính của hãng Apple cao hơn so với các hãng khác 1340 sản phẩm và chiếm 11.4% tổng số máy tính chúng ta bán , mặc dù trên thực tế giá thành của hãng Apple cáo hơn các hãng khác khá nhiều từ đó ta thấy được sự uy tính của Brand cũng như sự tin tưởng của khác hàng đối với Brand này*  
 🧠 *===>> : xu hướng khác hàng thích sử dụng apple hơn so với những hãng máy tính khác* 
""")

st.write("========================================================================================")

# # biểu đồ số lương máy tính bán được theo Processer
ve_bieu_do_cot_tong_so_luon_ban("Processor","Biểu đồ số lương bán theo từng Processer")

# # %%
# # vẽ biểu đồ tròn thể hiện phần trăm số lượng hàng bán được theo Processor
ve_bieu_do_tron("Processor","Phần trăm số lương hàng bán được theo Processor")

st.markdown("""
### 📊 Sản lượng bán máy tính theo Processer
 - *Ta thấy sản lượng bán máy tính của theo intel3 cao hơn so với các Precesser khác 1610 sản phẩm và chiếm 13.4% tổng số máy tính chúng ta bán, điều này xảy ra là vì giá trị trung bình của một chiếc máy với bộ xử lý intel 3 rẻ hơn các bộ xử lý khác rất nhiều phù hợp với túi tiền của hầu hết người sử dụng , học sinh , sinh viên , và với các tác vụ làm văn phòng bình thường như kế toán kiểm toán ,.. thì intel 3 có thể làm tốt vì vậy intel 3 vẫn là lựa chọn ưa chuộng của đa số khách hàng bình thường*  
 - *Ngược lại chúng ta thấy rằng những processer như AMR7 và AMDR5 là hai sản phẩm đứng thấp nhất sản lượng bán lần lượt là 1403 và 1415 chiếm 11.9% và 12% tổng sản lượng bán vì sao lại có điều này , về cơ bản thì chip AMD chỉ phù hợp với tiều số khách hàng đó là những người tập trung vào tác vụ xử lý đồ họa như game deverloper , streamer , thiết kế đồ họa kiến trúc , ... và cộng tác AMD cũng là dòng sản phẩm đắt hơn so với intel vì vậy không được đa số khách hàng tin dùng*
 - *Có một điều khá đặc biệt là intel 5 lại là sản phẩm bán được ít thứ 3 chỉ sau AMD 7 và 5 mặc dù trên thức tế intel 5 là sản phẩm được rất nhiều khách hàng quan tâm vì sự đa dụng là xử lý tất cả các tác vụ ở mức rất ổn định của nó(Cần kiểm chứng)* 
 
 🧠 *===>> : xu hướng khách hàng thích sử dụng vẫn ưa chuộng những máy có giá thành rẻ và làm tốt các tác vụ văn phòng* 

""")
st.write("========================================================================================")

# # %%
# # Biểu đồ số lượng bán máy tính theo dung lương bộ nhớ
ve_bieu_do_cot_tong_so_luon_ban("Storage","Biểu đồ số lương bán theo từng Storage")

# # %%
# # vẽ biểu đồ tròn thể hiện phần trăm số lượng hàng bán được theo Storage
ve_bieu_do_tron("Storage","Phần trăm số lương hàng bán được theo Storage")

st.markdown("""
### 📊 Sản lượng bán máy tính theo Storge
 - *Nhìn chung thì ta có thể thấy rằng dung lượng ổ cứng không có một sản phẩm nào quá được ưa chuộng đa phần khác hàng sẽ xử dụng theo nhu cầu bản thân nếu cần thì sẽ tăng len sau , nhưng chúng ta có thể thấy rõ rằng sản phẩm ổ cứng về HHD đang bị khác hàng bỏ qua khá nhiều bằng chứng là qua ba năm 2022,2023,2024 doanh số của ổ cứng HHD đều giảm và đứng cuối cùng , riêng năm 2024 HHD bán 2302 sản phẩm chiếm 19.6% tổng sản lượng bán , thứ 2 các hãng brand cũng đã giảm sản lượng sản xuất HHD mà thay vào đó sản xuát tăng cường SSD và đa dạng hóa chúng*  
 🧠 *===>> : xu hướng khác hàng thích sử và đang đân ưa chuộng SSD hơn vì sự hiện đại của chúng* 
""")
st.write("========================================================================================")

# # %%
# # sản lượng máy tính bán được theo từng tháng trong năm
ve_bieu_do_cot_tong_so_luon_ban("months",'Biểu đồ số lương bán theo từng months')

# # %%
# # vẽ biểu đồ tròn thể hiện phần trăm số lượng hàng bán được theo months
ve_bieu_do_tron("months","Phần trăm số lương hàng bán được theo months")
st.write("========================================================================================")

# # %%
# # số lương máy tính bán được theo hệ điều hành
ve_bieu_do_cot_tong_so_luon_ban("Operating System","Biểu đồ số lượng bán theo hệ điều hành")

# # %%
# # vẽ biểu đồ tròn thể hiện phần trăm số lượng hàng bán được theo Operating System
ve_bieu_do_tron("Operating System","Phần trăm số lương hàng bán được theo Operating System")

st.markdown("""
### 📊 Sản lượng bán máy tính theo months và Operating System
 - *về months thì không có một quy luật nào cả đa phần khác hàng sẽ mua máy tính vào bất kì một ngày nào trong năm vd có thể ngày sinh nhật , ngày lãnh lưỡng*
 -  *một điểm khá bất ngờ là về sự cân bằng của các Operating System , tưởng trừng như window sẽ là sản phẩm được ưa chuộng nhất , nhưng không phải sản lượng bán của window chỉ ngang bằng một sản phẩm khá ít ngưới biết đến là freedos Nhưng trên thực thì không phải như vậy bản chất Freedos chỉ là một mã nguồn mở được viết bởi một kỹ sư IT khi microsoft không hỗ trợ MSDOS cho cong ty anh ta nữa vì vậy việc FreeDos cao chỉ vì chiêu trò thương mại của các hãng máy tính , họ sẽ cài FreeDos mã nguồn mở để sau đó người sử dụng từ cài windows lậu hoặc người dùng tự có bản quyền windows vì vậy trên thực tế thì tất cả khách hàng đều quan và có xu hướng sử dụng windows*  
 🧠 *===>> : xu hướng khác hàng thích sử và trung thành với Operating System window* 
""")


