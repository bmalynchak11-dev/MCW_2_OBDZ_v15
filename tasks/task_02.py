def query() -> str:
    return """
    WITH purchase_stats AS (
        SELECT 
            p.id,
            pr.title,
            (p.quantity * pr.price) AS amount,
            AVG(p.quantity * pr.price) OVER (PARTITION BY pr.id) AS raw_avg
        FROM purchase p
        JOIN product pr ON pr.id = p.product_id
    )
    SELECT 
        id,
        title,
        amount,
        ROUND(raw_avg, 2) AS avg_amount
    FROM purchase_stats
    WHERE amount > raw_avg
    ORDER BY id;
    """