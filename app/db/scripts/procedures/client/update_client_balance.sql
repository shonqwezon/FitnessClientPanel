CREATE OR REPLACE PROCEDURE app.update_client_balance(client_id INTEGER, new_balance INTEGER)
SECURITY DEFINER
AS $$
BEGIN
    UPDATE client SET balance = new_balance WHERE id = client_id;
    RAISE NOTICE 'Balance of client "%" has been updated successfully (new balance = %).',
        client_id, new_balance;
END;
$$ LANGUAGE plpgsql;
