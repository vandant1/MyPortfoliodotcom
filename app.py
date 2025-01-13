import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import json



#Function to setup database

# Connect to SQLite database (You'll need to set up the db manually)
def fetch_data(query):
    conn = sqlite3.connect('portfolio.db')
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Title and description
st.title("Vandan Tarde's Portfolio")
st.markdown("Welcome to my portfolio! Below you can explore my projects, skills, achievements, and more.")

# Sidebar for theme customization and layout

# Sidebar for theme customization and layout
st.sidebar.header("Customize Your Experience")

# Add more theme options
theme_color = st.sidebar.radio("Select Theme", ["Sky-Blue & Lavender", "Professional Dark", "Minimalist Light"])

if theme_color == "Sky-Blue & Lavender":
    st.markdown(
        """
        <style>
        /* Main background and text */
        .main {background-color: #F5F9FF; color: #333333; font-family: 'Arial', sans-serif;}
        
        /* Sidebar background and text */
        .sidebar .sidebar-content {background-color: #ADD8E6; color: #333333;}
        
        /* Header and sub-header styling */
        h1, h2, h3 {color: #5A5A9A; font-family: 'Arial Black', sans-serif;}
        
        /* Button styling */
        button, .stButton > button {
            background-color: #5A5A9A; color: #FFFFFF;
            border-radius: 6px;
            font-weight: bold;
        }
        button:hover {
            background-color: #4169E1; /* Slight hover effect */
        }
        </style>
        """, unsafe_allow_html=True
    )

elif theme_color == "Professional Dark":
    st.markdown(
        """
        <style>
        /* Main background and text */
        .main {background-color: #1E1E1E; color: #E0E0E0; font-family: 'Segoe UI', sans-serif;}
        
        /* Sidebar background */
        .sidebar .sidebar-content {background-color: #333333; color: #E0E0E0;}
        
        /* Header styling */
        h1, h2, h3 {color: #50C878; font-family: 'Segoe UI Bold', sans-serif;}
        
        /* Button styling */
        button, .stButton > button {
            background-color: #50C878; color: #FFFFFF;
            border-radius: 6px;
            font-weight: bold;
        }
        button:hover {
            background-color: #3CB371;
        }
        </style>
        """, unsafe_allow_html=True
    )

elif theme_color == "Minimalist Light":
    st.markdown(
        """
        <style>
        /* Main background and text */
        .main {background-color: #FFFFFF; color: #333333; font-family: 'Georgia', serif;}
        
        /* Sidebar background */
        .sidebar .sidebar-content {background-color: #F0F0F0; color: #333333;}
        
        /* Header styling */
        h1, h2, h3 {color: #2E8B57; font-family: 'Georgia Bold', serif;}
        
        /* Button styling */
        button, .stButton > button {
            background-color: #2E8B57; color: #FFFFFF;
            border-radius: 6px;
            font-weight: bold;
        }
        button:hover {
            background-color: #228B22;
        }
        </style>
        """, unsafe_allow_html=True
    )

# Additional CSS for universal styling and smooth transitions
st.markdown(
    """
    <style>
    /* Smooth transition effect for theme changes */
    .main, .sidebar .sidebar-content, h1, h2, h3, button, .stButton > button {
        transition: all 0.3s ease-in-out;
    }
    /* Universal styling for images and text content */
    img {border-radius: 8px;}
    .text-content {margin: 0 10px;}
    </style>
    """, unsafe_allow_html=True
)

# Projects Section with images and brief descriptions
st.header("Projects Showcase")
projects = fetch_data("SELECT * FROM projects ORDER BY date_added DESC")

for index, project in projects.iterrows():
    st.image(project['image_url'], width=300)
    st.subheader(project['name'])
    st.write(project['description'])
    st.markdown(f"[View Project]({project['link']})")

# Timeline-Based Project Showcase
st.header("Timeline of Achievements")
timeline = fetch_data("SELECT * FROM achievements ORDER BY date_achieved DESC")

for index, row in timeline.iterrows():
    st.write(f"**{row['title']}** - {row['date_achieved']}")
    st.write(row['description'])

# Skills Section with Radar Chart
st.header("Skills")
skills = fetch_data("SELECT * FROM skills")
skills_data = skills.to_dict(orient='records')

# Display radar chart (you can adjust this to be more dynamic)
skills_chart = {
    "Skill": [skill['skill_name'] for skill in skills_data],
    "Proficiency": [skill['proficiency'] for skill in skills_data],
}

df_skills = pd.DataFrame(skills_chart)
fig = px.bar(df_skills, x="Skill", y="Proficiency", title="Skills Radar")
st.plotly_chart(fig)

# Interactive "About Me" Section with Visual Storytelling
st.header("About Me")
st.write("I am a passionate developer with experience in a variety of fields. I specialize in building scalable solutions, and I enjoy challenges and new learning opportunities.")
st.image("C:\\Users\\Hp\\OneDrive\\Pictures\\IMG_20240721_130003.jpg", caption="My Image", width=300)

# Real-Time Project Updates and Achievements
st.header("Real-Time Updates")
project_id = st.selectbox("Select Project to Update", projects['id'])
new_update = st.text_area("Enter Update")

if st.button("Save Update"):
    conn = sqlite3.connect('portfolio.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE projects SET description = ? WHERE id = ?", (new_update, project_id))
    conn.commit()
    conn.close()
    st.success("Project updated successfully!")

# Add new project form
with st.form(key="Add Project Form"):
    st.subheader("Add a New Project")
    new_project_name = st.text_input("Project Name")
    new_project_desc = st.text_area("Project Description")
    new_project_link = st.text_input("Project Link")
    new_project_image = st.text_input("Image URL")
    
    submit_button = st.form_submit_button(label="Add Project")

    if submit_button:
        conn = sqlite3.connect('portfolio.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO projects (name, description, link, image_url, date_added) VALUES (?, ?, ?, ?, ?)",
                       (new_project_name, new_project_desc, new_project_link, new_project_image, pd.to_datetime('today')))
        conn.commit()
        conn.close()
        st.success("New project added successfully!")

# Contact Section with social media links
st.sidebar.markdown("### Contact Me")
st.sidebar.markdown("[LinkedIn](https://www.linkedin.com)")
st.sidebar.markdown("[GitHub](https://github.com)")
st.sidebar.markdown("[Twitter](https://twitter.com)")

# Real-Time Project Updates (Live Updates)
def real_time_updates():
    st.header("Live Project Updates")
    project_updates = fetch_data("SELECT * FROM project_updates ORDER BY timestamp DESC")
    for update in project_updates.iterrows():
        st.write(f"{update[1]['timestamp']} - {update[1]['update']}")
        
real_time_updates()

# Personalized Experience (Theme and Layout Customization based on User)
st.sidebar.subheader("Layout Customization")
layout_option = st.sidebar.selectbox("Select Layout", ["Compact", "Detailed"])

if layout_option == "Compact":
    st.markdown("You have selected a compact layout. Only essential information will be displayed.")
else:
    st.markdown("You have selected a detailed layout. All the project information will be displayed.")

# Achievements Section with Dynamic Content
st.header("Achievements")
achievements = fetch_data("SELECT * FROM achievements")
for index, row in achievements.iterrows():
    st.write(f"**{row['title']}** - {row['date_achieved']}")
    st.write(row['description'])

# Footer Section for credits or additional contact information
st.markdown("""
---
#### Credits
- Designed and Developed by Robin Hood.
- Thank you for visiting my portfolio!

""")

