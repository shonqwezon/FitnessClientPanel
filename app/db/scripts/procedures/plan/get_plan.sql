CREATE OR REPLACE FUNCTION app.get_plans(in_sportcenter_id INTEGER)
RETURNS TABLE (id INTEGER,
                final_cost NUMERIC(8, 2),
                begin_time TIME,
                end_time TIME)
SECURITY DEFINER
AS $$
BEGIN
    RETURN QUERY SELECT p.id,
                        app.calculate_plan_cost(p.id) AS final_cost,
                        p.begin_time,
                        p.end_time
                FROM plan AS p WHERE p.sportcenter_id = in_sportcenter_id;
END;
$$ LANGUAGE plpgsql;
