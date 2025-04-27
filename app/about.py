import streamlit as st

from forms.contact import contact_form

#st.title("About Me")


@st.dialog("Contact Me")
def show_contact_form():
    contact_form()

# HERO SECTION
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
with col1:
    st.image("./image/jpg/myPic.png", width=230)
with col2:
    st.title("Martin Amilo", anchor=False)
    st.write(
        "Senior Data Analyst"
    )
    if st.button("🤷‍♀️ Contact Me"):
        show_contact_form()

# Experience & Qualification
st.write(" ")
st.subheader("Experience & Qualifications", anchor=False)
st.write("""
    - 7 years experience extracting actionable insights from data
    - Strong hands-on experience and knowledge in Python and Excel
    - Good understanding of statistical principles and their respective applications
    - Excellent team-player and displaying a strong sense of initiative on tasks
""")

# Skills
st.write(" ")
st.subheader("Hard Skills", anchor=False)
st.write("""
    - Programming: Python (Scikit-learn, Pandas), SQL, VBA
    - Data Visualization: PowerBi, MS Excel, Plotly
    - Modeling: Logistic regression, linear regression, decision trees
    - Databases: Postgres, MongoDB, MySQL
""")


st.markdown('''
*   Application created in honor of PgD in computer Science.
*   Nnamdi Azikiwe University, Awka

*   Development of Forensic System for Cybercrimecrime Detection And Prevention

''')