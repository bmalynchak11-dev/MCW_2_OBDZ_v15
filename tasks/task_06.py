def statement() -> str:
    return """
    WITH deleted_purchases AS (
        DELETE FROM purchase
        WHERE shipped_on IS NOT NULL 
          AND ordered_on < DATE '2024-07-01'
        RETURNING id, customer_id, product_id, quantity, ordered_on, shipped_on
    ),
    inserted_archive AS (
        INSERT INTO purchase_archive (id, customer_id, product_id, quantity, ordered_on, shipped_on)
        SELECT id, customer_id, product_id, quantity, ordered_on, shipped_on
        FROM deleted_purchases
        RETURNING id
    )
    INSERT INTO archive_log (moved)
    SELECT COUNT(*) FROM inserted_archive;
    """