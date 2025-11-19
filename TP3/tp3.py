#!/usr/bin/env python
# coding: utf-8

# 1.Load and Inspect Dataset

# In[3]:


import pandas as pd

df = pd.read_csv(r"C:\Users\LAPTA\Big-Data-TP\TP3\pizza_sales.csv")
print(df.head())
print(df.shape)
print(df.dtypes)
print(df.info())


# 2.Convert Data Types (Dates and Numbers)

# In[27]:


import pandas as pd


file_path = r"C:\Users\LAPTA\Big-Data-TP\TP3\pizza_sales.csv"


df = pd.read_csv(file_path)

numeric_cols = ["quantity", "unit_price", "total_price"]
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
df["order_time"] = pd.to_datetime(df["order_time"], format="%H:%M:%S", errors="coerce").dt.time

df["order_datetime"] = pd.to_datetime(df["order_date"].astype(str) + " " + df["order_time"].astype(str),
                                      errors="coerce")

print(df.head())
print(df.info())


# 3. Check Invalid Dates

# In[29]:


mask_bad = df['order_date'].isna()
print("عدد القيم التي لم تتغير:", mask_bad.sum())

print("\nأمثلة من order_date قبل التحويل:")
print(df.loc[mask_bad, 'order_date'].head(20))


# 4. Check Missing Dates but with Time

# In[30]:


missing_date = df['order_date'].isna().sum()

missing_date_with_time = df[df['order_date'].isna() & df['order_time'].notna()].shape[0]

print("عدد السجلات بدون تاريخ:", missing_date)
print("عدد السجلات بدون تاريخ لكن عندهم وقت:", missing_date_with_time)


# 5. Remove Rows with Missing Dates

# In[32]:


df = df.dropna(subset=['order_date'])
print("عدد السجلات بعد الحذف:", len(df))
print(df.head())


# 6. Feature Engineering

# In[ ]:


df['pizza_id'] = df['pizza_id'].astype(int)
df['order_id'] = df['order_id'].astype(int)
df['quantity'] = df['quantity'].astype(int)
df['order_time'] = pd.to_datetime(df['order_time'], format='%H:%M:%S').dt.time
df['year'] = df['order_date'].dt.year
df['month'] = df['order_date'].dt.month
df['day'] = df['order_date'].dt.day
df['weekday'] = df['order_date'].dt.day_name()
df['hour'] = df['order_datetime'].dt.hour
print(df.head())
print(df.dtypes)


# 7. Detect Outliers

# In[10]:


outliers = df[df["quantity"] > 10]
print("عدد السجلات الشاذة:", len(outliers))
outliers.head()


# 8. Check Quantity Distribution

# In[ ]:


df["quantity"].describe()


# 9. Check Duplicates

# In[ ]:


df.duplicated().sum()
df[df.duplicated()]


# 10. Check Null Values

# In[ ]:


df.isnull().sum()


# 11. Summary Statistics

# In[15]:


print(df[['quantity', 'unit_price', 'total_price']].describe())


# 12. Top 10 Pizzas Sold

# In[16]:


top_pizzas = df.groupby('pizza_name')['quantity'].sum().sort_values(ascending=False).head(10)
print(top_pizzas)

import matplotlib.pyplot as plt
top_pizzas.plot(kind='bar', color='orange', figsize=(10,5))
plt.title('Top 10 Pizzas by Quantity Sold')
plt.ylabel('Total Quantity Sold')
plt.xlabel('Pizza Name')
plt.xticks(rotation=45)
plt.show()


# 13. Sales by Category (Pie Chart)

# In[17]:


category_sales = df.groupby('pizza_category')['total_price'].sum()
print(category_sales)

category_sales.plot(kind='pie', autopct='%1.1f%%', figsize=(6,6), startangle=90)
plt.title('Sales by Pizza Category')
plt.ylabel('')
plt.show()


# 14. Sales by Pizza Size

# In[18]:


size_sales = df.groupby('pizza_size')['total_price'].sum()
print(size_sales)

size_sales.plot(kind='bar', color='green')
plt.title('Sales by Pizza Size')
plt.ylabel('Total Sales')
plt.xlabel('Pizza Size')
plt.show()


# Total Sales by Month

# In[4]:


# حساب إجمالي المبيعات لكل شهر
monthly_sales = df.groupby('month')['total_price'].sum().sort_values(ascending=False)

print(monthly_sales)

# عرض الشهر الأكثر مبيعًا
best_month = monthly_sales.idxmax()
best_month_value = monthly_sales.max()
print(f"📅 الشهر الأكثر مبيعًا هو: {best_month} بإجمالي مبيعات = ${best_month_value:.2f}")

# رسم بياني للمبيعات الشهرية
import matplotlib.pyplot as plt
plt.figure(figsize=(8,5))
monthly_sales.sort_index().plot(kind='bar', color='skyblue')
plt.title('Total Sales by Month')
plt.xlabel('Month')
plt.ylabel('Total Sales ($)')
plt.xticks(rotation=0)
plt.show()


# 15. Daily Sales Trend

# In[19]:


daily_sales = df.groupby('order_date')['total_price'].sum()
daily_sales.plot(kind='line', figsize=(12,5))
plt.title('Daily Sales Over Time')
plt.ylabel('Total Sales')
plt.xlabel('Date')
plt.show()


# 16. Hourly Sales

# In[21]:


hourly_sales = df.groupby('hour')['total_price'].sum()
print(hourly_sales)

hourly_sales.plot(kind='bar', color='skyblue', figsize=(10,5))
plt.title('Total Sales by Hour')
plt.xlabel('Hour of Day')
plt.ylabel('Total Sales ($)')
plt.xticks(rotation=0)
plt.show()


# 17. Sales by Weekday

# In[22]:


weekday_sales = df.groupby('weekday')['total_price'].sum()

days_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
weekday_sales = weekday_sales.reindex(days_order)

print(weekday_sales)

weekday_sales.plot(kind='bar', color='orange', figsize=(10,5))
plt.title('Total Sales by Weekday')
plt.xlabel('Day of Week')
plt.ylabel('Total Sales ($)')
plt.show()


# 18. Heatmap of Category vs Size

# In[23]:


category_size_sales = df.pivot_table(values='total_price', 
                                     index='pizza_category', 
                                     columns='pizza_size', 
                                     aggfunc='sum', 
                                     fill_value=0)

print(category_size_sales)

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(8,5))
sns.heatmap(category_size_sales, annot=True, fmt=".0f", cmap='YlGnBu')
plt.title('Total Sales by Pizza Category and Size')
plt.ylabel('Pizza Category')
plt.xlabel('Pizza Size')
plt.show()


# 19. Top Pizzas by Category

# In[24]:


pizza_by_category = df.groupby(['pizza_category','pizza_name'])['quantity'].sum().sort_values(ascending=False)

print(pizza_by_category.head(10))


# 20. Hourly Sales by Category (Stacked Bar)

# In[25]:


hourly_category_sales = df.pivot_table(values='total_price',
                                       index='hour',
                                       columns='pizza_category',
                                       aggfunc='sum',
                                       fill_value=0)

hourly_category_sales.plot(kind='bar', stacked=True, figsize=(12,6))
plt.title('Hourly Sales by Pizza Category')
plt.xlabel('Hour')
plt.ylabel('Total Sales ($)')
plt.show()


# In[3]:


df.to_csv('cleaned_pizza_data.csv', index=False)





