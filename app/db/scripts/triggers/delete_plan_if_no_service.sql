CREATE OR REPLACE FUNCTION delete_plan_if_no_service()
RETURNS TRIGGER
SECURITY DEFINER
AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM plan_service WHERE plan_id = OLD.plan_id) THEN
        DELETE FROM plan WHERE id = OLD.plan_id;
        RAISE NOTICE 'Plan "%" has been deleted.', OLD.plan_id;
    ELSE
        RAISE NOTICE 'There is no need to delete plan.';
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trigger_delete_plan_if_no_service
AFTER DELETE ON plan_service
FOR EACH ROW EXECUTE FUNCTION delete_plan_if_no_service();
