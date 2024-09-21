--CREATE TABLE heroes_with_image AS SELECT * FROM heroes;


--ALTER TABLE heroes_with_image ADD COLUMN imageAddress TEXT;

--UPDATE heroes_with_image
--SET imageAddress = 'https://www.dotabuff.com/assets/heroes/' || name || '.jpg';
