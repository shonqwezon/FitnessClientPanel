CREATE OR REPLACE FUNCTION app.get_plan_tech(in_sportcenter_id INTEGER DEFAULT NULL)
RETURNS TABLE (id INTEGER,
                name VARCHAR(50),
                sportcenter_name VARCHAR(50),
                base_cost NUMERIC(8, 2),
                begin_time TIME,
                end_time TIME,
                create_date TIMESTAMP)
SECURITY DEFINER
AS $$
BEGIN
    RETURN QUERY SELECT p.id,
                        p.name,
                        sc.name,
                        p.base_cost,
                        p.begin_time,
                        p.end_time,
                        p.create_date
                FROM plan AS p
                JOIN sportcenter sc ON sc.id = p.sportcenter_id
                WHERE (in_sportcenter_id IS NULL OR p.sportcenter_id = in_sportcenter_id);

    IF (in_sportcenter_id IS NOT NULL) AND (NOT FOUND) THEN
        RAISE EXCEPTION 'Plans of sportcenter "%" for admin do not exist', in_sportcenter_id;
    END IF;
END;
$$ LANGUAGE plpgsql;
