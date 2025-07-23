import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="Candidate Search Dashboard", layout="wide")

# === Load CSV Data ===
@st.cache_data
def load_data():
    return pd.read_csv("1_candidates.csv")

df = load_data()

# === Sidebar Filters ===
st.sidebar.header("🔍 Search Filters")

# Required Role field
role = st.sidebar.text_input("Role (required)", placeholder="e.g., Data Entry")

# Optional filters
name = st.sidebar.text_input("Name (optional)", placeholder="e.g., Tushar")
location = st.sidebar.text_input("Location (optional)", placeholder="e.g., Surat")

# === Filter Logic ===
filtered_df = df[df["Job Type"].str.contains(role, case=False, na=False)]

if name:
    filtered_df = filtered_df[filtered_df["Name"].str.contains(name, case=False, na=False)]

if location:
    filtered_df = filtered_df[filtered_df["City"].str.contains(location, case=False, na=False)]

# === Pagination Setup ===
results_per_page = 10
total_results = len(filtered_df)
total_pages = max(1, math.ceil(total_results / results_per_page))

# Page selector at the end
st.markdown(f"### Showing {total_results} result(s) for role: **{role}**")

# Temporary placeholder for page (will move control to end)
page = st.session_state.get("current_page", 1)
start = (page - 1) * results_per_page
end = start + results_per_page

# === Display Each Candidate ===
for idx, row in filtered_df.iloc[start:end].iterrows():
    with st.container():
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"""
                **Name:** {row.get('Name', 'N/A')}  
                **Role:** {row.get('Job Type', 'N/A')}  
                **Location:** {row.get('City', 'N/A')}  
                **Mobile.No:** {row.get('Contact', 'N/A')}  
                **Experience:** {row.get('Experience', 'N/A')}
            """)
        with col2:
            # Resume button
            resume_link = row.get("Resume") or row.get("resume_url") or ""
            if pd.notna(resume_link) and resume_link.strip() != "":
                resume_button_key = f"resume_btn_{idx}"
                if st.button("📄 Open Resume", key=resume_button_key):
                    js = f"window.open('{resume_link}')"
                    st.components.v1.html(f"<script>{js}</script>", height=0)
            else:
                st.write("❌ No Resume")

            # WhatsApp button logic
            mobile = str(row.get("Contact", "")).strip().replace(" ", "").replace("+91", "").replace("-", "")
            if pd.notna(mobile) and mobile.isdigit() and len(mobile) == 10:
                whatsapp_url = f"https://web.whatsapp.com/send?phone=91{mobile}"
                whatsapp_button_key = f"whatsapp_btn_{idx}"
                if st.button("💬 WhatsApp", key=whatsapp_button_key):
                    js = f"window.open('{whatsapp_url}')"
                    st.components.v1.html(f"<script>{js}</script>", height=0)
            else:
                st.write("❌ No WhatsApp Number")

        st.markdown("---")

# === Pagination Control at Bottom ===
st.markdown("### 🔁 Change Page")
new_page = st.number_input("Go to Page", min_value=1, max_value=total_pages, value=page, step=1)
st.session_state.current_page = new_page

# === Footer ===
st.markdown("Made with ❤️ using Streamlit")
