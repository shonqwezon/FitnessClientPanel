CREATE OR REPLACE PROCEDURE add_manager(fullname VARCHAR(50),
                                        email VARCHAR(50),
                                        password_hash VARCHAR(64),
                                        sportcenter_id INTEGER)
AS $$
BEGIN
    INSERT INTO manager (fullname, email, password_hash, sportcenter_id)
        VALUES (fullname, email, password_hash, sportcenter_id);
    RAISE NOTICE 'Manager "%" added successfully.', email;
END;
$$ LANGUAGE plpgsql;
