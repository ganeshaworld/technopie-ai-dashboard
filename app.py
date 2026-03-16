from openai import OpenAI
import streamlit as st
import pandas as pd
import plotly.express as px

# Page settings
st.set_page_config(
    page_title="AI Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Smart Data Analytics Dashboard")
st.write("Professional BI-style dashboard for data insights")

# Sidebar
st.sidebar.header("Upload & Controls")

theme = st.sidebar.selectbox(
    "Dashboard Theme",
    ["Light","Dark"]
)

template = "plotly_dark" if theme=="Dark" else "plotly"

file = st.sidebar.file_uploader(
    "Upload CSV or Excel file",
    type=["csv","xlsx"]
)

# MAIN APP
if file:

    # Load dataset
    if file.name.endswith(".csv"):
        data = pd.read_csv(file)
    else:
        data = pd.read_excel(file)

    st.sidebar.success("Dataset Loaded")

    numeric_cols = data.select_dtypes(include=['int64','float64']).columns
    categorical_cols = data.select_dtypes(include=['object']).columns

    # Sidebar filter
    if len(categorical_cols) > 0:

        filter_col = st.sidebar.selectbox(
            "Filter Category",
            categorical_cols
        )

        filter_value = st.sidebar.multiselect(
            "Select Values",
            data[filter_col].unique(),
            default=data[filter_col].unique()
        )

        data = data[data[filter_col].isin(filter_value)]

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 Overview","📈 Charts","📄 Data","🤖 AI Insights"]
    )

    # -------------------------
    # Overview Tab
    # -------------------------
    with tab1:

        st.subheader("Key Metrics")

        col1,col2,col3,col4 = st.columns(4)

        col1.metric("Rows", len(data))
        col2.metric("Columns", len(data.columns))
        col3.metric("Missing Values", data.isnull().sum().sum())
        col4.metric("Unique Values", data.nunique().sum())

    # -------------------------
    # Charts Tab
    # -------------------------
    with tab2:

        st.subheader("Dynamic Chart Builder")

        x_axis = st.selectbox("Select X-axis", data.columns)
        y_axis = st.selectbox("Select Y-axis", numeric_cols)

        chart_type = st.selectbox(
            "Select Chart Type",
            ["Bar Chart","Line Chart","Scatter Chart"]
        )

        if chart_type == "Bar Chart":
            fig = px.bar(data, x=x_axis, y=y_axis, template=template)

        elif chart_type == "Line Chart":
            fig = px.line(data, x=x_axis, y=y_axis, template=template)

        else:
            fig = px.scatter(data, x=x_axis, y=y_axis, template=template)

        st.plotly_chart(fig, use_container_width=True)

        # Automatic Charts
        st.subheader("Automatic Insights")

        col1,col2 = st.columns(2)

        if len(categorical_cols) > 0:

            chart_col = categorical_cols[0]

            fig2 = px.pie(
                data,
                names=chart_col,
                template=template,
                title=f"{chart_col} Share"
            )

            col1.plotly_chart(fig2, use_container_width=True)

        if len(numeric_cols) > 0:

            num_col = numeric_cols[0]

            fig3 = px.histogram(
                data,
                x=num_col,
                template=template,
                title=f"{num_col} Distribution"
            )

            col2.plotly_chart(fig3, use_container_width=True)

    # -------------------------
    # Data Tab
    # -------------------------
    with tab3:

        st.subheader("Dataset Preview")

        st.dataframe(data, use_container_width=True)

        st.download_button(
            "Download Filtered Data",
            data.to_csv(index=False),
            "filtered_data.csv"
        )

    # -------------------------
    # AI Insights Tab
    # -------------------------
    with tab4:

        st.subheader("🤖 AI Data Insights")

        api_key = st.text_input(
            "Enter OpenAI API Key",
            type="password"
        )

        if st.button("Generate AI Insights"):

            if api_key == "":
                st.warning("Please enter API key")

            else:

                client = OpenAI(api_key=api_key)

                summary = data.describe().to_string()

                prompt = f"""
                Analyze this dataset summary and give simple business insights.

                Dataset summary:
                {summary}

                Explain:
                - key trends
                - unusual values
                - business insights
                """

                response = client.responses.create(
                    model="gpt-4.1-mini",
                    input=prompt
                )

                st.success("AI Insights Generated")

                st.write(response.output_text)

else:

    st.info("Upload a dataset from the sidebar to start the dashboard.")