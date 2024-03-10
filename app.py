import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

olympics_logo ='https://lottie.host/a7c3b6e4-ff56-41dd-84b3-c844e2cdd27a/ZbddSVs3bF.json'
browse_data_animation='https://assets1.lottiefiles.com/packages/lf20_xmkgn4jj.json'

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,region_df)

st.sidebar.title("Sports Data Analysis")
st.sidebar.image('https://miro.medium.com/v2/resize:fit:3840/1*R_nXSzwJP9U-QO8Hgg72ew.jpeg')

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Overall Analysis','Medal Tally','Country-wise Analysis','Athlete wise Analysis', 'Browse Data')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")
        
    st.image('https://library.sportingnews.com/styles/twitter_card_120x120/s3/2022-01/Beijing-Olympic-medals-013122-Getty-FTR.jpg?itok=j0IAWute')
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    st.image('https://assets3.thrillist.com/v1/image/2740765/size/gn-gift_guide_variable_c_2x.jpg')
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x="Edition", y="region")
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.title("Events over the years")
    st.plotly_chart(fig)

    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="Edition", y="Name")
    st.title("Athletes over the years")
    st.plotly_chart(fig)

    st.title("No. of Events over time(Every Sport)")
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)

    st.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a Sport',sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu == 'Country-wise Analysis':

    st.sidebar.title('Country-wise Analysis')
    st.title("Country Wise analysis")
    st.image("https://content.api.news/v3/images/bin/b4dbca8dceeffc5a9da37c2dfe3f6e18")
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)

    st.title(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title("Top 10 athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)

if user_menu == 'Athlete wise Analysis':
    st.title("Athlete Wise Analysis")
    st.image("https://api.time.com/wp-content/uploads/2021/07/time_olympics_digital_final.jpg")
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)

if user_menu == 'Browse Data':
    st.title("Data Analysis")
    data = st.file_uploader("Upload a Dataset", type=["csv", "txt"])
    if data is None:
        st.image("https://datarundown.com/wp-content/uploads/2023/05/Model-Data-Analytics.jpg")

    if data is not None:
        activities = ["EDA","Pandas Profiling Report" , 'Sweetviz Report']
        choice = st.sidebar.selectbox("Select Activities", activities)
        df = pd.read_csv(data)

        # In EDA we are going to show some general analysis and some plots 
        # These plots are going to visualize the Dataset more effectively and Quickly 
        # So I have included some visuals here like Animated Plots , 3D , 2D , Heatmaps etc

        if choice == 'EDA':
            st.subheader("Exploratory Data Analysis")
            col=df.columns.to_list()
            
            st.dataframe(df.head())

            analyse=["Basic Features","2D , Animated & Facet Plots" , "Pie Charts" , "Heatmaps, 3D & Ternary Plots"]
            feature=st.sidebar.selectbox("Choose an Option" , analyse)

            if feature=="Basic Features":
                if st.checkbox("Show Shape"):
                    st.write(df.shape)

                if st.checkbox("Show Columns"):
                    all_columns = df.columns.to_list()
                    st.write(all_columns)

                if st.checkbox("Summary"):
                    try:
                        st.write(df.describe())
                    except:
                        st.warning("df.describe() cannot be performed on the given Dataset")

                if st.checkbox("Show Selected Columns"):
                    all_columns = df.columns.to_list()
                    selected_columns = st.multiselect("Select Columns", all_columns)
                    new_df = df[selected_columns]
                    st.dataframe(new_df)

                if st.checkbox("Correlation Plot(Seaborn)"):
                    try:
                       fig, ax = plt.subplots(figsize=(16, 7))
                       ax=sns.heatmap(df.corr(),cmap='rocket_r',fmt=".1f", annot=True)
                       st.pyplot(fig)
                    except:
                        st.warning('Correlation Plot cannot be performed on the given Dataset')

                if st.checkbox("Value Count Plot"):
                    try:
                        selected_col = st.selectbox("Choose a col",col)
                        df = df.dropna(subset=[selected_col]) 
                        data_Graph = df[selected_col].value_counts().reset_index().sort_values('index')
                        data_Graph.rename(columns={'index': selected_col, selected_col: 'Counts'}, inplace=True)
                        fig = px.bar(data_Graph, x=selected_col, y='Counts', color_discrete_sequence=['#F63366'],template='plotly_white')
                        st.plotly_chart(fig)
                    except:
                        st.warning('Rows & Columns of the given dataset is not accurate for this plot.')    


            if feature=="2D , Animated & Facet Plots":
                st.header("Basic Charts")
                x_axis = st.selectbox("Choose x axis",col)
                y_axis = st.selectbox("Choose y axis",col)
                color_col=st.selectbox("Choose color col",col)
                hover_cols=st.multiselect("Do you want to hover any data" , col)
                plot_type=st.selectbox("Choose the plot type" , ['Scatter' , 'Line' , 'Bar' , 'Box' , 'Violin'])
                final_df = df.dropna(subset=[color_col])
                if st.button('Generate 2D Plot'):
                    if plot_type=='Scatter':
                        fig=px.scatter(final_df , x=x_axis , y=y_axis , color=color_col , hover_data=hover_cols)
                    if plot_type=='Line':
                        fig=px.line(final_df , x=x_axis , y=y_axis , color=color_col , hover_data=hover_cols)
                    if plot_type=='Box':
                        fig=px.box(final_df , x=x_axis , y=y_axis , color=color_col , hover_data=hover_cols)  
                    if plot_type=='Bar':
                        fig=px.bar(final_df , x=x_axis , y=y_axis , color=color_col , hover_data=hover_cols) 
                    if plot_type=='Violin':
                        fig=px.violin(final_df , x=x_axis , y=y_axis , color=color_col , hover_data=hover_cols)   
                    st.plotly_chart(fig)        

                if st.checkbox('Generate Animated Plots'):
                    animated_frame = st.selectbox("Choose a column for Animation", col)
                    plot_type_animated=st.selectbox("Choose the plot type" , ['Scatter' , 'Bar'])
                    new_df = final_df.dropna(subset=[animated_frame])
                    if st.button("Show Plot"):
                        if plot_type_animated=='Scatter':
                            fig=px.scatter(new_df, x=x_axis, y=y_axis, animation_frame=animated_frame, 
                               color=color_col, log_x=True)
                        if plot_type_animated=='Bar':
                            fig=px.bar(new_df, x=x_axis, y=y_axis, animation_frame=animated_frame, 
                               color=color_col, log_x=True)
                        st.plotly_chart(fig)


                if st.checkbox('Facet Plot'):
                    facet_row_col=st.selectbox('Choose Facet row' , col)
                    facet_column_col=st.selectbox('Choose Facet column' , col)    
             
                    if st.button('Plot Facet'):
                        new_df=final_df.dropna(subset=[facet_column_col , facet_row_col])

                        #Checking the length of unique values of facet row and col if greater than 3 then we will not the graph
                        temp_row=new_df[facet_row_col].value_counts()
                        row_size=temp_row.shape[0]
                        temp_col=new_df[facet_column_col].value_counts()
                        col_size=temp_col.shape[0]

                        if (row_size>3 and col_size>3):
                            st.warning('Facet Row and Columns have large number of unique values , try using different columns')
                        elif row_size>3:
                            st.warning('Facet row is not present because of high number of unique values in it , choose another row value')
                            fig=px.scatter(new_df, x=x_axis, y=y_axis, facet_col=facet_column_col,color=color_col)
                            st.plotly_chart(fig)
                        elif col_size>3:
                            st.warning('Facet column is not present because of high number of unique values in it , choose another column value')
                            fig=px.scatter(new_df, x=x_axis, y=y_axis, facet_row=facet_row_col,color=color_col)
                            st.plotly_chart(fig)
                        else:
                            fig=px.scatter(new_df, x=x_axis, y=y_axis, facet_row=facet_row_col , facet_col=facet_column_col,color=color_col)    
                            st.plotly_chart(fig)



            if feature=="Pie Charts":
                st.header("Pie Charts")
                try:
                   temp=df.describe()
                   values_col=temp.columns.to_list()
                   x_axis = st.selectbox("Choose a value",values_col)
                   y_axis = st.selectbox("Choose the Category" , col)
                   hover_cols=st.multiselect("hover any data" , col)
                   fig=px.pie(df , values=x_axis , names=y_axis , hover_data=hover_cols)
                   fig.update_traces(textposition='inside' , textinfo='percent+label')
                   if st.button("Plot Pie Chart"):
                      st.plotly_chart(fig)   
                except:
                    st.warning('Try using different columns!')   

            if feature=="Heatmaps, 3D & Ternary Plots":
                st.header("Heatmaps & 3D Plots")
                x_axis = st.selectbox("Choose x-axis", col)
                y_axis = st.selectbox("Choose y-axis" , col)
                z_axis = st.selectbox("Choose z-axis" , col)
                if st.checkbox('Plot Heatmap'):
                    fig = px.density_heatmap(df, x=x_axis, y=y_axis, z=z_axis , marginal_x="histogram", marginal_y="histogram")
                    st.plotly_chart(fig)
                if st.checkbox('Plot 3D graphs'):
                    plot_type=st.selectbox("Choose the plot type" , ['Scatter' , 'Line'])
                    new_col=df.columns.to_list()
                    new_col.insert(0 , '-')
                    color_col=st.selectbox('Choose a color col' , new_col)
                    hover_cols=st.multiselect("Do you want to hover any data" , col)
                    if plot_type=='Scatter':
                        if color_col=='-':
                            fig = px.scatter_3d(df, x=x_axis, y=y_axis, z=z_axis, hover_data=hover_cols)
                        else:
                            final_df = df.dropna(subset=[color_col])
                            fig = px.scatter_3d(final_df, x=x_axis, y=y_axis, z=z_axis, color=color_col,hover_data=hover_cols)   
                    if plot_type=='Line':
                        if color_col=='-':
                            fig = px.line_3d(df, x=x_axis, y=y_axis, z=z_axis, hover_data=hover_cols)
                        else:
                            final_df = df.dropna(subset=[color_col])
                            fig = px.line_3d(final_df, x=x_axis, y=y_axis, z=z_axis,color=color_col,hover_data=hover_cols)    
                    st.plotly_chart(fig)
                if st.checkbox("Ternary Plot"):
                    temp=df.describe()
                    values_col=temp.columns.to_list()
                    st.write("For Better Visualisation make sure the x , y & z axis are numeric take look at below columns.")
                    st.write(values_col)
                    fig = px.scatter_ternary(df, a=x_axis, b=y_axis, c=z_axis)
                    st.plotly_chart(fig)