#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE TABLE orders (
    id serial PRIMARY KEY,
    order_number integer UNIQUE,
    price_dollars real,
    price_rub real,
    delivery_time date
);
EOSQL