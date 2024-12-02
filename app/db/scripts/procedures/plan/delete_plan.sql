CREATE OR REPLACE PROCEDURE app.delete_plan(
    in_id INTEGER
)
SECURITY DEFINER
AS $$
DECLARE
    result TEXT;
BEGIN
    DELETE FROM plan
    WHERE id = in_id
    RETURNING create_date INTO result;

    IF result IS NOT NULL THEN
        RAISE NOTICE 'Plan "%" ("%") has been deleted successfully.', in_id, result;
    ELSE
        RAISE NOTICE 'Plan "%" does not exist.', in_id;
    END IF;
END;
$$ LANGUAGE plpgsql;
