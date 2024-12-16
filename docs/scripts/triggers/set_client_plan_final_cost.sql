CREATE OR REPLACE FUNCTION set_plan_final_cost()
RETURNS TRIGGER
SECURITY DEFINER
AS $$
BEGIN
    NEW.final_cost := app.calculate_plan_cost(NEW.plan_id) * (NEW.plan_end_date - NEW.plan_begin_date);
    RAISE NOTICE 'Final cost has been updated.';
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE TRIGGER trigger_set_plan_final_cost
BEFORE INSERT ON client_plan
FOR EACH ROW EXECUTE FUNCTION set_plan_final_cost();
