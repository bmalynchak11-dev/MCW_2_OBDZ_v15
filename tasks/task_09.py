def query() -> str:
    return """
    WITH cust_category_revenue AS (
        SELECT 
            cat.id AS category_id,
            cat.name AS category,
            c.id AS customer_id,
            c.full_name AS customer,
            SUM(p.quantity * pr.price) AS revenue
        FROM purchase p
        JOIN product pr ON pr.id = p.product_id
        JOIN category cat ON cat.id = pr.category_id
        JOIN customer c ON c.id = p.customer_id
        GROUP BY cat.id, cat.name, c.id, c.full_name
    ),
    running_revenue AS (
        SELECT 
            category_id,
            category,
            customer_id,
            customer,
            revenue,
            SUM(revenue) OVER (PARTITION BY category_id) AS total_category_revenue,
            SUM(revenue) OVER (
                PARTITION BY category_id 
                ORDER BY revenue DESC, customer_id ASC
                ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
            ) AS cum_revenue,
            COALESCE(
                SUM(revenue) OVER (
                    PARTITION BY category_id 
                    ORDER BY revenue DESC, customer_id ASC
                    ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING
                ), 
                0
            ) AS prior_revenue
        FROM cust_category_revenue
    )
    SELECT 
        category,
        customer,
        revenue,
        ROUND((100.0 * cum_revenue / total_category_revenue), 1) AS cum_pct
    FROM running_revenue
    WHERE (100.0 * prior_revenue / total_category_revenue) < 80.0
    ORDER BY category_id, revenue DESC, customer_id ASC;
    """