CREATE OR REPLACE PROCEDURE app.delete_manager(
    in_fullname VARCHAR(50)
)
SECURITY DEFINER
AS $$
BEGIN
    DELETE FROM manager WHERE fullname = in_fullname;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Manager "%" does not exist', in_fullname;
    END IF;
END;
$$ LANGUAGE plpgsql;
