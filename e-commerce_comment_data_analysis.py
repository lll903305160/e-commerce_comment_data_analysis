# 导入原始数据data1
import pandas as pd
import json
import ast
data1 = pd.read_excel(r'd:\My Documents\Desktop\comments_评价表.xlsx')
data1.info() 

# 计算好评率
df1 = pd.pivot_table(data1,index ="shop",columns='textPolarity',values='评价内容',aggfunc='count',fill_value=0)
df1_favorable_rate = df1.div(df1.sum(axis=1),axis=0)  
df1_favorable_rate = df1_favorable_rate.reset_index()

# 观点拆分堆叠后得到数据data2
data2 = data1
data2['aspectItem'] = data2['aspectItem'].apply(ast.literal_eval)
data2 = data2.explode('aspectItem') 
data2 = pd.concat([data2.drop(['aspectItem'], axis=1), data2['aspectItem'].apply(pd.Series)], axis=1).reset_index(drop=True)
print(data2.head(1))


# 观点好评率
df2 = pd.pivot_table(data2,index ="shop",columns='aspectPolarity',values='评价内容',aggfunc='count',fill_value=0)
df2_view_rate = df2.div(df2.sum(axis=1),axis=0)
df2_view_rate = df2_view_rate.reset_index()
df2_view_rate

# 按观点类别分组数据
df3 = pd.pivot_table(data2,index=["shop","aspectCategory"],columns='aspectPolarity',values='评价内容',aggfunc='count',fill_value=0)
df3["sum"]=df3[["中","正","负"]].sum(axis=1)
df3.reset_index(inplace=True)
df3

# 输出excel
result = pd.ExcelWriter(r'd:\My Documents\Desktop\result.xlsx')
df1_favorable_rate.to_excel(result,sheet_name='favorable_rate',index=False)
df2_view_rate.to_excel(result,sheet_name='view_rate',index=False)
df3.to_excel(result,sheet_name='rate',index=False)
result.save()
