CREATE OR REPLACE FUNCTION app.get_services()
RETURNS TABLE (id INTEGER, description TEXT)
SECURITY DEFINER
AS $$
BEGIN
    RETURN QUERY SELECT s.id, s.description FROM service AS s;
END;
$$ LANGUAGE plpgsql;
