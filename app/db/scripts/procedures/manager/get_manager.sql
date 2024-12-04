CREATE OR REPLACE FUNCTION app.get_manager()
RETURNS TABLE (fullname VARCHAR(50), assign_date TIMESTAMP, email VARCHAR(50))
SECURITY DEFINER
AS $$
BEGIN
    RETURN QUERY SELECT m.fullname, m.assign_date, m.email, m.sportcenter_id FROM manager AS m;
END;
$$ LANGUAGE plpgsql;
