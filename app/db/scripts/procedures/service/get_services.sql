CREATE OR REPLACE FUNCTION app.get_services()
RETURNS TABLE (id INTEGER, description TEXT, cost NUMERIC(5, 2))
SECURITY DEFINER
AS $$
BEGIN
    RETURN QUERY SELECT s.id, s.description, s.cost FROM service AS s;
END;
$$ LANGUAGE plpgsql;
