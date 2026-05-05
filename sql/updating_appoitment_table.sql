UPDATE appointments
SET 
    start_time = created_at::time,
    end_time = 
        CASE 
            WHEN (created_at::time + interval '30 minutes') > '23:59:59'
            THEN '23:59:59'
            ELSE (created_at + interval '30 minutes')::time
        END
WHERE start_time IS NULL;

-- Verifying data 
SELECT id, created_at, start_time, end_time
FROM appointments
LIMIT 10;