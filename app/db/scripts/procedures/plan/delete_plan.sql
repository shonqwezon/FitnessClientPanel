CREATE OR REPLACE PROCEDURE app.delete_plan(
    in_id INTEGER
)
SECURITY DEFINER
AS $$
BEGIN
    DELETE FROM plan WHERE id = in_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Plan "%" does not exist', in_id;
    END IF;
END;
$$ LANGUAGE plpgsql;
