import streamlit as st
from datetime import datetime
import time
from pymongo import MongoClient

st.set_page_config(page_title="Feedbacks", layout="centered")

st.markdown(
    """
    <style>
    .title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        color: #333333;
        margin-top: 0px;
        margin-bottom: 40px;
    }
    .form-container {
        max-width: 600px;
        margin: 0 auto;
    }
    .sidebar-review {
        margin-bottom: 20px;
        border-bottom: 1px solid #ddd;
        padding-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.sidebar.image("logo.png", use_container_width=True)

st.markdown('<h1 class="title">Review Submission Form</h1>', unsafe_allow_html=True)

client = MongoClient("mongodb://localhost:27017/")
db = client["MedicalDB"]
collections = db["reviews"]

for key, default in {
    "name": "",
    "phone_number": "",
    "rating": 3,
    "review": "",
    "reset_form": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

if st.session_state.reset_form:
    st.session_state.name = ""
    st.session_state.phone_number = ""
    st.session_state.rating = 3
    st.session_state.review = ""
    st.session_state.reset_form = False

with st.container():
    with st.form(key="review_form"):
        name = st.text_input(
            "Please enter your name:", value=st.session_state.name, key="name"
        )
        phone_number = st.text_input(
            "Please enter your phone number:",
            value=st.session_state.phone_number,
            key="phone_number",
        )
        rating = st.slider("Rating", 1, 5, 3)
        review = st.text_area(
            "Please give feedback", value=st.session_state.review, key="review"
        )
        submitted = st.form_submit_button("Submit")

if submitted:
    if name and phone_number and review:
        if phone_number.isdigit() and len(phone_number) == 10:
            my_review = {
                "name": name,
                "phone_number": phone_number,
                "date": str(datetime.today().date()),
                "rating": rating,
                "review": review,
            }
            collections.insert_one(my_review)
            st.success("Thank you for the feedback")
            st.session_state.reset_form = True
            time.sleep(2)
            st.rerun()
        else:
            st.error("Phone number is invalid. It should be exactly 10 digits.")
    else:
        st.warning("Please don't leave any fields empty.")

st.sidebar.header("User reviews")
st.sidebar.markdown("---")

reviews = list(collections.find())
if reviews:
    for review in reviews:
        st.sidebar.markdown(
            f"""
            <b>Name:</b> {review['name'].title()} <br>
            <b>Phone:</b> {review['phone_number']} <br>
            <b>Date:</b> {review['date']} <br>
            <b>Rating:</b> {review['rating']} <br>
            <b>Review:</b> {review['review']}
            <hr>
            """,
            unsafe_allow_html=True,
        )
else:
    st.sidebar.info("No reviews yet.")
