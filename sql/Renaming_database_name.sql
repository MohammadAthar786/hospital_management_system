-- Checking Active connection of a database
SELECT pid, datname, usename, state
FROM pg_stat_activity
WHERE datname = 'old_database_name';

-- terminating all active connections of a database

SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = 'old_database_name'
  AND pid <> pg_backend_pid();

--Renaming databse name 
ALTER DATABASE old_database_name RENAME TO new_database_name;