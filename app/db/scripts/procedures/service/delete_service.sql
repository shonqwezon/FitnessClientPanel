CREATE OR REPLACE PROCEDURE app.delete_service(
    in_id INTEGER
)
SECURITY DEFINER
AS $$
DECLARE
    result TEXT;
BEGIN
    DELETE FROM service
    WHERE id = in_id
    RETURNING description INTO result;

    IF result IS NOT NULL THEN
        RAISE NOTICE 'Service "%" ("%") has been deleted successfully.', in_id, result;
    ELSE
        RAISE NOTICE 'Service "%" does not exist.', in_id;
    END IF;
END;
$$ LANGUAGE plpgsql;
