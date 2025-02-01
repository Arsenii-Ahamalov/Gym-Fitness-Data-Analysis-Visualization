import streamlit as st
import nbformat
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

st.set_page_config(layout="wide", page_title="📊 Gym Fitness Data Dashboard")

st.title("📊 Gym Fitness Data Dashboard")

st.markdown(
    """
    🏋️ **About the Data**
    This dashboard visualizes data from a **gym fitness dataset**.
    The data includes:
    - **Key physiological metrics** (BMP, BMI, fat percentage).
    - **Workout details** (session duration, calories burned).
    - **Demographics & experience levels** (age, gender, experience level).
    """
)

NOTEBOOK_PATH = "gym_analyze.ipynb"

def execute_notebook(notebook_path):
    """Executes a Jupyter Notebook and returns only plots (no tables)."""
    with open(notebook_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    exec_globals = {"st": st, "plt": plt, "pd": pd, "np": np}
    plots = []

    for cell in nb.cells:
        if cell.cell_type == "code":
            try:
                cell_code = cell.source

                # Ensure display is not executed in a notebook environment.
                cell_code = cell_code.replace("display(", "# Removed display(")

                exec(cell_code, exec_globals)

                # Check if the figure is generated
                fig = plt.gcf()
                if fig and fig.get_axes():
                    plots.append(fig)  # Add the plot once
                    plt.close(fig)

            except Exception as e:
                st.error(f"Error in cell execution: {e}")

    return plots

extracted_plots = execute_notebook(NOTEBOOK_PATH)

st.subheader("📈 Fitness Data Visualizations")

if extracted_plots:
    # Only one set of columns, no doubling of plots
    for fig in extracted_plots:
        st.pyplot(fig)  # Display each plot once
else:
    st.warning("No plots were found in the notebook.")

st.success("Dashboard loaded successfully! 🚀")

