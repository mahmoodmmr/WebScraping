-- Step 1: Add the new address column
--ALTER TABLE heroes ADD COLUMN address TEXT;

-- Step 2: Update the address column by copying the name and making necessary changes
--UPDATE heroes
--SET address = LOWER(REPLACE(name, ' ', '-'));


UPDATE heroes
SET address = REPLACE(address, '''', '');