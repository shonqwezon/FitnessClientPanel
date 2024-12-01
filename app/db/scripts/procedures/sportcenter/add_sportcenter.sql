CREATE OR REPLACE PROCEDURE add_sportcenter(in_name VARCHAR(50),
                                        in_address VARCHAR(50),
                                        in_open_time TIME,
                                        in_close_time TIME,
                                        in_cost_ratio NUMERIC(3,2))
AS $$
BEGIN
    INSERT INTO sportcenter (name, address, open_time, close_time, cost_ratio)
        VALUES (in_name, in_address, in_open_time, in_close_time, in_cost_ratio);
    RAISE NOTICE 'Sportcenter "%" added successfully.', in_name;
END;
$$ LANGUAGE plpgsql;
