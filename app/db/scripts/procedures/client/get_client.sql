CREATE OR REPLACE FUNCTION app.get_client(in_fullname VARCHAR(50) DEFAULT NULL)
RETURNS TABLE (id INTEGER,
                fullname VARCHAR(50),
                balance NUMERIC(8, 2),
                reg_date TIMESTAMP)
SECURITY DEFINER
AS $$
BEGIN
    RETURN QUERY SELECT c.id, c.fullname, c.balance, c.reg_date
        FROM client AS c
        WHERE (in_fullname IS NULL OR in_fullname = c.fullname);

    IF (in_fullname IS NOT NULL) AND (NOT FOUND) THEN
        RAISE EXCEPTION 'Client "%" does not exist', in_fullname;
    END IF;
END;
$$ LANGUAGE plpgsql;
