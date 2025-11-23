import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="Retail Dashboard", layout="wide")

st.title("📊 Retail Store Analytics")
st.markdown("This dashboard connects to the **Retail Inventory System** to visualize stock data.")
st.markdown("---")

def load_data():
    conn = sqlite3.connect("store_data.db")
    df = pd.read_sql_query("SELECT * FROM inventory", conn)
    conn.close()
    return df

try:
    data = load_data()
except:
    st.error("Database not found! Please run the 'manager_gui.py' file first to create the database.")
    st.stop()

if data.empty:
    st.info("No data available. Please add some items using the Desktop App.")
else:
    col1, col2, col3 = st.columns(3)
    
    total_items = data['quantity'].sum()
    total_value = (data['price'] * data['quantity']).sum()
    unique_categories = data['category'].nunique()

    col1.metric("Total Stock Count", f"{total_items} Units")
    col2.metric("Total Inventory Value", f"₹ {total_value:,.2f}")
    col3.metric("Active Categories", unique_categories)

    st.markdown("---")

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Stock Value by Category")
        category_group = data.groupby("category")["quantity"].sum().reset_index()
        
        fig = px.pie(category_group, values='quantity', names='category', 
                     title='Quantity Distribution', hole=0.4)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Price vs Quantity Analysis")
        fig2 = px.scatter(data, x="price", y="quantity", color="category", 
                          size="quantity", title="Product Price vs. Stock Level")
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Recent Entries")
    st.dataframe(data.tail(10))
    if st.button("Reload Data"):
        st.rerun()