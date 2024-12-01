CREATE OR REPLACE FUNCTION get_manager_table()
RETURNS TABLE (fullname TEXT, assign_date DATE, email TEXT) AS
$$
BEGIN
    RETURN QUERY fullname, assign_date, email FROM manager;
END;
$$ LANGUAGE plpgsql;
