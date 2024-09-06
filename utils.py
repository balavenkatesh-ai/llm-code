ALTER TABLE schema_name.tip_inventory
ADD COLUMN wi_id INTEGER,
ADD COLUMN pr_ids INTEGER[], -- Assuming you're using PostgreSQL for ARRAY type
ADD COLUMN status VARCHAR(20) DEFAULT 'OPEN';