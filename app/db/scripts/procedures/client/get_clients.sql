CREATE OR REPLACE FUNCTION app.get_clients()
RETURNS TABLE (fullname VARCHAR(50),
                balance NUMERIC(8, 2),
                reg_date TIMESTAMP)
SECURITY DEFINER
AS $$
BEGIN
    RETURN QUERY SELECT c.fullname, c.balance, c.reg_date FROM client AS c;
END;
$$ LANGUAGE plpgsql;
