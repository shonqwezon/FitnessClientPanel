CREATE OR REPLACE PROCEDURE app.add_plan(in_base_cost NUMERIC(8, 2),
                                        in_begin_time TIME,
                                        in_end_time TIME,
                                        in_sportcenter_id INTEGER)
SECURITY DEFINER
AS $$
DECLARE
    new_id INTEGER;
BEGIN
    INSERT INTO plan (base_cost, begin_time, end_time, sportcenter_id)
        VALUES (in_base_cost, in_begin_time, in_end_time, in_sportcenter_id) RETURNING id INTO new_id;
    RAISE NOTICE 'Plan "%" has been added successfully.', new_id;
END;
$$ LANGUAGE plpgsql;
