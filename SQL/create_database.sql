CREATE DATABASE fastapi
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;

COMMENT ON DATABASE fastapi
    IS 'Fast API tutorial Database';