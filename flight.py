import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt
import plotly.express as px

# ui configuration
st.set_page_config(
    page_title='Flight App', page_icon="", layout="wide",)

# load data
@st.cache_data
def load_data():
    return pd.read_csv("flight_dataset.csv")

# ui integration
with st.spinner("loading dataset..."):
    df = load_data()

st.title("Flight Data Analysis")
st.subheader("A simple flight operations overview")

st.sidebar.title("Menu")
choice = st.sidebar.radio("Option",["View Data", "Visualize Data", "Column Analysis",'Correlation Analysis'])

if choice == 'View Data':
   st.header("View Dataset")
   st.dataframe(df)
elif choice == 'Visualize Data':
    st.header("Visualization")
    cat_cols = df.select_dtypes(include='object').columns.tolist()
    num_cols = df.select_dtypes(exclude='object').columns.tolist()
    cat_cols.remove('Airline')
    num_cols.remove('Price')
    num_cols.remove('Date')
    cat_cols.append('Price')
    cat_cols.append('Destination')

    snum_col = st.sidebar.selectbox("Select a numerical column", num_cols)
    scat_col = st.sidebar.selectbox("Select a categorical column", cat_cols)

    c1, c2 = st.columns(2)
    # visualize numerical column
    fig1 = px.histogram(df, x=snum_col, title=f"Distribution of {snum_col}")
    c1.plotly_chart(fig1)
   
    # visualize categorical column  
    fig2 = px.pie(df, names=scat_col, title=f"Distribution of {scat_col}", hole=0.3)
    c2.plotly_chart(fig2)
    fig3 = px.box(df, x=scat_col, y=snum_col, title=f"{snum_col} by {scat_col}")
    st.plotly_chart(fig3)
    fig4 = px.treemap(df, path=['Source','Price'], title=f"Flight Type Distribution")
    st.plotly_chart(fig4)
    fig5 = px.scatter(df, x=scat_col, y=snum_col)
    st.plotly_chart(fig5)

elif choice == 'Column Analysis':
    columns = df.columns.tolist()
    scol = st.sidebar.selectbox("Select a column", columns)
    if df[scol].dtype =='object':
        vc=df[scol].value_counts()
        most_common = vc.idxmax()
        c1, c2 = st.columns(2)
        # value counts
        c2.subheader("Total Data")
        c2. dataframe(vc, use_container_width=True)
        c2.metric("Most Common", most_common, int(vc[most_common]))
        fig1 = px.funnel_area(names= vc.index, values= vc.values, title=f"{scol} Funnel Area", height=600)
        c1.plotly_chart(fig1)
        fig2 = px.pie(df, names=scol, title=f"Percentage wise of {scol}", hole=0.2)
        st.plotly_chart(fig2)
        fig3 = px.bar(df, y=scol, title=f"{scol}", height= 800)
        st.plotly_chart(fig3)
        
        col_count = df[scol].value_counts()
        fig4 = px.bar(col_count, x=col_count.index, y=col_count.values, title=f"Distribution of {scol}", height= 800, log_y=True)
        st.plotly_chart(fig4)
        fig5 = px.scatter(df, x =scol, title=f"{scol}", height=500)
        st.plotly_chart(fig5)
        fig6= px.sunburst(df, path=['Source','Price'], height=400)
        st.plotly_chart(fig6)    
elif choice == 'Correlation Analysis':
    num_col = df.select_dtypes(include='number').columns.tolist()
    c1, c2 = st.columns(2)
    colx = c1.selectbox("Select Column for X axis", num_col)
    coly = c2.selectbox("Select Column for Y axis", num_col, index=1)
    fig7 = px.scatter(df, x=colx, y=coly, title=f'Correlation b/w {colx} and {coly}')
    st.plotly_chart(fig7, use_container_width=True, height=700)