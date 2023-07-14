-- 4. Buy buy buy
-- script that creates a trigger that decr the qty of an item after adding a new order
CREATE TRIGGER decr_count BEFORE INSERT ON orders
FOR EACH ROW UPDATE items
SET quantity = quantity - NEW.number
WHERE name = NEW.item_name;
