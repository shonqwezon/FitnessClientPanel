CREATE OR REPLACE FUNCTION is_correct_manager(
    in_email VARCHAR(50),
    in_password_hash VARCHAR(64)
)
RETURNS BOOLEAN AS $$
DECLARE
    result BOOLEAN;
BEGIN
    SELECT EXISTS (
        SELECT 1
        FROM manager
        WHERE email = in_email AND password_hash = in_password_hash
    ) INTO result;

    RETURN result;
END;
$$ LANGUAGE plpgsql;
