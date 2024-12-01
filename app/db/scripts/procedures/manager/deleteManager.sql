CREATE OR REPLACE PROCEDURE delete_manager(
    fullname VARCHAR(50)
)
DECLARE
    result BOOLEAN := FALSE;
BEGIN
    DELETE FROM manager AS m
    WHERE m.fullname = fullname
    RETURNING TRUE INTO result;

    IF result THEN
        RAISE NOTICE 'Manager "%" has been deleted successfully.', fullname;
    ELSE
        RAISE NOTICE 'Manager "%" does not exist.', fullname;
    END IF;
END;
$$ LANGUAGE plpgsql;
