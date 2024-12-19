import streamlit as st
from utils import load_data
from utils import customize_title_charts
from utils import customize_plotly_charts
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import warnings
warnings.filterwarnings('ignore')


query = """
WITH pre_aggregations AS(
SELECT 
    muomv.ongoing_date,
    COUNT(*) AS total_players,
    COUNT(CASE WHEN sex = 'M' THEN 1 END) AS total_men,
    COUNT(CASE WHEN sex = 'F' THEN 1 END) AS total_women,	
    COUNT(CASE WHEN c.continent = 'Asia' THEN 1 END) AS total_Asia,
    COUNT(CASE WHEN c.continent = 'Oceania' THEN 1 END)  AS total_Oceania,
    COUNT(CASE WHEN c.continent = 'Africa' THEN 1 END) AS total_Africa,
    COUNT(CASE WHEN c.continent = 'Europe' THEN 1 END) AS total_Europe,
    COUNT(CASE WHEN c.continent = 'Americas' THEN 1 END) AS total_Americas,  
    COUNT(CASE WHEN muomv.title IN ('CM','FM','IM','WCM','WFM','WGM','WH','WIM')  THEN 1 END)  AS total_other_titles,
	COUNT(CASE WHEN muomv.title = 'GM' THEN 1 END)  AS total_GMs,
	COUNT(CASE WHEN muomv.title = 'NT' THEN 1 END)  AS total_NO_TITLE,    
    COUNT(CASE WHEN muomv.activity_status = 'a' THEN 1 END)  AS total_active_players,
	COUNT(CASE WHEN muomv.activity_status = 'i' THEN 1 END) AS total_inactive_players,    
    COUNT(CASE WHEN muomv.age_category = 'Less than 19' THEN 1 END)  AS total_less_than_19,
 	COUNT(CASE WHEN muomv.age_category = '19-30' THEN 1 END) AS total_19_to_30,
	COUNT(CASE WHEN muomv.age_category = '31-40' THEN 1 END) AS total_31_to_40,
    COUNT(CASE WHEN muomv.age_category = '41-50' THEN 1 END) AS total_41_to_50,
    COUNT(CASE WHEN muomv.age_category = '51-65' THEN 1 END) AS total_51_to_65,
    COUNT(CASE WHEN muomv.age_category = 'More than 66' THEN 1 END)  AS total_more_than_66
FROM   montlhyupdate_open_players_with_age_group_mv muomv                                             --montlhyupdate_with_age_group_mv mumv
LEFT JOIN players p ON muomv.ID = p.ID
LEFT JOIN countries c ON muomv.fed = c.code
WHERE muomv.rating >= 1500 
  AND EXTRACT(MONTH FROM muomv.ongoing_date) = (SELECT get_last_month())
GROUP BY ongoing_date
    )
    
SELECT
	ongoing_date AS date,
    ROUND(total_men * 1.0 / NULLIF(total_players, 0), 2) AS percentage_men,
    ROUND(total_women * 1.0 / NULLIF(total_players, 0), 2) AS percentage_women,
    ROUND(total_Asia  * 1.0 / NULLIF(total_players, 0), 2) AS percentage_Asia,
    ROUND(total_Oceania  * 1.0 / NULLIF(total_players, 0), 2) AS percentage_Oceania,
    ROUND(total_Africa  * 1.0 / NULLIF(total_players, 0), 2) AS percentage_Africa,
    ROUND(total_Europe * 1.0 / NULLIF(total_players, 0), 2) AS percentage_Europe,
    ROUND(total_Americas * 1.0 / NULLIF(total_players, 0), 2) AS percentage_Americas,  
    ROUND(total_other_titles * 1.0 / NULLIF(total_players, 0), 2) AS percentage_other_titles,
	ROUND(total_GMs * 1.0 / NULLIF(total_players, 0), 2) AS percentage_GMs,
	ROUND(total_NO_TITLE * 1.0 / NULLIF(total_players, 0), 2) AS percentage_NO_TITLE,    
    ROUND(total_active_players * 1.0 / NULLIF(total_players, 0), 2) AS percentage_active_players,
	ROUND(total_inactive_players * 1.0 / NULLIF(total_players, 0), 2) AS percentage_inactive_players,    
    ROUND(total_less_than_19 * 1.0 / NULLIF(total_players, 0), 2) AS percentage_less_than_19,
 	ROUND(total_19_to_30 * 1.0 / NULLIF(total_players, 0), 2) AS percentage_19_to_30,
	ROUND(total_31_to_40 * 1.0 / NULLIF(total_players, 0), 2) AS percentage_31_to_40,
    ROUND(total_41_to_50 * 1.0 / NULLIF(total_players, 0), 2) AS percentage_41_to_50,
    ROUND(total_51_to_65 * 1.0 / NULLIF(total_players, 0), 2) AS percentage_51_to_65,
    ROUND(total_more_than_66 * 1.0 / NULLIF(total_players, 0), 2) AS percentage_more_than_66
    
FROM pre_aggregations
ORDER BY ongoing_date ASC;


"""



