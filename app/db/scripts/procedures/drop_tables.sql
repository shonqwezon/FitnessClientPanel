CREATE OR REPLACE PROCEDURE app.drop_tables()
SECURITY DEFINER
AS $$
DECLARE
    table_record RECORD;
BEGIN
    FOR table_record IN
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public'
    LOOP
        CALL drop_table(table_record.tablename, FALSE);
    END LOOP;

    RAISE NOTICE 'All tables have been dropped.';
END;
$$ LANGUAGE plpgsql;
