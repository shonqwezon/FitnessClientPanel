CREATE OR REPLACE FUNCTION update_client_balance()
RETURNS TRIGGER AS
$$
DECLARE
    left_days_ratio REAL;
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE client
            SET balance = balance - NEW.final_cost
            WHERE client.id = NEW.client_id;
    ELSIF TG_OP = 'DELETE' THEN
        left_days_ratio := EXTRACT(DAY FROM (OLD.plan_end_date - CURRENT_DATE)) /
                EXTRACT(DAY FROM (OLD.plan_end_date - OLD.plan_begin_date));

        UPDATE client
            SET balance = balance + OLD.final_cost * left_days_ratio
            WHERE client.id = OLD.client_id;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trigger_update_balance
AFTER INSERT OR DELETE ON client_plan
FOR EACH ROW EXECUTE FUNCTION update_client_balance();
