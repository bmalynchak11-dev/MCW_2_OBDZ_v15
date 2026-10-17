def query() -> str:
    return """
    WITH ref_counts AS (
        SELECT referred_by AS customer_id, COUNT(*) AS referrals
        FROM customer
        WHERE referred_by IS NOT NULL
        GROUP BY referred_by
    ),
    purch_stats AS (
        SELECT 
            customer_id,
            COUNT(*) AS purchases,
            COALESCE(SUM(quantity), 0) AS items
        FROM purchase
        GROUP BY customer_id
    )
    SELECT 
        c.id,
        c.full_name,
        COALESCE(r.referrals, 0) AS referrals,
        COALESCE(p.purchases, 0) AS purchases,
        COALESCE(p.items, 0) AS items
    FROM customer c
    LEFT JOIN ref_counts r ON r.customer_id = c.id
    LEFT JOIN purch_stats p ON p.customer_id = c.id
    ORDER BY c.id;
    """