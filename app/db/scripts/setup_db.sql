CREATE SCHEMA IF NOT EXISTS app;
CREATE USER {user} WITH PASSWORD '{password}';
REVOKE ALL ON SCHEMA public FROM {user};
ALTER USER {user} SET search_path TO app, public;
GRANT USAGE ON SCHEMA app TO {user};
