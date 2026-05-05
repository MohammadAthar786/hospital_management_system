-- checking foreign key constraint name 
SELECT conname
FROM pg_constraint
WHERE conrelid = 'medications'::regclass;