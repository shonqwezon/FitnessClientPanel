CREATE OR REPLACE FUNCTION get_manager_table()
RETURNS TABLE (fullname VARCHAR(50), assign_date TIMESTAMP, email VARCHAR(50)) AS
$$
BEGIN
    RETURN QUERY SELECT m.fullname, m.assign_date, m.email FROM manager AS m;
END;
$$ LANGUAGE plpgsql;
