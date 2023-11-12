CREATE TABLE IF NOT EXISTS product (
    p_id VARCHAR(37),
    p_name VARCHAR(100),
    p_unitprice DECIMAL(10,2)
);
ALTER TABLE product ADD PRIMARY KEY (p_id);