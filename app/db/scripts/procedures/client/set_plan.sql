CREATE OR REPLACE PROCEDURE app.set_plan(in_client_id INTEGER, in_plan_id INTEGER, plan_end DATE)
SECURITY DEFINER
AS $$
BEGIN
    BEGIN
        PERFORM app.delete_client_plan(in_client_id);
    EXCEPTION
        WHEN OTHERS THEN
            RAISE NOTICE 'There is no plans to delete: "%"', SQLERRM;
    END;
    INSERT INTO client_plan (client_id, plan_id, plan_end_date)
        VALUES (in_client_id, in_plan_id, plan_end);
    RAISE NOTICE 'Plan "%" has been set successfully to client "%" until "%".',
        in_plan_id, in_client_id, plan_end;
END;
$$ LANGUAGE plpgsql;
