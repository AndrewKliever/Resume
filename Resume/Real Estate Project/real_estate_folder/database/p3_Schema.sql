-- Creating schema if not found and then creating table

CREATE SCHEMA IF NOT EXISTS p3_Schema;

CREATE TABLE p3_Schema.RAW(

state VARCHAR(50),
city VARCHAR(50),	
"avg.list price" VARCHAR(50),
"avg.price/sqft" VARCHAR(50),
"avg.days on market" VARCHAR(50),
lat VARCHAR(50),
lng VARCHAR(50)

);

-- Creating table to stage data pulled from csv file into

CREATE TABLE p3_Schema.cleaned(

state VARCHAR(50),
city VARCHAR(50),	
"avg.list price" VARCHAR(50),
"avg.price/sqft" VARCHAR(50),
"avg.days on market" VARCHAR(50),
lat VARCHAR(50),
lng VARCHAR(50)

);

-- Copying data from csv file into new staging table

COPY p3_Schema.RAW
FROM '/Users/kp/Git/project_3 - Final/database/cleaned_redfin_data_with_coords.csv' 
DELIMITER ',' 
CSV HEADER 
;

--Copying data from staging table and eliminating rows with null value in WHERE clause

INSERT INTO p3_Schema.cleaned
(
	state, 
    city, 
    "avg.list price", 
    "avg.price/sqft", 
    "avg.days on market",
	lat,
	lng
)

SELECT
	state, 
    city, 
    "avg.list price", 
    "avg.price/sqft", 
    "avg.days on market",
	lat,
	lng

FROM p3_Schema.RAW

WHERE
	p3_Schema.RAW."avg.list price" IS NOT NULL

	AND
	
    p3_Schema.RAW."avg.price/sqft" IS NOT NULL
;




