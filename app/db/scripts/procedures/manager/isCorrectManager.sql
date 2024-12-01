CREATE OR REPLACE FUNCTION is_correct_manager(
    email VARCHAR(50),
    password_hash VARCHAR(64)
)
RETURNS BOOLEAN AS $$
DECLARE
    result BOOLEAN;
BEGIN
    SELECT EXISTS (
        SELECT 1
        FROM manager AS m
        WHERE m.email = email AND m.password_hash = password_hash
    ) INTO result;

    RETURN result;
END;
$$ LANGUAGE plpgsql;
