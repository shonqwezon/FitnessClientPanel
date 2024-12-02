CREATE OR REPLACE FUNCTION app.get_plan_tech(in_sportcenter_id INTEGER)
RETURNS TABLE (id INTEGER,
                base_cost NUMERIC(8, 2),
                begin_time TIME,
                end_time TIME,
                create_date TIMESTAMP)
SECURITY DEFINER
AS $$
BEGIN
    RETURN QUERY SELECT p.id,
                        p.base_cost,
                        p.begin_time,
                        p.end_time,
                        p.create_date
                FROM plan AS p WHERE p.sportcenter_id = in_sportcenter_id;
END;
$$ LANGUAGE plpgsql;
