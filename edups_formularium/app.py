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
menu = ["Active Ingredients", "Dosage Forms", "Prescribing Products", "Brands"]
choice = st.sidebar.selectbox("Menu", menu)

# -----------------------------------
# Function Definitions
# -----------------------------------

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
        query = """
        SELECT pp.ProductID, ai.ActiveIngredientName, df.DosageFormDescription, pp.PrescribingProduct, pp.Strength
        FROM prescribing_products pp
        JOIN active_ingredients ai ON pp.ActiveIngredientID = ai.IngredientID
        JOIN dosage_forms df ON pp.DosageFormID = df.DosageFormID
        """
        prescribing_products = pd.read_sql(query, engine)
        st.dataframe(prescribing_products)
    except SQLAlchemyError as e:
        st.error(f"Error fetching Prescribing Products: {e}")

def show_brands():
    st.header("Brands")
    try:
        query = """
        SELECT b.BrandID, b.BrandName, pp.PrescribingProduct, pp.Strength
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

if choice == "Active Ingredients":
    show_active_ingredients()
elif choice == "Dosage Forms":
    show_dosage_forms()
elif choice == "Prescribing Products":
    show_prescribing_products()
elif choice == "Brands":
    show_brands()
