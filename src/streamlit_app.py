import streamlit as st
import pandas as pd
import json
import sys
import os
import requests
import spacy
from geopy.geocoders import Nominatim

# Append path to import AI models
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from ai_models.scripts.main import assign_donors
from ai_models.scripts.news_report import get_summarized_news

# Load NLP Model for extracting disaster type and location
nlp = spacy.load("en_core_web_sm")

# File to persist donor data
DONOR_FILE = "donors.json"

def load_donors():
    if os.path.exists(DONOR_FILE):
        with open(DONOR_FILE, "r") as file:
            return json.load(file)
    return []

def save_donors(donors):
    with open(DONOR_FILE, "w") as file:
        json.dump(donors, file, indent=2)

donors = load_donors()

def get_coordinates(city_name):
    """Convert a city name into a dictionary with latitude and longitude."""
    geolocator = Nominatim(user_agent="disaster_relief_app")
    location = geolocator.geocode(city_name)
    if location:
        return {"latitude": location.latitude, "longitude": location.longitude}
    return None

def sanitize_donors_locations(donors_list):
    """
    Ensures that each donor's location is a dictionary.
    If a donor's location is a string, attempt to convert it using get_coordinates.
    """
    for donor in donors_list:
        loc = donor.get("location")
        if isinstance(loc, str):
            coords = get_coordinates(loc)
            if coords:
                donor["location"] = coords
    return donors_list

# Sanitize donors data to ensure location is in the correct format
donors = sanitize_donors_locations(donors)

def extract_location_from_text(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in ["GPE", "LOC"]:
            return ent.text
    return None

def get_user_location():
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        if "city" in data:
            return data["city"]
    except Exception as e:
        return None
    return None

# ----------------------------
# Custom CSS for a modern look
# ----------------------------
st.markdown("""
    <style>
    /* Set a light background */
    .reportview-container {
        background: #f7f7f7;
    }
    /* Style for sidebar */
    .sidebar .sidebar-content {
        background-image: linear-gradient(#2e7bcf, #2e7bcf);
        color: white;
    }
    /* Style for cards */
    .card {
        background-color: white;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    /* Headings */
    h1, h2, h3 {
        font-family: 'Helvetica Neue', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# Sidebar Navigation
# ----------------------------
st.sidebar.title("CrisisConnect")
st.sidebar.markdown("Disaster Relief Platform")
st.sidebar.markdown("Helping victims find the aid they need quickly!")
page = st.sidebar.radio("Navigate", ["Sign In", "Home", "Victims", "Donors", "Public Services"])
vic_text_temp = ""

# ----------------------------
# Sign In Page
# ----------------------------
if page == "Sign In":
    st.title("Sign In")
    with st.form("login_form"):
        user_type = st.radio("I am a:", ["Victim", "Donor"])
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign In")
        if submitted:
            # In a real app, authentication would occur here.
            st.success(f"Welcome {username}! You signed in as a {user_type}.")

# ----------------------------
# Home Page (News and Updates)
# ----------------------------
elif page == "Home":
    st.title("Latest Disaster News & Updates")
    st.markdown("Get personalized news updates based on your situation.")
    
    # Let the user enter details about their situation if not already provided
    user_description = st.text_area("Describe your situation for personalized news:", height=100)
    
    if st.button("Get Personalized News"):
        news_data = get_summarized_news(user_description)
        
        # Display the disaster type as a headline
        st.markdown(f"### News on {news_data['disaster_type'].capitalize()}")
        
        # Display the summary in an expander for better UX
        with st.expander("View Summary"):
            st.info(news_data['summary'])
        
        # Display the related articles as clickable cards or links
        st.markdown("#### Related Articles")
        for article in news_data['articles']:
            with st.container():
                st.markdown(f"**[{article['title']}]({article['url']})**")
                st.write(article['description'])
                st.markdown("---")


# elif page == "Home":
#     st.title("Latest Disaster News & Updates")
#     st.markdown("Stay informed with the latest news on disasters and relief efforts in your area.")
#     col1, col2 = st.columns([2, 1])
#     with col1:
#         st.image("https://images.unsplash.com/photo-1504384308090-c894fdcc538d?fit=crop&w=800&q=80",
#                  use_container_width =True)
#     with col2:
#         st.markdown("**Breaking News:** Real-time updates will appear here as soon as they are available.")
#     location = get_user_location() or st.text_input("Enter your city (e.g., New York, USA)")
#     if st.button("Get Latest News"):
#         news = get_summarized_news(vic_text_temp)
#         for item in news:
#             st.markdown(f"### Cluster {item['cluster_id']}")
#             st.write(item['summary'])
#             for article in item['articles']:
#                 st.markdown(f"[{article['title']}]({article['url']})")

# ----------------------------
# Victims Page
# ----------------------------
elif page == "Victims":
    st.title("Find Help")
    st.markdown("Describe your situation below so we can match you with the best donors nearby.")
    
    with st.form("victim_form"):
        victim_text = st.text_area("Describe your situation", height=150, help="Include details about what you need.")
        submitted_victim = st.form_submit_button("Find Donors")
    
    if submitted_victim:
        vic_text_temp = victim_text
        # Try to infer city from text; fallback to IP-based location.
        inferred_city = extract_location_from_text(victim_text) or get_user_location()
        victim_location = get_coordinates(inferred_city) if inferred_city else None
        if victim_location:
            top_donors, _ = assign_donors(victim_text, victim_location, donors, top_x=5)
            st.markdown("### Top Matching Donors")
            for donor in top_donors:
                # Display each donor in a card-like container.
                with st.container():
                    st.markdown(f"#### {donor.get('name', 'Unnamed Donor')}")
                    cols = st.columns(2)
                    with cols[0]:
                        st.write(f"**Type:** {donor.get('donor_type', 'N/A')}")
                        st.write(f"**Category:** {donor.get('donation_category', 'N/A')}")
                        st.write(f"**Offer:** {donor.get('offer_summary', '')}")
                    with cols[1]:
                        st.write(f"**Capacity Left:** {donor.get('capacity', 0)}")
                        norm_score = donor.get('normalized_score', 0)
                        st.write(f"**Match Score:** {norm_score:.2f}")
                        st.progress(norm_score)
        else:
            st.error("Could not determine your location. Please ensure your description includes your city or try another city name.")
    
    st.markdown("#### Search Donors by Category")
    search_term = st.text_input("Enter a donation category to search")
    if st.button("Search"):
        filtered_donors = [d for d in donors if search_term.lower() in d.get("donation_category", "").lower()]
        if filtered_donors:
            df = pd.DataFrame(filtered_donors)
            st.dataframe(df)
        else:
            st.info("No donors found matching that category.")

# ----------------------------
# Donors Page (Donor Registration)
# ----------------------------
elif page == "Donors":
    st.title("Register as a Donor")
    st.markdown("Join our platform to help those in need by offering your resources.")
    with st.form("donor_registration_form"):
        col1, col2 = st.columns(2)
        with col1:
            donor_name = st.text_input("Your Name")
            donor_type = st.selectbox("Type", ["Individual", "NGO", "Government"])
            donation_category = st.selectbox("Category", ["Food", "Shelter", "Medical", "Supplies", "Financial", "Transport"])
        with col2:
            capacity = st.number_input("Capacity", min_value=1, value=5)
            # Use detected location if possible, or ask for input.
            city = get_user_location() or st.text_input("Enter your city (e.g., New York, USA)")
        description = st.text_area("Describe Your Offer", help="Include details such as available resources and delivery times.")
        submitted_donor = st.form_submit_button("Register Donor")
    
    if submitted_donor:
        donor_location = get_coordinates(city)
        if donor_location:
            new_donor = {
                "id": len(donors) + 1,
                "name": donor_name,
                "donor_type": donor_type,
                "donation_category": donation_category,
                "capacity": capacity,
                "city": city,  # For display purposes.
                "location": donor_location,  # Used for geographic matching.
                "description": description
            }
            donors.append(new_donor)
            save_donors(donors)
            st.success("Donor Registered Successfully!")
        else:
            st.error("Invalid city name. Please try again.")
    
    st.markdown("### Current Donors")
    if donors:
        df = pd.DataFrame(donors)[["id", "name", "donor_type", "donation_category", "capacity", "city", "description"]]
        st.dataframe(df)
    else:
        st.info("No donors registered yet.")

# ----------------------------
# Public Services Page
# ----------------------------
elif page == "Public Services":
    st.title("Public Services Map")
    st.markdown("This section will show nearby public services on a map. [Map integration coming soon...]")
