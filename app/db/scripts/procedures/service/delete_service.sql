CREATE OR REPLACE PROCEDURE app.delete_service(
    in_id INTEGER
)
SECURITY DEFINER
AS $$
BEGIN
    DELETE FROM service WHERE id = in_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Service "%" does not exist', in_id;
    END IF;
END;
$$ LANGUAGE plpgsql;
