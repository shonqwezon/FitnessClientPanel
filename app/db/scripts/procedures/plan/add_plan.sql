CREATE OR REPLACE PROCEDURE app.add_plan(in_base_cost NUMERIC(8, 2),
                                        in_begin_time TIME,
                                        in_end_time TIME,
                                        in_sportcenter_id INTEGER,
                                        service_ids INTEGER[])
SECURITY DEFINER
AS $$
DECLARE
    new_id INTEGER;
    service_id INTEGER;
BEGIN
    IF (service_ids IS NULL) OR (array_length(service_ids, 1) IS NULL) THEN
        RAISE EXCEPTION 'Service idss array cannot be EMPTY';
    END IF;

    INSERT INTO plan (base_cost, begin_time, end_time, sportcenter_id)
        VALUES (in_base_cost, in_begin_time, in_end_time, in_sportcenter_id) RETURNING id INTO new_id;

    FOREACH service_id IN ARRAY service_ids LOOP
        INSERT INTO plan_service VALUES (new_id, service_id);
    END LOOP;

    RAISE NOTICE 'Plan "%" has been added successfully.', new_id;
END;
$$ LANGUAGE plpgsql;
