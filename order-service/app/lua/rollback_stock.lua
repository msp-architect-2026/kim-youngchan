-- Rollback reserved stock
-- KEYS[1]: stock:{sneaker_id}:{size}
-- ARGV[1]: quantity to restore (always 1)

local stock_key = KEYS[1]
local quantity = tonumber(ARGV[1])

redis.call('INCRBY', stock_key, quantity)
return 1