



df_gender = load_data(query)

# Generate the tick values and labels
#tick_vals = df_gender["date"]
tick_labels = df_gender["date"].dt.strftime("%Y-%m").unique() # Leave as a global variable?

# Create the figure
fig_gender = go.Figure()

# Add the first bar trace (e.g., Men) with custom color
fig_gender.add_trace(go.Bar(
    x=df_gender["date"],
    y=df_gender["percentage_men"].round(2),
    name="Men",
    marker_color="cadetblue"  # Custom color
))
# Add the second bar trace (e.g., Women) with custom color
fig_gender.add_trace(go.Bar(
    x=df_gender["date"],
    y=df_gender["percentage_women"].round(2),
    name="Women",
    marker_color="goldenrod"  # Custom color
))

title_gender = customize_title_charts(text="Trends in Gender Distribution Among Top Players",
                                      y=0.9,
                                      x=0.5,
                                      xanchor='center',
                                      yanchor='top',
                                      font=dict(size=20),
                                      subtitle= dict(
                                        text="Gender percentages among the strongest 100 players <br> per country over the last 10 years <br>",
                                        font=dict(color="gray", size=12))                     
                                        )

fig_gender = customize_plotly_charts(fig=fig_gender,                                     
                                     barmode='stack',
                                     xaxis_title='Date',
                                     yaxis_title='Percentage',
                                     legend_title='Category',
                                     bargap=0.3,
                                     width=800,
                                     height=400,
                                     title=title_gender,
                                     font=dict(
                                        family="Courier New, monospace",
                                        size=12),
                                     tickvals=tick_labels,
                                    ticktext=tick_labels,
                                    tickangle=45                                    
                                    )


st.plotly_chart(fig_gender,use_container_width=True)