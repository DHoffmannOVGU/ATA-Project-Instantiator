import streamlit as st
import streamlit_antd_components as sac
import pandas as pd

from PIL import Image
image = Image.open('logo_ata.png')

# Initialize session state if not already initialized
if 'project_data' not in st.session_state:
    st.session_state['project_data'] = {
        "name": "",
        "Personal": {},
        "Material": {},
    }

with st.sidebar:
    st.image(image, caption='Ata Logo')
    sac.menu(items = [
        sac.SegmentedItem("Home", icon="home", href="/"),
        sac.SegmentedItem("Project Instantiation", icon="project"),
        sac.SegmentedItem("Project Status", icon="project", href="https://project-status.streamlit.app/"),
    ],
    index=1,)

st.header("Project Instantiation App")
project_name = st.text_input("Project Name")
st.session_state['project_data']["name"] = project_name


with st.expander("Upload Raw Data"):
    excel_data = st.file_uploader("Upload Excel file", type=["xlsx"])
    project_picture = st.file_uploader("Upload Project Picture", type=["png", "jpg"])



# Exchange how tabs are displayed
tabs = sac.segmented(
    items=["Operator Cost", "Material Cost"],
    index=0,
    align="center",
    size="lg",
    grow=True,
)

# Define the sections to iterate over
sections = ["Preparation", "Welding", "Machining", "Postprocessing", "Transportation"]

# Create menu items for the sections
menu_items = [sac.MenuItem(section) for section in sections]

nav_column, display_column = st.columns([1, 2])



if tabs == "Operator Cost":
# Display the menu and capture the selected section
    with nav_column:
        selected_section = sac.menu(menu_items, format_func='title', open_all=True)

    if selected_section:
        # Fetch existing values from session state, or use default values if not present
        existing_values = st.session_state['project_data']["Personal"].get(selected_section, {'Work Hours': 0, 'Hourly Rate': 0, 'Additional Costs': 0})

        with display_column:
            #derive_button = st.button("Derive from database", type="secondary", use_container_width=True, key=f"derive-button-{selected_section}")
            work_hours = st.number_input(f"Work hours ({selected_section})", value=existing_values['Work Hours'])
            hourly_rate = st.number_input(f"Hourly rate ({selected_section})", value=existing_values['Hourly Rate'])
            additional_costs = st.number_input(f"Additional costs ({selected_section})", value=existing_values['Additional Costs'])

            # Update session state
            st.session_state['project_data']["Personal"][selected_section] = {
                'Work Hours': work_hours,
                'Hourly Rate': hourly_rate,
                'Additional Costs': additional_costs
            }

    st.button("Confirm and upload to database", type="primary", use_container_width=True)

elif tabs == "Material Cost":
    # Initialize the DataFrame for Material Costs
    df = pd.DataFrame(
        index=["0 – 80mm", "80 – 170mm", "Profile, Rohre etc.", "Schrauben, Schild", "Zuschlag"],
        columns=["Calculated Weight", "Delivery Weight", "Price", "Price per kg"]
    )

    # Use the Streamlit data editor to edit the DataFrame
    edited_df = st.data_editor(df)

    # Update session state
    st.session_state['project_data']["Material"] = edited_df.to_dict(orient="index")

# Display the dictionary for debugging
st.write("Debugging Dictionary:")
st.write(st.session_state['project_data'])
