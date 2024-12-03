CREATE OR REPLACE FUNCTION check_plan_time()
RETURNS TRIGGER
SECURITY DEFINER
AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM sportcenter s
        WHERE s.id = NEW.sportcenter_id
          AND (NEW.begin_time <= s.open_time OR NEW.end_time >= s.close_time)
    ) THEN
        RAISE EXCEPTION 'worker hours of plan must be beetwen worker hours of sportcenter';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE TRIGGER trigger_check_plan_time
BEFORE INSERT ON plan
FOR EACH ROW EXECUTE FUNCTION check_plan_time();
