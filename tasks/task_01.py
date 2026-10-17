def query() -> str:
    return """
    SELECT c.id, c.full_name
    FROM customer c
    JOIN purchase p ON p.customer_id = c.id
    JOIN product pr ON pr.id = p.product_id
    JOIN category cat ON cat.id = pr.category_id
    WHERE cat.name = 'Напої'

    INTERSECT

    SELECT c.id, c.full_name
    FROM customer c
    JOIN purchase p ON p.customer_id = c.id
    JOIN product pr ON pr.id = p.product_id
    JOIN category cat ON cat.id = pr.category_id
    WHERE cat.name = 'Молочні вироби'

    EXCEPT

    SELECT c.id, c.full_name
    FROM customer c
    JOIN purchase p ON p.customer_id = c.id
    JOIN product pr ON pr.id = p.product_id
    JOIN category cat ON cat.id = pr.category_id
    WHERE cat.name = 'Побутова хімія'

    ORDER BY id;
    """