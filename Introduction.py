import streamlit as st
import warnings
from utils_pages import bubble_chart
from utils_pages import load_data
warnings.filterwarnings('ignore')
st.set_page_config(layout="wide")

# ---- QUERY ----
query = """
    SELECT 
    c.country,
    c.continent,
    mu.Ongoing_date AS "date",
    COUNT(CASE WHEN mu.title = 'GM' THEN 1 END) AS "count of Gm",
    COUNT(CASE WHEN mu.title != 'NT' THEN 1 END) AS "count of titled players",
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY mu.rating) AS "median of rating"
FROM MontlhyUpdates mu
LEFT JOIN countries c ON mu.fed = c.code    
WHERE FED not in ('NON','FID')   
GROUP BY c.country, mu.Ongoing_date, c.continent
ORDER BY mu.Ongoing_date asc,"median of rating" DESC

"""
df = load_data(query)
max_date = df['date'].max()
max_date_right_format = max_date.strftime("%Y-%m-%d")

# ---- PAGE TITLE ----
st.title("♟️ Chess Analytics: A Global Perspective")

# ---- PROJECT OVERVIEW ----
st.markdown(
    f"""
    ## 🌍 End-to-End Chess Analytics Project  

    This project explores the **global chess landscape** over the past **5 years**, leveraging **demographic insights** 
    and **chess performance metrics** to measure a country's chess strength.  

    🔵 Covers **200+ countries**.  
    🔵 Includes **only the top 100 strongest players** (by rating) from each country.  
    🔵 **Updated monthly** to reflect the latest trends. **Last update: {max_date_right_format}** 

    """
    )
# ---- KEY INSIGHTS ----

st.markdown("### 🔍 Some Key Insights")
st.markdown(
    """
    🌟 **If we assumed there are only 100 TOP players worldwide**:  """)

st.markdown(    
    """
    🔹94 would be men, only 6 women but among the top-performing countries, **China** challenges this trend.  
    🔹56 **wouldn't have a title**, 34 **would have a title (not GM)**, and **only 10 would be Grand Masters**.  
    🔹 **Nearly 6 out of 10 Grand Masters would be European**.  
    """
)
st.markdown(
    f"🌟 **Top 5 Chess Countries** (based on 3 key metrics). **Last update: {max_date_right_format}** ")

df = df[df['date']== max_date][['country','count of Gm',	'count of titled players',	'median of rating']].head()
st.dataframe(df, hide_index=True)  

# ---- INTERACTIVE BUBBLE CHART INTRO ----  
expander_bubble_chart = st.expander(" A Taste of the Data: Interactive Bubble Chart", icon="▶️")

with expander_bubble_chart:
    st.markdown("## 📊 A Taste of the Data: Interactive Bubble Chart")
    st.markdown(
        """
        This interactive **bubble plot** visualizes the relationship between **median Elo rating** and
        **number of Grand Masters (GMs)** for different countries over the last **5 years**.
        **Each bubble represents a country** and its size corresponds to the number of **titled players**.
        """
    )
    # Placeholder for Bubble Chart
    with st.container(border=True):
        
        fig = bubble_chart(query= query, color_column='continent' ,text= "Median Rating vs Amount of Gms Players <br> per Country Over Time <br>")

        st.plotly_chart(fig,use_container_width=True)
    
# ---- PROJECT OBJECTIVES ----
# Project structure
expander_objectives = st.expander("Objectives", icon="🎯")
with expander_objectives:
    st.markdown("### 🎯 Objectives")
    st.markdown(
        """
        🔵 **Exploring** the global chess landscape using **demographic variables** and **chess-related factors**.  
        🔵 **Measuring** a country’s chess strength through **3 key performance metrics**.
        """
    )

    # ---- DEMOGRAPHIC VARIABLES & CHESS FACTORS ----
    col1, col2, col3 = st.columns(3)
    with col1:
        # ---- KEY METRICS ----
        st.markdown("### 🔹Key Metrics") #📊
        st.markdown(
            """
            **📈 Median of rating**
            **👑 Number of Grand Masters**
            **🎖️ Number of titled players**
            """
        )

    with col2:
        st.markdown("### 🔹Demographic Variables") #🚻
        st.markdown(
            """
            **👨‍🦰 Gender**
            **📅 Age**
            """
        )

    with col3:
        st.markdown("### 🔹Chess-Related Factors") #🏆
        st.markdown(
            """
            🔄 **Activity status**
            🎖️ **Title**
            📊 **Rating**
            """
        )

# ---- PROJECT STRUCTURE ----
expander_project_structure = st.expander("Project Structure (5 Pages)", icon="🗂️")
with expander_project_structure:
    st.markdown("### 🗂️ Project Structure (5 Pages)")
    st.markdown(
        """
        1️⃣ **Introduction** - Overview of the project.  
        2️⃣ **Outlook** - Key insights and high-level trends.  
        3️⃣ **Continent Analysis** - Performance trends by continent.  
        4️⃣ **Comparison Tool** - Compare two countries (💡 *My favorite page!*)  
        5️⃣ **Top 5 Chess Players** - Highlights of the strongest players.  
        """
    )



#--- SOURCE OF DATA ---

expander_data = st.expander("Source of data", icon="💠")

with expander_data:
    st.markdown("### 💠Source of data")
    st.markdown("""
    The data used in this project is sourced from the [FIDE website](https://ratings.fide.com/download_lists.phtml), 
    which provides monthly updates. I downloaded data spanning **the last 5 years**, resulting in 60 text files containing 
    information on all players registered with FIDE—a significant amount of data!

    
    After preprocessing the data, I created a PostgreSQL database consisting of three tables:
    """)

    # Table descriptions
    st.markdown("""
    - 🔹**players:** Contains static player information.    
    - 🔹**countries:** Stores geographic attributes.
    - 🔹**monthlyupdates:** Holds dynamic player information that changes monthly.
    """)

# ---- PROJECT DOCUMENTATION ----
expander_documentation = st.expander("Documentation & Code", icon="📌")
with expander_documentation:
    st.markdown(
        """
        ## 📌 **Documentation & Code:**  
        Explore the full methodology and source code in the **GitHub repository**.  
        [🔗 Check it out here](https://github.com/hzoscar/chess_rating_analytics_project_streamlit.git)  
        """)
    
    
    
