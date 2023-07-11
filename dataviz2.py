import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('2003_2017_waste.csv')
df = df.dropna()

# Set Streamlit app title and layout
st.set_page_config(page_title="Waste Management Analysis", layout="wide")

# Define CSS style
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to bottom, #373232, #69CCF7);
    }
    
    .block-container {
        margin-top: 60px;
        padding: 30px;
        background-color: #545454;
        border-radius: 10px;
        max-width: 55rem;
    }
    
    .css-1w3yi3r label {
        font-size: 18px !important;
    }
    
    .css-hi6a2p p {
        font-size: 24px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar with chart selection
chart_type = st.sidebar.selectbox("Navigate", ['Home', 'Line Chart', 'Bar Chart', 'Stacked Bar Chart', 'Heatmap'])

# Home
if chart_type == 'Home':
    st.title("SINGAPORE WASTE MANAGEMENT ANALYSIS")
    st.subheader("Problem Statement")
    st.write("The dataset attempts to address the issue of waste management in Singapore. Despite Singapore's well-developed waste management system, there are continuous worries about garbage generation, recycling rates, and sustainability. Therefore, the concern of this issue is that there is a lack of efficient resource allocation in waste management. If this issue continued, there will be increasing in environmental pollution as it may result in inadequate waste collection and disposal infrastructure.")
    st.subheader("Data Description")
    st.write("The Singapore Waste Management Analysis dataset is a comprehensive compilation of information about Singapore's waste management practices and statistics. It offers useful insights into numerous areas of waste generation, disposal, recycling, and overall waste management practices used in the country. The collection contains a wide range of data acquired from a variety of sources, including government agencies, environmental organizations, and research institutes. The dataset contains information on many sorts of garbage, such as food, paper or cardboard, plastics, Construction & Demolition (C&D), and horticultural waste. It includes information of the waste disposed, total waste recycled, total waste generated, recycling rate for each type of waste.")
    st.subheader("Objectives:")
    st.write("1. Determine waste type that generates more total waste")
    st.write("2. To determine the relationship between waste type and recycling rate")
    st.write("3. To determine the relationship between recycling rate over years")

# Line Chart
elif chart_type == 'Line Chart':
    st.subheader("Line Chart")
    waste_types = df['waste_type'].unique()
    waste_type = st.sidebar.selectbox("Select Waste Type", waste_types)
    filtered_data = df[df['waste_type'] == waste_type]

    st.write("The line chart demonstrates the recycling rate over time for a specific waste type selected from the sidebar. It uses the filtered_data DataFrame to plot the recycling rate against the years. This visualization helps track the trend and changes in recycling rates for the chosen waste type.")
    # Create the line chart using Plotly Express
    fig = px.line(filtered_data, x='year', y='recycling_rate', hover_data=['recycling_rate'])
    fig.update_layout(title=f'Recycling Rate for {waste_type} Over Time', xaxis_title='Year', yaxis_title='Recycling Rate')
    st.plotly_chart(fig)

# Bar Chart
elif chart_type == 'Bar Chart':
    st.subheader("Bar Chart")
    # Filter by year
    years = df['year'].unique()
    selected_year = st.sidebar.selectbox("Select Year", years)
    df_filtered = df[df['year'] == selected_year]

    grouped_data = df_filtered.groupby('waste_type')['recycling_rate'].sum()
    sort_by = st.sidebar.selectbox("Sort By", ['None', 'Ascending', 'Descending'])
    if sort_by == 'Ascending':
        grouped_data = grouped_data.sort_values(ascending=True)
    elif sort_by == 'Descending':
        grouped_data = grouped_data.sort_values(ascending=False)

    st.write("The bar chart showcases the total waste generated by waste type in the year 2017. It utilizes the grouped_data DataFrame, which groups the data by waste type and sums the recycling rates. This bar chart allows for easy comparison of the recycling rates across different waste types, providing an overview of waste generation in 2017.")
    # Create the bar chart using Plotly Express
    fig = px.bar(grouped_data, orientation='h', labels={'value': 'Recycling Rate'})
    fig.update_layout(title=f'Total Waste Generated by Waste Type in {selected_year}')
    st.plotly_chart(fig)

# Stacked Bar Chart
elif chart_type == 'Stacked Bar Chart':
    st.subheader("Stacked Bar Chart")
    # Filter by year
    years = df['year'].unique()
    selected_year = st.sidebar.selectbox("Select Year", years)
    df_filtered = df[df['year'] == selected_year]

    grouped_data = df_filtered.groupby('waste_type')[['waste_disposed_of_tonne', 'total_waste_recycled_tonne']].sum()

    # Calculate the total waste (disposed + recycled)
    grouped_data['Total Waste'] = grouped_data['waste_disposed_of_tonne'] + grouped_data['total_waste_recycled_tonne']

    # Sort the data based on user selection
    sort_by = st.sidebar.selectbox("Sort By", ['Total Waste', 'Waste Disposed', 'Total Waste Recycled'])
    if sort_by == 'Waste Disposed':
        grouped_data = grouped_data.sort_values(by='waste_disposed_of_tonne', ascending=False)
    elif sort_by == 'Total Waste Recycled':
        grouped_data = grouped_data.sort_values(by='total_waste_recycled_tonne', ascending=False)
    else:
        grouped_data = grouped_data.sort_values(by='Total Waste', ascending=True)

    st.write("The stacked bar chart represents waste disposal and recycling quantities by waste type. By using the grouped_data DataFrame, which sums the waste disposed of and recycled for each waste type, it visualizes the relative proportions of waste disposal and recycling. Each bar is stacked to show the contribution of waste disposed of and waste recycled within each waste type. This visualization enables a comprehensive understanding of waste management practices across various waste types.")
    # Create the stacked bar chart using Plotly
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=grouped_data.index,
        x=grouped_data['waste_disposed_of_tonne'],
        name='Waste Disposed',
        orientation='h',
        marker_color='#FF6103'
    ))
    fig.add_trace(go.Bar(
        y=grouped_data.index,
        x=grouped_data['total_waste_recycled_tonne'],
        name='Waste Recycled',
        orientation='h',
        marker_color='#00BFFF'
    ))

    fig.update_layout(
        barmode='stack',
        title=f'Waste Disposal and Recycling by Waste Type in {selected_year}',
        xaxis_title='Quantity (tonne)',
        yaxis_title='Waste Type'
    )

    st.plotly_chart(fig)

# Heatmap
else:
    st.subheader("Correlation Heatmap")
    numeric_cols = df.select_dtypes(include='number').columns
    corr = df[numeric_cols].corr()

    st.write("The correlation heatmap provides an overview of the correlations between different numeric variables in the dataset. It uses the corr DataFrame, which calculates the correlation coefficients between the numeric columns of the original dataset. The heatmap is color-coded to represent the strength and direction of the correlations. It helps identify relationships between variables, highlighting which factors might be positively or negatively correlated. This visualization aids in understanding the interdependencies among different waste management variables.")
    # Create the heatmap using Seaborn and Plotly
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    ax.set_title("Correlation Heatmap")

    # Convert the Seaborn heatmap to Plotly format
    fig = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.index,
        colorscale='Viridis',
        zmin=-1,
        zmax=1
    ))

    fig.update_layout(
        title="Correlation Heatmap",
        xaxis_title="Variables",
        yaxis_title="Variables"
    )

    st.plotly_chart(fig)
