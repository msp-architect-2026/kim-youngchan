"""
Common database queries for order service
All queries use parameterized statements to prevent SQL injection
"""

# ============= Order Queries =============

INSERT_ORDER = """
    INSERT INTO orders 
    (user_id, sneaker_id, size, status, reserve_token, created_at)
    VALUES (%s, %s, %s, %s, %s, %s)
"""

GET_ORDER_BY_ID = """
    SELECT id, user_id, sneaker_id, size, status, reserve_token, created_at, updated_at
    FROM orders
    WHERE id = %s
"""

GET_ORDER_BY_TOKEN = """
    SELECT id, user_id, sneaker_id, size, status, reserve_token, created_at, updated_at
    FROM orders
    WHERE reserve_token = %s
"""

GET_ORDERS_BY_USER = """
    SELECT id, user_id, sneaker_id, size, status, reserve_token, created_at, updated_at
    FROM orders
    WHERE user_id = %s
    ORDER BY created_at DESC
    LIMIT %s OFFSET %s
"""

COUNT_ORDERS_BY_USER = """
    SELECT COUNT(*) as total
    FROM orders
    WHERE user_id = %s
"""

UPDATE_ORDER_STATUS = """
    UPDATE orders
    SET status = %s, updated_at = %s
    WHERE id = %s
"""

# ============= Admin Queries =============

GET_ALL_ORDERS = """
    SELECT id, user_id, sneaker_id, size, status, reserve_token, created_at, updated_at
    FROM orders
    ORDER BY created_at DESC
    LIMIT %s OFFSET %s
"""

COUNT_ALL_ORDERS = """
    SELECT COUNT(*) as total
    FROM orders
"""

COUNT_ORDERS_BY_STATUS = """
    SELECT status, COUNT(*) as count
    FROM orders
    GROUP BY status
"""

GET_RESERVED_ORDERS = """
    SELECT id, user_id, sneaker_id, size, status, reserve_token, created_at, updated_at
    FROM orders
    WHERE status = 'RESERVED'
    AND created_at < DATE_SUB(NOW(), INTERVAL %s SECOND)
"""

# ============= Consistency Check Queries =============

GET_EXPIRED_RESERVATIONS = """
    SELECT id, user_id, sneaker_id, size, reserve_token, created_at
    FROM orders
    WHERE status = 'RESERVED'
    AND created_at < DATE_SUB(NOW(), INTERVAL %s SECOND)
    LIMIT %s
"""

CANCEL_EXPIRED_RESERVATION = """
    UPDATE orders
    SET status = 'CANCELLED', updated_at = NOW()
    WHERE id = %s AND status = 'RESERVED'
"""