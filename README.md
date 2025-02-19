# Order Data Analysis

This project uses **Streamlit** to showcase **15 SQL queries** for analyzing order data. The queries help in identifying key business insights such as revenue-generating products, profit margins, discounts, and regional sales trends.

## Database Used: `order_data_analysis`

### 1. Top 10 Revenue-Generating Products
```sql
SELECT p.product_id, SUM(oi.quantity * oi.sale_price) AS total_revenue
FROM order_details oi
JOIN product p ON oi.product_id = p.product_id
GROUP BY p.product_id
ORDER BY total_revenue DESC
LIMIT 10;
```

### 2. Top 5 Cities with the Highest Profit Margins
```sql
SELECT r.city,
       ROUND(SUM(oi.profit) / SUM(oi.quantity * oi.sale_price) * 100, 2) AS profit_margin
FROM orders o
JOIN order_details oi ON o.order_id = oi.order_id
JOIN location_details r ON o.location_id = r.location_id
GROUP BY r.city
ORDER BY profit_margin DESC
LIMIT 5;
```

### 3. Total Discount Given per Category
```sql
SELECT
    c.category_name,
    SUM(od.discount) AS total_discount
FROM order_details od
JOIN product p ON od.product_id = p.product_id
JOIN category c ON p.category_id = c.category_id
GROUP BY c.category_name
ORDER BY total_discount DESC;
```

### 4. Average Sale Price per Product Category
```sql
SELECT c.category_name, ROUND(AVG(sale_price), 2) AS sale_average
FROM order_details od
JOIN product p ON p.product_id = od.product_id
JOIN category c ON c.category_id = p.category_id
GROUP BY c.category_name
ORDER BY c.category_name ASC, sale_average DESC;
```

### 5. Region with the Highest Average Sale Price
```sql
SELECT l.region, ROUND(AVG(od.sale_price), 2) AS sale_average
FROM order_details od
JOIN orders o ON od.order_id = o.order_id
JOIN location_details l ON o.location_id = l.location_id
GROUP BY l.region
ORDER BY sale_average DESC
LIMIT 1;
```

### 6. Total Profit per Category
```sql
SELECT
    c.category_name,
    SUM(od.profit) AS total_profit
FROM order_details od
JOIN product p ON od.product_id = p.product_id
JOIN category c ON p.category_id = c.category_id
GROUP BY c.category_name
ORDER BY total_profit DESC;
```

### 7. Top 3 Segments with the Highest Quantity of Orders
```sql
SELECT o.segment, SUM(od.quantity) AS total_quantity
FROM order_details od
JOIN orders o ON o.order_id = od.order_id
GROUP BY o.segment
ORDER BY total_quantity DESC
LIMIT 3;
```

### 8. Average Discount Percentage Given per Region
```sql
SELECT r.region,
       ROUND(AVG(oi.discount), 2) AS discount_average_region
FROM orders o
JOIN order_details oi ON o.order_id = oi.order_id
JOIN location_details r ON o.location_id = r.location_id
GROUP BY r.region
ORDER BY discount_average_region DESC
LIMIT 5;
```

### 9. Product Category with the Highest Total Profit
```sql
SELECT
    c.category_name,
    SUM(od.profit) AS total_profit
FROM order_details od
JOIN product p ON od.product_id = p.product_id
JOIN category c ON p.category_id = c.category_id
GROUP BY c.category_name
ORDER BY total_profit DESC
LIMIT 1;
```

### 10. Total Revenue Generated per Year
```sql
SELECT
    YEAR(o.order_date) AS order_year,
    ROUND(SUM(od.sale_price * od.quantity), 2) AS total_revenue
FROM order_details od
JOIN orders o ON od.order_id = o.order_id
GROUP BY order_year
ORDER BY order_year ASC;
```

## Usage
- Run the **Streamlit** app to visualize the results of these queries interactively.
- Modify or expand the queries to gain further insights into the dataset.

## Contributing
Feel free to suggest improvements or add more queries to enhance the analysis!

---
This README provides clear explanations and formatting for easy readability on GitHub. Let me know if you need further tweaks!

