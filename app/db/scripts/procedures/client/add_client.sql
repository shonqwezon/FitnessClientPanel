CREATE OR REPLACE PROCEDURE app.add_client(in_fullname VARCHAR(50), in_balance NUMERIC(8, 2))
SECURITY DEFINER
AS $$
BEGIN
    INSERT INTO client (fullname, balance) VALUES (in_fullname, in_balance);
    RAISE NOTICE 'Client "%" has been added successfully with balance "%".', in_fullname, in_balance;
END;
$$ LANGUAGE plpgsql;
