import streamlit as st
from utils import load_data
## App title

st.set_page_config(page_title='Chess Players Analysis', layout='wide')

st.title('Chess Players Analytics Dashboard')

# # Sidebar for Navigation
page = st.sidebar.selectbox(
     "Select Dashboard",
     ("Overview", "Dashboard 1", "Dashboard 2", "Dashboard 3", "Dashboard 4"))


# Example: Fetch top players from the "Open" group
query = """
    SELECT name, rating 
    FROM project.players 
    WHERE Group_index = 'O' AND date = '01-11-2024' AND  activity_status = 'a'
    ORDER BY Rating DESC
    LIMIT 10;
"""

df = load_data(query)
print(df)




# Load the selected dashboard
# if page == "Dashboard 1":
#     dashboard_1.show()
# elif page == "Dashboard 2":
#     dashboard_2.show()
# elif page == "Dashboard 3":
#     dashboard_3.show()
# elif page == "Dashboard 4":
#     dashboard_4.show()
# else:
#     st.write("Welcome to the Chess Analytics App! Select a dashboard from the sidebar.")