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

    IF (sportcenter_id IS NOT NULL) AND (NOT FOUND) THEN
        RAISE EXCEPTION 'Sportcenter "%" does not exist', sportcenter_id;
    END IF;
END;
$$ LANGUAGE plpgsql;
