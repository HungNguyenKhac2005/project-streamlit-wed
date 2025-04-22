# import thư viện 
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from random import randint
import streamlit as st
import io

# viết tiêu đề cho page3
st.title("📃 Khám Phá mối liên hệ giữa biến định tính và biến định lượng") 

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


# # tạo một list danh sách các màu 
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
    st.pyplot(plt)

# xây dựng hàm vẽ biểu đồ tròn thể hiện phần trăm tổng doanh thu theo loại
def ve_bieu_do_phan_tram_tong_doanh_so(ten_cot,ten_bieu_do):
    plt.figure(figsize=(5,5))    
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
    st.pyplot(plt)

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
    st.pyplot(plt)
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
        st.pyplot(plt)
        return ten,percent
    elif(dk=="1"):
        plt.figure(figsize=(20, 5))
        df_new = data[danh_sach_ten_cot]
        sns.lineplot(x=ten_cot_can_ve_theo,y=danh_sach_ten_cot[1],data=df_new)
        plt.title(ten_bieu_do)
        plt.legend()
        st.pyplot(plt)
    elif(int(dk) > 1):
        df_new = data[danh_sach_ten_cot]
        df_melted = df_new.melt(id_vars=[ten_cot_can_ve_theo], var_name="Loại", value_name="Giá trị")
        plt.figure(figsize=(20, 5))
        df_melted
        loai = df_melted["Loại"].value_counts().index.to_list()
        sns.lineplot(x=ten_cot_can_ve_theo,y="Giá trị",data=df_melted,hue='Loại',markers='D')
        plt.title(ten_bieu_do)
        st.pyplot(plt)
    

# Hàm vẽ biểu đồ boxplot 
def ve_bieu_do_box_plot(danh_sach_ten_cot,ten_bieu_do,hue):
    df = data[danh_sach_ten_cot]
    plt.figure(figsize=(20,5))
    sns.boxplot(x=df[danh_sach_ten_cot[0]],y=df[danh_sach_ten_cot[1]],data=df,hue=hue,palette=palettes[randint(0,len(palettes)-1)])
    plt.title(ten_bieu_do)    
    plt.xticks(rotation=45,ha='right')
    plt.legend()
    st.pyplot(plt)

# Hàm vẽ bểu đồ violin plot
def ve_bieu_do_violin_plot(danh_sach_ten_cot,ten_bieu_do,hue):
    df = data[danh_sach_ten_cot]
    plt.figure(figsize=(20,5))
    sns.violinplot(x=df[danh_sach_ten_cot[0]],y=df[danh_sach_ten_cot[1]],data=df,hue=hue,palette=palettes[randint(0,len(palettes)-1)],split=True)
    plt.title(ten_bieu_do)    
    plt.xticks(rotation=45,ha='right')
    plt.legend()
    st.pyplot(plt)

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
    st.pyplot(plt)




# # + Khám phá mối quan hệ giữa biến định tính và biến định lượng
st.header("Phân Tích Dữ Liệu")

# data.head()
st.write("========================================================================================")


# # vẽ biểu đồ cột tổng doanh thu theo Brand
ve_bieu_do_cot_tong_doanh_thu("Brand","biểu đồ tổng doanh thu của công ty theo brand")


# # vẽ biểu đồ trong thể hiện phần trăm tổng doanh số theo Brand 
ve_bieu_do_phan_tram_tong_doanh_so("Brand","Biểu đồ phần trăm tổng doanh thu theo Brand")

st.markdown("""
### 📊 Tổng doanh số bán máy tính theo Brand
 - *Ta thấy rằng top 3 hãng mang lại doanh thu cao nhất lần lượt là Apple , razer , MSI , 3.84tr$ , 3tr$ và 2.99tr$ chiếm ~15% , 11.7% và 11.6% , mặc dù về sản lượng bán MSI chỉ đứng thứ 3 và razer thì đứng cuối cùng nhưng doanh số của razer mang lại cao thứ 2 chỉ sau Apple từ đấy ta có thể khẳng định được giả thuyết đã đưa ra ở trên về AMD đó là giá thành của AMD cao từ đó ta thấy được rằng lươn nhuận AMD mang lại cũng sẽ là cao*

""")

   
st.write("========================================================================================")


# # vẽ biểu đồ cột tổng doanh thu theo Processor
ve_bieu_do_cot_tong_doanh_thu("Processor","biểu đồ tổng doanh thu của công ty theo Processor")


# # vẽ biểu đồ trong thể hiện phần trăm tổng doanh số theo Processor 
ve_bieu_do_phan_tram_tong_doanh_so("Processor","Biểu đồ phần trăm tổng doanh thu theo Processor")

st.markdown("""
### 📊 Tổng doanh số bán máy tính theo Processer
 - *Tương tự như phần Brand Ta thấy rằng top 3 hãng mang lại doanh thu cao nhất lần lượt là AMD9 , intel9 , intel7 , 4.49tr$ , 4.47tr$ và 3.47tr$ chiếm ~17.5% , 17.4% và 13.5% , mặc dù về sản lượng bán AMD9 đứng cuối cùng còn intel9 thì đứng thứ 5*
  
""")
 
st.write("========================================================================================")


# # vẽ biểu đồ cột tổng doanh thu theo Storage
ve_bieu_do_cot_tong_doanh_thu("Storage","biểu đồ tổng doanh thu của công ty theo Storage")


# # vẽ biểu đồ trong thể hiện phần trăm tổng doanh số theo Storage 
ve_bieu_do_phan_tram_tong_doanh_so("Storage","Biểu đồ phần trăm tổng doanh thu theo Storage")

st.markdown("""

### 📊 Tổng doanh số bán máy tính theo storage
 - *ta có thể thấy rằng doanh số mà các ổ cứng SSD mang lại khá khá cân bằng nhau tuy nhiên chúng ta có thể thấy rằng HHD đang không được ưa chuộng cả về sản lượng lẫn giá thành , doanh số mà HHD mang lại rất thấp chỉ chiếm có ~17% trong khi các SSD thì đều trên 20%*
   
""")

st.write("========================================================================================")


# # vẽ biểu đồ cột tổng doanh thu theo months
ve_bieu_do_cot_tong_doanh_thu("months","biểu đồ tổng doanh thu của công ty theo months")


# # vẽ biểu đồ tròn thể hiện phần trăm tổng doanh số theo months 
ve_bieu_do_phan_tram_tong_doanh_so("months","Biểu đồ phần trăm tổng doanh thu theo months")

st.markdown("""
### 🧠 ***Kết Luận***
 - *Ta thấy rằng về xu hướng thì khách hàng vẫn có xu hướng thích những máy tính có cấu hình thấp và giá thành rẻ nhưng trên thực tế doanh số là lợi nhuận của công ty đến chủ yếu từ những sản phẩm chất lượng có giá thành từ tầm trung đến cao*
 - *==> nên tập trung quảng cáo những sản phẩm chất lượng cao , giá thành cao vì đây là những sản phẩm mang lại doanh thu và lợi nhuận cao cho tông ty nhưng lại không được khách hàng tin dùng và mua nhiều vd như hãng MSI razer,.., không cần tập trung quảng quá quá nhiều về những sản phẩm phổ thông như hãng Apple, processer intel 3 tại vì nó đã quá phổ biến và nổi tiếng *

""")


# data.head()
st.write("========================================================================================")


# # vẽ biểu đồ cột với giá trị là tổng doanh thu của năm nay so sánh với cùng kì năm ngoái theo Brand
danh_sach_ten_cot = ['Brand','Price ($)','LY price']
ds_gia_tri_ve_theo_cot = ['Price ($)','LY price']
ds_df_tr_ve = ve_nhieu_bieu_do_cot(danh_sach_ten_cot,"Tổng doanh thu theo brand của năm nay và cùng kì năm ngoái",'Brand',ds_gia_tri_ve_theo_cot)
print(ds_df_tr_ve[0])


# # vẽ biểu đồ đường thẻ hiện độ tăng trưởng của tổng doanh thu theo Brand
a = ve_bieu_do_duong(danh_sach_ten_cot,"Brand","Biểu đồ đường thể hiện tổng doanh thu theo Brand của năm nay và so với cùng kì năm ngoái\n","%")
st.markdown("""
### 📊 Tổng doanh số bán máy tính theo storage
 - *Ta thấy doanh sô tăng trưởng cao nhất là Acer 5.52% điều này xảy ra là vì những năm gần đây các sản phẩm đến từ đài loan nơi có trụ sở của công ty chip hàng đầu NVIDIA đặt tại đó sản xuất chip vô cùng phổ biến vì giá thành hợp lý , chip hoạt động tốt phù hợp với lứa sinh viên , học sinh*
 - *Tăng trưởng thấp nhất thuộc về Apple 3.5% vì cơ bản sản phẩm này đã uy tín và bán được nhiều hàng từ rất lâu về trước vậy nên việc tăng trưởng thấp là dễ hiểu , apple tập trung vào việc dữ ổn định tập khách hàng hơn là giới thiệu khác hàng mới*
 
""")

  
st.write("========================================================================================")


# # vẽ biểu đồ cột với giá trị là tổng doanh thu của năm nay so sánh với cùng kì năm ngoái theo Processor
danh_sach_ten_cot = ['Processor','Price ($)','LY price']
ds_gia_tri_ve_theo_cot = ['Price ($)','LY price']
ds_df_tr_ve = ve_nhieu_bieu_do_cot(danh_sach_ten_cot,"ổng doanh thu theo Processor của năm nay và cùng kì năm ngoái",'Processor',ds_gia_tri_ve_theo_cot)
print(ds_df_tr_ve[0])


# # vẽ biểu đồ đường thẻ hiện độ tăng trưởng của tổng doanh thu theo Processor
ve_bieu_do_duong(danh_sach_ten_cot,'Processor',"Biểu đồ đường thể hiện tổng doanh thu theo Processor của năm nay và so với cùng kì năm ngoái\n",'%')
st.write("========================================================================================")


# # vẽ biểu đồ cột với giá trị là tổng doanh thu của năm nay so sánh với cùng kì năm ngoái theo Storage
danh_sach_ten_cot = ['Storage','Price ($)','LY price']
ds_gia_tri_ve_theo_cot = ['Price ($)','LY price']
ds_df_tr_ve = ve_nhieu_bieu_do_cot(danh_sach_ten_cot,"ổng doanh thu theo Storage của năm nay và cùng kì năm ngoái",'Storage',ds_gia_tri_ve_theo_cot)
print(ds_df_tr_ve[0])


# # vẽ biểu đồ đường thẻ hiện độ tăng trưởng của tổng doanh thu theo Storage
ve_bieu_do_duong(danh_sach_ten_cot,'Storage',"Biểu đồ đường thể hiện tổng doanh thu theo Storage của năm nay và so với cùng kì năm ngoái\n",'%')
st.write("========================================================================================")


# # vẽ biểu đồ cột với giá trị là tổng doanh thu của năm nay so sánh với cùng kì năm ngoái theo months
danh_sach_ten_cot = ['months','Price ($)','LY price']
ds_gia_tri_ve_theo_cot = ['Price ($)','LY price']
ve_nhieu_bieu_do_cot(danh_sach_ten_cot,"Biểu đồ tổng doanh số theo tháng của năm nay và cùng kì năm ngoái","months",ds_gia_tri_ve_theo_cot)


# # vẽ biểu đồ đường thẻ hiện độ tăng trưởng của tổng doanh thu theo months
ve_bieu_do_duong(danh_sach_ten_cot,"months","Biểu đồ đường thể hiện tổng doanh thu theo months của năm nay và so với cùng kì năm ngoái\n",'%')
st.write("========================================================================================")


# data.head()


# ten_cot = ["RAM (GB)",'Price ($)']
# ve_bieu_do_duong(ten_cot,'RAM (GB)','Mối liên hệ dữa RAM (GB) và giá của máy tính\n','1')


# data.head()


# # vẽ biểu đồ boxplot để so sánh khoảng giá máy tính theo brand
ten_cot = ['Brand','Price ($)']
ve_bieu_do_box_plot(ten_cot,'Biểu đồ so sánh khoảng giá máy tính của các hãng\n','Brand')
st.write("========================================================================================")


# # vẽ biểu đồ violin thể hiện sự phân bố của giá và khoảng giá theo từng Brand
ten_cot = ['Brand','Price ($)']
ve_bieu_do_violin_plot(ten_cot,'Biểu đồ KDE vầ boxplot theo từng Brand\n','Brand')
st.markdown("""
### 📊 Phân tích biểu đồ phân phối giá của máy tính theo Brand
 - *Từ biểu đồ Boxplot và biểu đồ violin ta thấy rằng đa phần dữ liệu về giá của các brand đều bị lệch xuống dưới cho thấy dữ liệu có độ phân tán mạnh tập trung chủ yếu ở những khoảng giá thấp*
 
""")


# #   
st.write("========================================================================================")


# # vẽ biểu đồ boxplot để so sánh khoảng giá máy tính theo Operating System	
ten_cot = ['Operating System','Price ($)']
ve_bieu_do_box_plot(ten_cot,'Biểu đồ so sánh khoảng giá máy tính của các Operating System\n','Operating System')


# # vẽ biểu đồ violin thể hiện sự phân bố của giá và khoảng giá theo từng Operating System
ten_cot = ['Operating System','Price ($)']
ve_bieu_do_violin_plot(ten_cot,'Biểu đồ KDE vầ boxplot theo từng Operating System\n','Operating System')
st.write("========================================================================================")


# # vẽ biểu đồ boxplot để so sánh khoảng giá máy tính theo Processor
ten_cot = ['Processor','Price ($)']
ve_bieu_do_box_plot(ten_cot,'Biểu đồ so sánh khoảng giá máy tính của các Processor\n','Processor')


# # vẽ biểu đồ violin thể hiện sự phân bố của giá và khoảng giá theo từng Processor
ten_cot = ['Processor','Price ($)']
ve_bieu_do_violin_plot(ten_cot,'Biểu đồ KDE vầ boxplot theo từng Processor\n','Processor')
st.write("========================================================================================")


# data.head()


# # giá trị trung bình của máy tính theo Brand
ten_cot = ['Brand','Price ($)']
ve_bieu_do_poinplot(ten_cot,'Giá trị trung bình và khoảng tin cậy theo từng Brand\n',hue='Brand')
st.write("========================================================================================")


# # giá trị trung bình của máy tính theo Processor
ten_cot = ['Processor','Price ($)']
ve_bieu_do_poinplot(ten_cot,'Giá trị trung bình và khoảng tin cậy theo từng Processor\n',hue='Processor')
st.write("========================================================================================")


# # giá trị trung bình của máy tính theo Storage
ten_cot = ['Storage','Price ($)']
ve_bieu_do_poinplot(ten_cot,'Giá trị trung bình và khoảng tin cậy theo từng Storage\n',hue='Storage')
st.write("========================================================================================")


# # giá trị trung bình của máy tính theo GPU
ten_cot = ['GPU','Price ($)']
ve_bieu_do_poinplot(ten_cot,'Giá trị trung bình và khoảng tin cậy theo từng GPU\n',hue='GPU')
st.write("========================================================================================")


# # giá trị trung bình của máy tính theo Operating System
ten_cot = ['Operating System','Price ($)']
ve_bieu_do_poinplot(ten_cot,'Giá trị trung bình và khoảng tin cậy theo từng Operating System\n',hue='Operating System')
st.write("========================================================================================")


# # Tổng số bán máy tính của brand theo processer
# data.head()
plt.figure(figsize=(20,5))
sns.countplot(x='Brand',data=data,hue='Processor')
plt.title("Tổng số bán máy tính của Brand theo Processor\n")
st.pyplot(plt)

# # Lấy ra xem mỗi brand thì có bao nhiêu processer
ten_hang = data['Brand'].value_counts().index.to_list()
df_brand_processoe = data.groupby("Brand")['Processor'].value_counts().reset_index()
total_processer_brand = {}
for i in range(len(ten_hang)):
    total_processer_brand[ten_hang[i]] = len(df_brand_processoe[df_brand_processoe['Brand']==ten_hang[i]])
st.write(total_processer_brand)
st.write("========================================================================================")


# # sử dụng pivot để lấy ra từng hãng có bao nhiêu processer mỗi loại
df_brand_processoe_wide_forrmat = df_brand_processoe.pivot(index="Processor",columns="Brand",values="count")
df_brand_processoe_wide_forrmat = df_brand_processoe_wide_forrmat.reset_index()
# df_brand_processoe_wide_forrmat


# # vẽ biểu đồ thể hiện tổng số lượng bán của brand theo từng loại processer
fig,ax = plt.subplots(ncols=5,nrows=2,figsize=(22,10))
index=0
for i in range(2):
    for j in range(5):
        sns.barplot(x='Processor',y=ten_hang[index],data=df_brand_processoe_wide_forrmat,color=color_list[index],ax=ax[i][j])
        ax[i][j].set_xticks(range(len(df_brand_processoe_wide_forrmat['Processor'])))
        ax[i][j].set_xticklabels(df_brand_processoe_wide_forrmat['Processor'], rotation=45,ha='right')
        ax[i][j].set_title(ten_hang[index])
        index+=1
fig.suptitle("Biểu đồ sản lượng bán computer của Brand theo từng processor\n")
st.pyplot(fig)

st.write("========================================================================================")


# data.head()


# # Tạo một list danh sách gòm các tháng trong năm
months = [
    "January", "February", "March", "April", "May", "June", 
    "July", "August", "September", "October", "November", "December"
]

# # tạo các list rỗng đê chứa  dữ liệu doanh thu từng quý của năm 2023 và 2024
tong_doanh_thu_theo_quy_2024 = []
tong_doanh_thu_theo_quy_2023 = []

# # Tính toán để đưa ra doanh số theo từng quý của năm 2024 và cùng kì năm ngoái (2023)
for i in range(0,len(months),4):
    batch = months[i:i+4]
    quy = data[data['months'].isin(batch)]
    quy_2024 = quy['Price ($)'].sum()
    quy_2023 = quy['LY price'].sum()
    tong_doanh_thu_theo_quy_2024.append(quy_2024)
    tong_doanh_thu_theo_quy_2023.append(quy_2023)

# # vẽ biểu đồ doanh số theo từng quý năm 2024
fig,ax = plt.subplots(ncols=3,nrows=1,figsize=(20,5))
bars = sns.barplot(x=['quý 1','quý 2','quý 3'],y=tong_doanh_thu_theo_quy_2024,ax=ax[0],palette=palettes[randint(0,len(palettes)-1)])
ax[0].set_title("Biểu đồ doanh số theo quý năm 2024")
ax[0].set_xlabel('Quý')
ax[0].set_ylabel('Tổng doanh số')

# # ghi số liệu cho biểu đồ năm 2024
for i in range(3):
    ax[0].bar_label(bars.containers[i], fmt="%.0f", fontsize=12, fontweight="bold", padding=3)


# # vẽ biểu đồ doanh số theo từng quý năm 2023
bar_1 = sns.barplot(x=['quý 1','quý 2','quý 3'],y=tong_doanh_thu_theo_quy_2023,ax=ax[1],palette=palettes[randint(0,len(palettes)-1)])
ax[1].set_title("Biểu đồ doanh số theo quý năm 2023")
ax[1].set_xlabel('Quý')
ax[1].set_ylabel('Tổng doanh số')

# # ghi số liệu cho năm 2023
for i in range(3):
    ax[1].bar_label(bar_1.containers[i], fmt="%.0f", fontsize=12, fontweight="bold", padding=3)

# # Tính toán phần trăm tăng trưởng của quý trong năm 2024 so với cùng kì năm ngoái (2023)
phan_trams= []
for i in range(3):
    phan_tram = ((tong_doanh_thu_theo_quy_2024[i]-tong_doanh_thu_theo_quy_2023[i])/tong_doanh_thu_theo_quy_2023[i])*100
    phan_trams.append(phan_tram)
bar_2 = sns.barplot(x=['quý 1','quý 2','quý 3'],y=phan_trams,palette=palettes[randint(0,len(palettes)-1)])
ax[2].set_xlabel("Quý")
ax[2].set_ylabel("phần trăm tăng trưởng")
ax[2].set_title("Độ tăng trưởng của quý so với cùng kì năm ngoái \n (của năm 2024 so với 2023)")

# # ghi số liệu tăng trưởng
for i in range(3):
    ax[2].bar_label(bar_2.containers[i], fontsize=12, fontweight="bold", padding=3)



fig.suptitle("Tổng doanh thu theo quý và độ tăng trưởng so với cùng kì năm  ngoái \n\n\n")
st.pyplot(fig)
