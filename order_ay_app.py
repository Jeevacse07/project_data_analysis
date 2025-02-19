import streamlit as st
import pandas as pd
import pymysql
import matplotlib.pyplot as plt

# Streamlit App Title
st.title("📊 SQL Data Viewer with Streamlit") 

# Database Connection Function
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password=dbpassword,
        database="order_data_analysis",
        cursorclass=pymysql.cursors.DictCursor
    )

# Function to Fetch Data
def fetch_data(query):
    connection = get_db_connection()
    df = None
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            data = cursor.fetchall()
            df = pd.DataFrame(data)
    finally:
        connection.close()
    return df

# Define Queries
query_dict = {
    "Top 10 Revenue Generating Products": """
        SELECT p.product_id, SUM(oi.quantity * oi.sale_price) AS total_revenue
        FROM order_details oi
        JOIN product p ON oi.product_id = p.product_id
        GROUP BY p.product_id
        ORDER BY total_revenue DESC
        LIMIT 10;
    """,
    "Top 5 Cities with Highest Profit Margins": """
        SELECT r.city, 
               ROUND(SUM(oi.profit) / SUM(oi.quantity * oi.sale_price) * 100, 2) AS profit_margin
        FROM orders o
        JOIN order_details oi ON o.order_id = oi.order_id
        JOIN location_details r ON o.location_id = r.location_id
        GROUP BY r.city
        ORDER BY profit_margin DESC
        LIMIT 5;
    """,
    "Total Discount Given for Each Category": """
        SELECT c.category_name, SUM(od.discount) AS total_discount
        FROM order_details od
        JOIN product p ON od.product_id = p.product_id
        JOIN category c ON p.category_id = c.category_id
        GROUP BY c.category_name
        ORDER BY total_discount DESC;
    """,
    "Average Sale Price per Product Category": """
        SELECT c.category_name, ROUND(AVG(sale_price), 2) AS sale_average 
        FROM order_details od
        JOIN product p ON p.product_id = od.product_id
        JOIN category c ON c.category_id = p.category_id
        GROUP BY c.category_name
        ORDER BY c.category_name ASC, sale_average DESC;
    """,
    "Region with Highest Average Sale Price": """
        SELECT l.region, ROUND(AVG(od.sale_price), 2) AS sale_average 
        FROM order_details od
        JOIN orders o ON od.order_id = o.order_id
        JOIN location_details l ON o.location_id = l.location_id
        GROUP BY l.region
        ORDER BY sale_average DESC
        LIMIT 1;
    """,
    "Total Profit Per Category": """
        SELECT c.category_name, SUM(od.profit) AS total_profit
        FROM order_details od
        JOIN product p ON od.product_id = p.product_id
        JOIN category c ON p.category_id = c.category_id
        GROUP BY c.category_name
        ORDER BY total_profit DESC;
    """,
    "Top 3 Segments with Highest Quantity of Orders": """
        SELECT o.segment, SUM(od.quantity) AS total_quantity
        FROM order_details od
        JOIN orders o ON o.order_id = od.order_id
        GROUP BY o.segment
        ORDER BY total_quantity DESC
        LIMIT 3;
    """,
    "Average Discount Percentage per Region": """
        SELECT r.region, ROUND(AVG(oi.discount), 2) AS discount_average_region
        FROM orders o
        JOIN order_details oi ON o.order_id = oi.order_id
        JOIN location_details r ON o.location_id = r.location_id
        GROUP BY r.region
        ORDER BY discount_average_region DESC
        LIMIT 5;
    """,
    "Product Category with Highest Total Profit": """
        SELECT c.category_name, SUM(od.profit) AS total_profit
        FROM order_details od
        JOIN product p ON od.product_id = p.product_id
        JOIN category c ON p.category_id = c.category_id
        GROUP BY c.category_name
        ORDER BY total_profit DESC
        LIMIT 1;
    """,
    "Total Revenue Generated Per Year": """
        SELECT YEAR(o.order_date) AS order_year, 
               ROUND(SUM(od.sale_price * od.quantity), 2) AS total_revenue
        FROM order_details od
        JOIN orders o ON od.order_id = o.order_id
        GROUP BY order_year
        ORDER BY order_year ASC;
    """
}

# Visualization
st.sidebar.header("Select a Query")
selected_query = st.sidebar.selectbox("Choose a Query", list(query_dict.keys()))

if selected_query:
    df = fetch_data(query_dict[selected_query])
    if not df.empty:
        st.dataframe(df)

        # Convert second column to numeric
        df[df.columns[1]] = pd.to_numeric(df[df.columns[1]], errors='coerce')

        if selected_query == "Top 10 Revenue Generating Products":
            fig, ax = plt.subplots()
            df.set_index(df.columns[0])[df.columns[1]].plot(kind='bar', ax=ax)
            st.pyplot(fig)

        elif selected_query == "Total Discount Given for Each Category":
            fig, ax = plt.subplots()
            df.set_index(df.columns[0])[df.columns[1]].plot(kind='barh', ax=ax)
            st.pyplot(fig)

        elif "profit_margin" in df.columns or "total_profit" in df.columns or "total_discount" in df.columns:
            fig, ax = plt.subplots()
            df.set_index(df.columns[0])[df.columns[1]].plot(kind='pie', autopct='%1.1f%%', ax=ax)
            st.pyplot(fig)

        elif "discount_average_region" in df.columns or "sale_average" in df.columns:
            fig, ax = plt.subplots()
            df.set_index(df.columns[0])[df.columns[1]].plot(kind='barh', ax=ax)
            st.pyplot(fig)

        elif "order_year" in df.columns:
            fig, ax = plt.subplots()
            df.set_index(df.columns[0])[df.columns[1]].plot(kind='line', ax=ax)
            st.pyplot(fig)
        elif selected_query == "Top 3 Segments with Highest Quantity of Orders":
            df[df.columns[1]] = pd.to_numeric(df[df.columns[1]], errors='coerce')
            fig, ax = plt.subplots()
            df.set_index(df.columns[0])[df.columns[1]].plot(kind='bar', ax=ax, color=['blue', 'green', 'red'])
            ax.set_ylabel("Total Orders")
            ax.set_title("Top 3 Segments with Highest Quantity of Orders")
            st.pyplot(fig)
        else:
            st.write("No suitable visualization found.")

