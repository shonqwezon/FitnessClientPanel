CREATE OR REPLACE FUNCTION app.delete_client_plan(
    in_client_id INTEGER, in_plan_id INTEGER
)
RETURNS DATE
SECURITY DEFINER
AS $$
DECLARE
    result DATE;
BEGIN
    DELETE FROM client_plan
    WHERE client_id = in_client_id AND plan_id = in_plan_id
    RETURNING plan_end_date INTO result;

    RETURN result;
END;
$$ LANGUAGE plpgsql;
