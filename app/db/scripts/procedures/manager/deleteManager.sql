CREATE OR REPLACE PROCEDURE delete_manager(
    in_fullname VARCHAR(50)
)
AS $$
DECLARE
    result BOOLEAN := FALSE;
BEGIN
    DELETE FROM manager
    WHERE fullname = in_fullname
    RETURNING TRUE INTO result;

    IF result THEN
        RAISE NOTICE 'Manager "%" has been deleted successfully.', in_fullname;
    ELSE
        RAISE NOTICE 'Manager "%" does not exist.', in_fullname;
    END IF;
END;
$$ LANGUAGE plpgsql;
