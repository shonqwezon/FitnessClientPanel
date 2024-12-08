CREATE OR REPLACE FUNCTION app.get_client_plan(in_client_id INTEGER)
RETURNS TABLE (plan_id INTEGER, plan_begin_date DATE, plan_end_date DATE)
SECURITY DEFINER
AS $$
BEGIN
    RETURN QUERY SELECT cp.plan_id, cp.plan_begin_date, cp.plan_end_date
        FROM client_plan AS cp
        WHERE in_client_id = cp.client_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Plan of client "%" does not exist', in_client_id;
    END IF;
END;
$$ LANGUAGE plpgsql;
