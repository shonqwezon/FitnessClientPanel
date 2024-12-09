CREATE OR REPLACE FUNCTION app.delete_client_plan(in_client_id INTEGER)
RETURNS DATE
SECURITY DEFINER
AS $$
DECLARE
    result DATE;
BEGIN
    DELETE FROM client_plan
    WHERE client_id = in_client_id RETURNING plan_end_date INTO result;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Client "%" or Plan "%" does not exist', in_client_id, in_plan_id;
    END IF;
    RETURN result;
END;
$$ LANGUAGE plpgsql;
