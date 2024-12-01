CREATE OR REPLACE PROCEDURE drop_table(table_name TEXT)
AS $$
BEGIN
    EXECUTE FORMAT('DROP TABLE IF EXISTS public.%I CASCADE', table_name);
    RAISE NOTICE 'Table % has been dropped successfully.', table_name;
END;
$$ LANGUAGE plpgsql;
