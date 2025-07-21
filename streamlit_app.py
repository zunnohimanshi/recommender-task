import streamlit as st
import requests
import json

st.title("Unified Data Submission")

# Tabs for 3 forms
tab1, tab2, tab3 = st.tabs(["Career", "Contact", "Book Demo"])

API_URL = "http://127.0.0.1:8000/submit/"


with tab1:
    st.subheader("Career Application")
    with st.form("career_form"):
        fullName = st.text_input("Full Name")
        email = st.text_input("Email")
        countryCode = st.text_input("Country Code", value="IN")
        number = st.text_input("Phone Number")
        linkedIn = st.text_input("LinkedIn URL")
        currentLocation = st.text_input("Current Location")
        job = st.text_input("Job Title")
        jobType = st.selectbox("Job Type", ["Full-Time", "Part-Time", "Internship", "Contract"])

        submitted = st.form_submit_button("Submit Career")
        if submitted:
            payload = {
                "data": {
                    "career": {
                        "fullName": fullName,
                        "email": email,
                        "phone": {"countryCode": countryCode, "number": number},
                        "linkedIn": linkedIn,
                        "currentLocation": currentLocation,
                        "job": job,
                        "jobType": jobType
                    },
                    "contact": {
                        "fullName": "Dummy",
                        "email": "dummy@example.com",
                        "phone": {"countryCode": "IN", "number": "9999999999"},
                        "projectName": "dummy",
                        "services": "Web Development",
                        "message": "dummy"
                    },
                    "bookDemo": {
                        "fullName": "Dummy",
                        "email": "dummy@example.com",
                        "phone": "9999999999",
                        "companyName": "dummy",
                        "jobTitle": "dummy",
                        "industry": "SaaS",
                        "members": "1-10"
                    }
                }
            }
            response = requests.post(API_URL, json=payload)
            st.write("Raw response:", response.text)
            st.success(response.json().get("message", "Submitted!"))


with tab2:
    st.subheader("Contact Inquiry")
    with st.form("contact_form"):
        fullName = st.text_input("Name")
        email = st.text_input("Email")
        countryCode = st.text_input("Country Code", value="+91")
        number = st.text_input("Phone Number")
        projectName = st.text_input("Project Name")
        services = st.selectbox("Service", ["Web Development", "SEO", "App Development", "Marketing"])
        message = st.text_area("Message")

        submitted = st.form_submit_button("Submit Contact")
        if submitted:
            payload = {
                "data": {
                    "career": {
                        "fullName": "Dummy",
                        "email": "dummy@example.com",
                        "phone": {"countryCode": "IN", "number": "9999999999"},
                        "linkedIn": "https://dummy.com",
                        "currentLocation": "dummy",
                        "job": "dummy",
                        "jobType": "Full-Time"
                    },
                    "contact": {
                        "fullName": fullName,
                        "email": email,
                        "phone": {"countryCode": countryCode, "number": number},
                        "projectName": projectName,
                        "services": services,
                        "message": message
                    },
                    "bookDemo": {
                        "fullName": "Dummy",
                        "email": "dummy@example.com",
                        "phone": "9999999999",
                        "companyName": "dummy",
                        "jobTitle": "dummy",
                        "industry": "SaaS",
                        "members": "1-10"
                    }
                }
            }
            response = requests.post(API_URL, json=payload)
            st.success(response.json().get("message", "Submitted!"))


with tab3:
    st.subheader("Book a Demo")
    with st.form("demo_form"):
        fullName = st.text_input("Your Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        companyName = st.text_input("Company Name")
        jobTitle = st.text_input("Your Role")
        industry = st.selectbox("Industry", ["SaaS", "EdTech", "Finance", "Healthcare"])
        members = st.selectbox("Team Size", ["1-10", "11-50", "51-200", "201-500", "500+"])

        submitted = st.form_submit_button("Submit Demo Request")
        if submitted:
            payload = {
                "data": {
                    "career": {
                        "fullName": "Dummy",
                        "email": "dummy@example.com",
                        "phone": {"countryCode": "IN", "number": "9999999999"},
                        "linkedIn": "https://dummy.com",
                        "currentLocation": "dummy",
                        "job": "dummy",
                        "jobType": "Full-Time"
                    },
                    "contact": {
                        "fullName": "Dummy",
                        "email": "dummy@example.com",
                        "phone": {"countryCode": "IN", "number": "9999999999"},
                        "projectName": "dummy",
                        "services": "Web Development",
                        "message": "dummy"
                    },
                    "bookDemo": {
                        "fullName": fullName,
                        "email": email,
                        "phone": phone,
                        "companyName": companyName,
                        "jobTitle": jobTitle,
                        "industry": industry,
                        "members": members
                    }
                }
            }
            response = requests.post(API_URL, json=payload)
            st.success(response.json().get("message", "Submitted!"))
