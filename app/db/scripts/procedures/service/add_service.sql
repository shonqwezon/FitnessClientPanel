CREATE OR REPLACE PROCEDURE add_service(in_description TEXT,
                                        in_cost NUMERIC(5, 2))
AS $$
BEGIN
    INSERT INTO service (description, cost)
        VALUES (in_description, in_cost);
    RAISE NOTICE 'Service "%" has been added successfully.', in_description;
END;
$$ LANGUAGE plpgsql;
