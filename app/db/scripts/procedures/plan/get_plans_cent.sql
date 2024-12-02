CREATE OR REPLACE FUNCTION app.get_plans(in_sportcenter_id INTEGER)
RETURNS TABLE (id INTEGER,
                final_cost NUMERIC(8, 2),
                begin_time TIME,
                end_time TIME,
                body TEXT[])
SECURITY DEFINER
AS $$
BEGIN
    RETURN QUERY SELECT p.id,
                        app.calculate_plan_cost(p.id) AS final_cost,
                        p.begin_time,
                        p.end_time,
                        array_agg(s.description) AS body
                FROM plan AS p
                JOIN plan_service ps ON ps.plan_id = p.id
                JOIN service s ON s.id = ps.service_id
                WHERE p.sportcenter_id = in_sportcenter_id
                GROUP BY p.id;
END;
$$ LANGUAGE plpgsql;
