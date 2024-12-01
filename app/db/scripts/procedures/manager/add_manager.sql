CREATE OR REPLACE PROCEDURE add_manager(in_fullname VARCHAR(50),
                                        in_email VARCHAR(50),
                                        in_password_hash VARCHAR(64),
                                        in_sportcenter_id INTEGER)
AS $$
BEGIN
    INSERT INTO manager (fullname, email, password_hash, sportcenter_id)
        VALUES (in_fullname, in_email, in_password_hash, in_sportcenter_id);
    RAISE NOTICE 'Manager "%" has been added successfully.', in_email;
END;
$$ LANGUAGE plpgsql;
