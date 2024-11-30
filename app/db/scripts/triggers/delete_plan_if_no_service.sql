CREATE OR REPLACE FUNCTION delete_plan_if_no_service()
RETURNS TRIGGER AS
$$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM plan_service WHERE plan_id = OLD.plan_id) THEN
        DELETE FROM plan WHERE id = OLD.plan_id;
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trigger_delete_plan_if_no_service
AFTER DELETE ON plan_service
FOR EACH ROW EXECUTE FUNCTION delete_plan_if_no_service();
