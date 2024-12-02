CREATE OR REPLACE FUNCTION app.get_sportcenter(sportcenter_id INTEGER DEFAULT NULL)
RETURNS TABLE (id INTEGER,
                name VARCHAR(50),
                address VARCHAR(50))
STABLE
SECURITY DEFINER
AS $$
BEGIN
    RETURN QUERY SELECT s.id, s.name, s.address FROM sportcenter AS s
        WHERE (sportcenter_id IS NULL OR s.id = sportcenter_id);
END;
$$ LANGUAGE plpgsql;
