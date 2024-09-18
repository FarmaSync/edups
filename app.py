import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# -----------------------------------
# Streamlit Page Configuration
# -----------------------------------

# Set the page layout to 'wide' to utilize the full width of the browser
st.set_page_config(
    page_title="EHR Medications Formulary Database Demo",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------
# Database Connection Setup
# -----------------------------------

# Define the path to your SQLite database
DATABASE_URL = "sqlite:///ehr_medications.db"

# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# -----------------------------------
# Function Definitions
# -----------------------------------

def search_prescribing_product():
    st.header("Search Prescribing Products and View Associated Brands")
    try:
        # Fetch all unique Prescribing Products
        query = "SELECT DISTINCT PrescribingProduct FROM prescribing_products ORDER BY PrescribingProduct ASC"
        prescribing_products = pd.read_sql(query, engine)

        # Debug: Show the number of prescribing products fetched
        st.markdown(f"**Total Prescribing Products Found:** {len(prescribing_products)}")

        prescribing_product_list = prescribing_products['PrescribingProduct'].dropna().unique().tolist()

        # Search field for user to input keywords
        search_query = st.text_input("Enter Prescribing Product Name:", "")

        if search_query:
            # Filter prescribing products based on the search query (case-insensitive)
            filtered_products = [
                product.strip() for product in prescribing_product_list
                if search_query.lower() in product.lower()
            ]

            # Debug: Show filtered products
            #st.markdown(f"**Filtered Products:** {filtered_products if filtered_products else 'None'}")

            if filtered_products:
                # Dropdown to select from filtered prescribing products
                selected_product = st.selectbox("Select a Prescribing Product:", filtered_products)

                # Fetch Brands associated with the selected Prescribing Product
                brand_query = """
                    SELECT b.BrandName
                    FROM brands b
                    JOIN prescribing_products pp ON b.ProductID = pp.ProductID
                    WHERE pp.PrescribingProduct = :product
                    ORDER BY b.BrandName ASC
                """
                brands = pd.read_sql(brand_query, engine, params={"product": selected_product})

                # Debug: Show the number of brands fetched
                st.markdown(f"**Total Brands Found for '{selected_product}':** {len(brands)}")

                if not brands.empty:
                    st.subheader(f"Brands under '{selected_product}':")
                    st.dataframe(brands.reset_index(drop=True), use_container_width=True)
                else:
                    st.warning(f"No brands found for the prescribing product '{selected_product}'.")
            else:
                st.warning("No prescribing products match your search query.")
        else:
            st.info("Please enter a keyword to search for prescribing products.")
    except SQLAlchemyError as e:
        st.error(f"An error occurred while fetching data: {e}")

def show_active_ingredients():
    st.header("Active Ingredients")
    try:
        query = "SELECT * FROM active_ingredients"
        active_ingredients = pd.read_sql(query, engine)
        # Debug: Show the number of active ingredients fetched
        st.markdown(f"**Total active ingredients Found:** {len(active_ingredients)}")
        st.dataframe(active_ingredients, use_container_width=True)
    except SQLAlchemyError as e:
        st.error(f"Error fetching Active Ingredients: {e}")

def show_dosage_forms():
    st.header("Dosage Forms")
    try:
        query = "SELECT * FROM dosage_forms"
        dosage_forms = pd.read_sql(query, engine)
            # Debug: Show the number of dosage forms fetched
        st.markdown(f"**Total dosage forms Found:** {len(dosage_forms)}")
        st.dataframe(dosage_forms, use_container_width=True)
    except SQLAlchemyError as e:
        st.error(f"Error fetching Dosage Forms: {e}")

def show_prescribing_products():
    st.header("Prescribing Products")
    try:
        query = """SELECT * FROM prescribing_products"""
        prescribing_products = pd.read_sql(query, engine)
        # Debug: Show the number of prescribing products fetched
        st.markdown(f"**Total Prescribing Products Found:** {len(prescribing_products)}")
        st.dataframe(prescribing_products, use_container_width=True)
    except SQLAlchemyError as e:
        st.error(f"Error fetching Prescribing Products: {e}")

def show_brands():
    st.header("Brands")
    try:
        query = """
        SELECT * FROM brands b
        """
        brands = pd.read_sql(query, engine)
        # Debug: Show the number of brands fetched
        st.markdown(f"**Total brands Found:** {len(brands)}")
        st.dataframe(brands, use_container_width=True)
    except SQLAlchemyError as e:
        st.error(f"Error fetching Brands: {e}")

# -----------------------------------
# Streamlit App Layout
# -----------------------------------

st.title("EHR Medications Formulary Database Demo")

# -----------------------------------
# Navigation Logic using Radio Buttons
# -----------------------------------
st.sidebar.header("Menu")
menu_options = [
    "Search Prescribing Product",
    "Prescribing Products",
    "Brands",
    "Active Ingredients",
    "Dosage Forms"
]
selected_page = st.sidebar.radio("Select a Page", menu_options)

# Display the selected page
if selected_page == "Search Prescribing Product":
    search_prescribing_product()
elif selected_page == "Prescribing Products":
    show_prescribing_products()
elif selected_page == "Brands":
    show_brands()
elif selected_page == "Active Ingredients":
    show_active_ingredients()
elif selected_page == "Dosage Forms":
    show_dosage_forms()
