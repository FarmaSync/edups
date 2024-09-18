import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# -----------------------------------
# Database Connection Setup
# -----------------------------------

# Define the path to your SQLite database
DATABASE_URL = "sqlite:///ehr_medications.db"

# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# -----------------------------------
# Streamlit App Layout
# -----------------------------------

st.title("EHR Medications Formulary Database Demo")

# Sidebar for navigation
menu = ["Search brands by Prescribing Product","Active Ingredients", "Dosage Forms", "Prescribing Products", "Brands"]
choice = st.sidebar.selectbox("Menu", menu)

# -----------------------------------
# Function Definitions
# -----------------------------------

def search_prescribing_product():
    st.header("Search Prescribing Products and View Associated Brands")
    try:
        # Fetch all unique Prescribing Products
        query = "SELECT DISTINCT PrescribingProduct FROM prescribing_products ORDER BY PrescribingProduct ASC"
        prescribing_products = pd.read_sql(query, engine)
        prescribing_product_list = prescribing_products['PrescribingProduct'].tolist()
        
        # Search field for user to input keywords
        search_query = st.text_input("Enter Prescribing Product Name:", "")
        
        if search_query:
            # Filter prescribing products based on the search query (case-insensitive)
            filtered_products = [product for product in prescribing_product_list if search_query.lower() in product.lower()]
            
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
                
                if not brands.empty:
                    st.subheader(f"Brands under '{selected_product}':")
                    st.dataframe(brands.reset_index(drop=True))
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
        st.dataframe(active_ingredients)
    except SQLAlchemyError as e:
        st.error(f"Error fetching Active Ingredients: {e}")

def show_dosage_forms():
    st.header("Dosage Forms")
    try:
        query = "SELECT * FROM dosage_forms"
        dosage_forms = pd.read_sql(query, engine)
        st.dataframe(dosage_forms)
    except SQLAlchemyError as e:
        st.error(f"Error fetching Dosage Forms: {e}")

def show_prescribing_products():
    st.header("Prescribing Products")
    try:
        query = """SELECT * FROM prescribing_products"""
        
        prescribing_products = pd.read_sql(query, engine)
        #selected_product = st.selectbox("Select a Prescribing Product", prescribing_products['PrescribingProduct'])
        #product_details = prescribing_products[prescribing_products['PrescribingProduct'] == selected_product]
        #st.write(product_details)
        st.dataframe(prescribing_products)
    except SQLAlchemyError as e:
        st.error(f"Error fetching Prescribing Products: {e}")


def show_brands():
    st.header("Brands")
    try:
        query = """
        SELECT b.BrandID, b.BrandName, b.productID, pp.PrescribingProduct, pp.Strength
        FROM brands b
        JOIN prescribing_products pp ON b.ProductID = pp.ProductID
        """
        brands = pd.read_sql(query, engine)
        st.dataframe(brands)
    except SQLAlchemyError as e:
        st.error(f"Error fetching Brands: {e}")

# -----------------------------------
# Navigation Logic
# -----------------------------------
if choice == "Search brands by Prescribing Product":
    search_prescribing_product()
elif choice == "Active Ingredients":
    show_active_ingredients()
elif choice == "Dosage Forms":
    show_dosage_forms()
elif choice == "Prescribing Products":
    show_prescribing_products()
elif choice == "Brands":
    show_brands()
