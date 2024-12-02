CREATE OR REPLACE PROCEDURE app.delete_sportcenter(
    in_id INTEGER
)
SECURITY DEFINER
AS $$
DECLARE
    result TEXT;
BEGIN
    DELETE FROM sportcenter
    WHERE id = in_id
    RETURNING name INTO result;

    IF result IS NOT NULL THEN
        RAISE NOTICE 'Sportcenter "%" ("%") has been deleted successfully.', in_id, result;
    ELSE
        RAISE NOTICE 'Sportcenter "%" does not exist.', in_id;
    END IF;
END;
$$ LANGUAGE plpgsql;
