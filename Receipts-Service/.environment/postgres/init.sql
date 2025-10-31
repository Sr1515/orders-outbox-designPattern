CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS receipts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id INTEGER,
    order_id UUID,
    username TEXT,
    ammount NUMERIC(10, 2),
    items JSONB
);

