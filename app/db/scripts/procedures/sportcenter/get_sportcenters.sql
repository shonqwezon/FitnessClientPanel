CREATE OR REPLACE FUNCTION app.get_sportcenters()
RETURNS TABLE (id INTEGER,
                name VARCHAR(50),
                address VARCHAR(50))
SECURITY DEFINER
AS $$
BEGIN
    RETURN QUERY SELECT s.id, s.name, s.address FROM sportcenter AS s;
END;
$$ LANGUAGE plpgsql;
