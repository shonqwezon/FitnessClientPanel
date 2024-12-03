CREATE OR REPLACE PROCEDURE app.add_client(in_fullname VARCHAR(50))
SECURITY DEFINER
AS $$
BEGIN
    INSERT INTO client (fullname) VALUES (in_fullname);
    RAISE NOTICE 'Client "%" has been added successfully.', in_fullname;
END;
$$ LANGUAGE plpgsql;
