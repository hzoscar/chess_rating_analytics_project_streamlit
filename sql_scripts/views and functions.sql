------------------------------------------------------------------------------------------
--top_10_open_players_view
------------------------------------------------------------------------------------------

-- Create a view named 'top_10_open_players_view' to display the top 10 open players by rating for the last month month.
CREATE VIEW top_10_open_players_view AS
WITH top_10_players AS ( 
    -- Define a Common Table Expression (CTE) to calculate the rankings of players for last date.
    SELECT 
        mu.*,  -- Select all columns from the MontlhyUpdates table.
        p.name,  -- Add the player's name from the players table.
        ROW_NUMBER() OVER (
            PARTITION BY mu.ongoing_date  -- Partition by the ongoing_date to calculate rank per month.
            ORDER BY mu.rating DESC       -- Rank players by their rating in descending order.
        ) AS rank
    FROM MontlhyUpdates mu
    LEFT JOIN players p ON mu.ID = p.ID  -- Join the MontlhyUpdates table with players to get player names.
    WHERE 
        -- Group_index = 'O' AND  -- Filter for players in the Open category ('O').
        FED NOT IN ('NON', 'FID')  -- Exclude federations 'NON' (non-existent) and 'FID' (FIDE).
        AND activity_status = 'a'  -- Include only active players ('a').
		AND ongoing_date = (select max(ongoing_date)from MontlhyUpdates mu )
        )
SELECT
    t.name,  -- Select the player's name from the CTE.
    t.rating,  -- Select the player's rating.
    t.fed,
    t.ongoing_date  -- Select the date of the update.
FROM top_10_players t
LEFT JOIN countries c ON t.fed = c.code  -- Optionally join with the countries table to add country metadata.
WHERE t.rank <= 10  -- Filter the top 10 players for each date based on their ranking.
ORDER BY t.ongoing_date ASC;  -- Order the results by date in ascending order.

-----------------------------------------------------------------
-- top_10_open_players_over_time_view
-----------------------------------------------------------------

-- Create a view named 'top_10_open_players_over_time_view' to display the top 10 open players by rating for each month.
CREATE VIEW top_10_open_players_over_time_view AS
WITH top_10_players AS ( 
    -- Define a Common Table Expression (CTE) to calculate the rankings of players for each date.
    SELECT 
        mu.*,  -- Select all columns from the MontlhyUpdates table.
        p.name,  -- Add the player's name from the players table.
        ROW_NUMBER() OVER (
            PARTITION BY mu.ongoing_date  -- Partition by the ongoing_date to calculate rank per month.
            ORDER BY mu.rating DESC       -- Rank players by their rating in descending order.
        ) AS rank
    FROM MontlhyUpdates mu
    LEFT JOIN players p ON mu.ID = p.ID  -- Join the MontlhyUpdates table with players to get player names.
    WHERE 
        -- Group_index = 'O' AND  -- Filter for players in the Open category ('O').
        FED NOT IN ('NON', 'FID')  -- Exclude federations 'NON' (non-existent) and 'FID' (FIDE).
        AND activity_status = 'a'  -- Include only active players ('a').
		)
SELECT
    t.name,  -- Select the player's name from the CTE.
    t.rating,  -- Select the player's rating.
    t.fed,
    t.ongoing_date  -- Select the date of the update.
FROM top_10_players t
LEFT JOIN countries c ON t.fed = c.code  -- Optionally join with the countries table to add country metadata.
WHERE t.rank <= 10  -- Filter the top 10 players for each date based on their ranking.
ORDER BY t.ongoing_date ASC;  -- Order the results by date in ascending order.


-----------------------------------------------------------------------------
-- Function get_last_month
-----------------------------------------------------------------------------
-- Create a function named 'get_last_month' that returns an integer value.
CREATE FUNCTION get_last_month()
    RETURNS INT  -- Specifies that the function will return an integer.
    LANGUAGE plpgsql  -- Defines the function's language as PL/pgSQL.
	AS
	$$
	DECLARE
    	last_month INTEGER;  -- Declare a variable to store the result (last month's value).
	BEGIN
	    -- Extract the month from the maximum 'Ongoing_date' in the 'MonthlyUpdates' table.
	    SELECT 
	        EXTRACT(MONTH FROM MAX(mu.Ongoing_date))  -- Get the month part of the latest date.
	    INTO last_month  -- Store the result in the 'last_month' variable.
	    FROM MontlhyUpdates mu;  -- Query the 'MonthlyUpdates' table.
	    
	    -- Return the value of 'last_month'.
	    RETURN last_month;
	END;
	$$;

-----------------------------------------------------------------------------
-- Function get_last_YEAR
-----------------------------------------------------------------------------
-- Create a function named 'get_last_year' that returns an integer value.
CREATE FUNCTION get_last_year()
    RETURNS INT  -- Specifies that the function will return an integer.
    LANGUAGE plpgsql  -- Defines the function's language as PL/pgSQL.
	AS
	$$
	DECLARE
    	last_year INTEGER;  -- Declare a variable to store the result (last month's value).
	BEGIN
	    -- Extract the month from the maximum 'Ongoing_date' in the 'MonthlyUpdates' table.
	    SELECT 
	        EXTRACT(YEAR FROM MAX(mu.Ongoing_date))  -- Get the month part of the latest date.
	    INTO last_year  -- Store the result in the 'last_month' variable.
	    FROM MontlhyUpdates mu;  -- Query the 'MonthlyUpdates' table.
	    
	    -- Return the value of 'last_month'.
	    RETURN last_year;
	END;
	$$;

-----------------------------------------------------------------------------
-- Materialized view montlhyupdate_open_players_with_age_group_mv
-----------------------------------------------------------------------------

CREATE MATERIALIZED VIEW montlhyupdate_open_players_with_age_group_mv AS
SELECT 
    mu.*,
    EXTRACT(YEAR FROM mu.ongoing_date) - p.b_day AS age,
    CASE 
        WHEN EXTRACT(YEAR FROM mu.ongoing_date) - p.b_day <= 18 THEN 'Less than 19'
        WHEN EXTRACT(YEAR FROM mu.ongoing_date) - p.b_day BETWEEN 19 AND 30 THEN '19-30'
        WHEN EXTRACT(YEAR FROM mu.ongoing_date) - p.b_day BETWEEN 31 AND 40 THEN '31-40'
        WHEN EXTRACT(YEAR FROM mu.ongoing_date) - p.b_day BETWEEN 41 AND 50 THEN '41-50'
        WHEN EXTRACT(YEAR FROM mu.ongoing_date) - p.b_day BETWEEN 51 AND 65 THEN '51-65'
        ELSE 'More than 66'
    END AS age_category
FROM montlhyupdates mu
LEFT JOIN players p on mu.ID = p.ID
--WHERE mu.group_index='O';

CREATE INDEX idx_o_rating ON montlhyupdate_open_players_with_age_group_mv (rating);
CREATE INDEX idx_o_ongoing_date ON montlhyupdate_open_players_with_age_group_mv (ongoing_date);