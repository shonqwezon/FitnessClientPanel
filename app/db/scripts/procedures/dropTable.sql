CREATE OR REPLACE PROCEDURE drop_table(table_name TEXT)
AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM information_schema.tables
        WHERE table_schema = 'public' AND table_name = table_name
    ) THEN
        EXECUTE FORMAT('DROP TABLE %I', table_name);
        RAISE NOTICE 'Table "%" has been dropped.', table_name;
    ELSE
        RAISE NOTICE 'Table "%" does not exist.', table_name;
    END IF;
END;
$$ LANGUAGE plpgsql;
