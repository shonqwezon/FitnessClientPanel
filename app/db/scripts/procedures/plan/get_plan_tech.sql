CREATE OR REPLACE FUNCTION app.get_plan_tech(in_sportcenter_id INTEGER DEFAULT NULL)
RETURNS TABLE (id INTEGER,
                sportcenter_id INTEGER,
                base_cost NUMERIC(8, 2),
                begin_time TIME,
                end_time TIME,
                create_date TIMESTAMP)
SECURITY DEFINER
AS $$
BEGIN
    RETURN QUERY SELECT p.id,
                        p.sportcenter_id,
                        p.base_cost,
                        p.begin_time,
                        p.end_time,
                        p.create_date
                FROM plan AS p WHERE (in_sportcenter_id IS NULL OR p.sportcenter_id = in_sportcenter_id);

    IF (in_sportcenter_id IS NOT NULL) AND (NOT FOUND) THEN
        RAISE EXCEPTION 'Plans of sportcenter "%" for admin do not exist', in_sportcenter_id;
    END IF;
END;
$$ LANGUAGE plpgsql;
