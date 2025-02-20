import streamlit as st
import pandas as pd
import pymysql
import matplotlib.pyplot as plt
import seaborn as sns

# Streamlit App Title
st.title("📊 SQL Data Viewer with Streamlit") 

# Database Connection Function
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="dbpasswd",
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
    """,
    "Profitability of Different Shipping Modes": """
        SELECT o.ship_mode, COUNT(o.order_id) AS total_orders,
               SUM(od.sale_price) AS total_sales,
               SUM(od.profit) AS total_profit,
               ROUND(SUM(od.profit) / SUM(od.sale_price) * 100, 2) AS profit_margin_percentage
        FROM orders o
        JOIN order_details od ON o.order_id = od.order_id
        GROUP BY o.ship_mode
        ORDER BY total_profit DESC;
    """,
    "Top 10 Most Profitable Products": """
        SELECT p.product_id, SUM(od.profit) AS total_profit
        FROM order_details od
        JOIN product p ON od.product_id = p.product_id
        GROUP BY p.product_id
        ORDER BY total_profit DESC
        LIMIT 10;
    """,
    "Category-Wise Revenue and Profit Trends": """
        SELECT c.category_name, SUM(od.sale_price * od.quantity) AS total_revenue, 
               SUM(od.profit) AS total_profit
        FROM order_details od
        JOIN orders o ON od.order_id = o.order_id
        JOIN product p ON od.product_id = p.product_id
        JOIN category c ON p.category_id = c.category_id
        GROUP BY c.category_name
        ORDER BY total_revenue DESC;
    """,
    "Identify the Top 3 Loss-Making Products in Each Category": """
        WITH RankedProducts AS (
            SELECT c.category_name, p.product_id, SUM(od.profit) AS total_loss,
                   RANK() OVER (PARTITION BY c.category_name ORDER BY SUM(od.profit) ASC) AS rnk
            FROM order_details od
            JOIN product p ON od.product_id = p.product_id
            JOIN category c ON p.category_id = c.category_id
            GROUP BY c.category_name, p.product_id
            HAVING SUM(od.profit) < 0
        )
        SELECT category_name, product_id, total_loss
        FROM RankedProducts
        WHERE rnk <= 3
        ORDER BY category_name, rnk;
    """,
    "Month with Highest Sales in Each Year": """
        SELECT YEAR(o.order_date) AS year, MONTH(o.order_date) AS month, SUM(od.quantity) AS total_sales
        FROM order_details od
        JOIN orders o ON od.order_id = o.order_id
        GROUP BY year, month
        ORDER BY year DESC, total_sales DESC;
    """,
    "Product Subcategory with the Most Profit (Top 10)": """
        SELECT s.sub_category_name, SUM(od.profit) AS total_profit
        FROM order_details od
        JOIN product p ON od.product_id = p.product_id
        JOIN subcategory s ON p.sub_category_id = s.sub_category_id
        GROUP BY s.sub_category_name
        ORDER BY total_profit DESC
        LIMIT 10;
    """,
    "Impact of Shipping Mode on Order Volume and Profitability": """
        SELECT o.ship_mode, COUNT(o.order_id) AS order_count, SUM(od.profit) AS total_profit
        FROM orders o
        JOIN order_details od ON o.order_id = od.order_id
        GROUP BY o.ship_mode
        ORDER BY order_count DESC;
    """,
    "Top 3 Most Profitable States in Each Region": """
        WITH RankedStates AS (
            SELECT l.region, l.state, SUM(od.profit) AS total_profit,
                   RANK() OVER (PARTITION BY l.region ORDER BY SUM(od.profit) DESC) AS rnk
            FROM orders o
            JOIN location_details l ON o.location_id = l.location_id
            JOIN order_details od ON o.order_id = od.order_id
            GROUP BY l.region, l.state
        )
        SELECT region, state, total_profit
        FROM RankedStates
        WHERE rnk <= 3
        ORDER BY region, rnk;
    """,
    "Customer Segments with the Highest Order Value": """
        SELECT o.segment, ROUND(AVG(od.sale_price * od.quantity), 2) AS avg_order_value
        FROM orders o
        JOIN order_details od ON o.order_id = od.order_id
        GROUP BY o.segment
        ORDER BY avg_order_value DESC;
    """,
    "Subcategories with the Most Discounted Sales (Top 10)": """
        SELECT s.sub_category_name, SUM(od.discount) AS total_discount
        FROM order_details od
        JOIN product p ON od.product_id = p.product_id
        JOIN subcategory s ON p.sub_category_id = s.sub_category_id
        GROUP BY s.sub_category_name
        ORDER BY total_discount DESC
        LIMIT 10;
    """,
    "State-Wise Profitability Analysis (Top 5)": """
        SELECT l.state, SUM(od.profit) AS total_profit
        FROM orders o
        JOIN location_details l ON o.location_id = l.location_id
        JOIN order_details od ON o.order_id = od.order_id
        GROUP BY l.state
        ORDER BY total_profit DESC
        LIMIT 5;
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

        elif selected_query == "Customer Segments with the Highest Order Value":
            fig, ax = plt.subplots()
            df.set_index(df.columns[0])[df.columns[1]].plot(kind='bar', ax=ax, color=['blue', 'green', 'red'])
            ax.set_ylabel("Average Order Value")
            ax.set_title("Customer Segments with the Highest Order Value")
            st.pyplot(fig)
        
            fig, ax = plt.subplots(figsize=(10, 5))
            
        elif selected_query == "Top 3 Most Profitable States in Each Region":
           # Sort states by total profit
            df = df.sort_values(by=["total_profit"], ascending=False)

            # Set Seaborn style
            sns.set_theme(style="whitegrid")

            # Create figure with subplots
            fig, ax1 = plt.subplots(figsize=(10, 6))

            # Bar chart
            sns.barplot(data=df, x="state", y="total_profit", ax=ax1, color="skyblue", alpha=0.7)

            # Line plot (overlayed)
            ax2 = ax1.twinx()
            sns.lineplot(data=df, x="state", y="total_profit", marker="o", linewidth=2.5, color="tab:red", ax=ax2)

            # Labels and Titles
            ax1.set_xlabel("State")
            ax1.set_ylabel("Total Profit (Bar Chart)", color="tab:blue")
            ax2.set_ylabel("Total Profit (Line Chart)", color="tab:red")
            plt.title("Profit Trends of Top Profitable States", fontsize=16, fontweight='bold')
            plt.xticks(rotation=45, fontsize=10)
            ax1.grid(True, linestyle="--", alpha=0.7)

            # Display plot in Streamlit
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

        elif selected_query == "Identify the Top 3 Loss-Making Products in Each Category":
            df[df.columns[2]] = pd.to_numeric(df[df.columns[2]], errors='coerce')
            fig, ax = plt.subplots(figsize=(10, 5))
            df.set_index(df.columns[0])[df.columns[2]].plot(kind='barh', ax=ax, color='red')
            ax.set_xlabel("Total Loss")
            ax.set_ylabel("Product ID")
            ax.set_title("Top 3 Loss-Making Products in Each Category")
            st.pyplot(fig)

        elif selected_query == "Month with Highest Sales in Each Year":
            fig, ax = plt.subplots(figsize=(10, 5))
            df[df.columns[1]] = pd.to_datetime(df[df.columns[1]].astype(str), format='%m', errors='coerce').dt.strftime('%b')
            df.rename(columns={df.columns[0]: "Year", df.columns[1]: "Month", df.columns[2]: "Total Sales"}, inplace=True)
            df["Total Sales"] = pd.to_numeric(df["Total Sales"], errors='coerce')

            # Pivot the DataFrame to have months as columns and years as rows
            df_pivot = df.pivot(index="Year", columns="Month", values="Total Sales")

            df_pivot.T.plot(kind='line', marker="o", ax=ax)

            ax.set_xlabel("Month")
            ax.set_ylabel("Total Sales")
            ax.set_title("Month with Highest Sales in Each Year")
            ax.legend(title="Year") 
            st.pyplot(fig)

        else:
            st.write("No suitable visualization found.")


