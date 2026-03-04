-- Reserve stock atomically
-- KEYS[1]: stock:{sneaker_id}:{size}
-- ARGV[1]: quantity to reserve (always 1)

local stock_key = KEYS[1]
local quantity = tonumber(ARGV[1])

local current_stock = tonumber(redis.call('GET', stock_key) or 0)

if current_stock >= quantity then
    redis.call('DECRBY', stock_key, quantity)
    return 1
else
    return 0
end