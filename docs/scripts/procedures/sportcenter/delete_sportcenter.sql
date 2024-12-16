CREATE OR REPLACE PROCEDURE app.delete_sportcenter(
    in_id INTEGER
)
SECURITY DEFINER
AS $$
BEGIN
    DELETE FROM sportcenter WHERE id = in_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Sportcenter "%" does not exist', in_id;
    END IF;
END;
$$ LANGUAGE plpgsql;
