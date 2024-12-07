CREATE OR REPLACE FUNCTION app.get_client_plan(in_client_id INTEGER)
RETURNS INTEGER
SECURITY DEFINER
AS $$
DECLARE
    plan_id INTEGER;
BEGIN
    SELECT cp.plan_id INTO plan_id FROM client_plan AS cp WHERE in_client_id = cp.client_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Plan of client "%" does not exist', in_client_id;
    END IF;

    RETURN plan_id;
END;
$$ LANGUAGE plpgsql;
