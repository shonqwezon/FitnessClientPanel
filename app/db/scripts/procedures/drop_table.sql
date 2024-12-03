CREATE OR REPLACE PROCEDURE app.drop_table(table_name TEXT, explicity BOOLEAN DEFAULT TRUE)
SECURITY DEFINER
AS $$
BEGIN
    IF explicity THEN
        EXECUTE FORMAT('DELETE FROM public.%I', table_name);
    END IF;
    EXECUTE FORMAT('DROP TABLE IF EXISTS public.%I CASCADE', table_name);
    RAISE NOTICE 'Table % has been dropped successfully.', table_name;
END;
$$ LANGUAGE plpgsql;
