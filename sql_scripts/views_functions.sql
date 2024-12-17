------------------------------------------------------------------------------------------
--top_10_open_players_view
------------------------------------------------------------------------------------------

-- Create a view named 'top_10_open_players_view' to display the top 10 open players by rating for each month.
CREATE VIEW top_10_open_players_view AS
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
        Group_index = 'O'  -- Filter for players in the Open category ('O').
        AND FED NOT IN ('NON', 'FID')  -- Exclude federations 'NON' (non-existent) and 'FID' (FIDE).
        AND activity_status = 'a'  -- Include only active players ('a').
)
SELECT
    t.name,  -- Select the player's name from the CTE.
    t.rating,  -- Select the player's rating.
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