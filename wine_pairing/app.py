from base64 import b64encode

import streamlit as st
from backend import recommend_wine, recommend_food

# Title of the web app
st.title("Food and Wine Pairing")

# Radio buttons for selecting pairing type
pairing_type = st.radio(
    "Choose Pairing Type:",
    ("Food Pairing", "Wine Pairing")
)


# Text input for description
description = st.text_input("Description")


upload_type = st.radio(
    "Choose upload type: (Support formats: jpeg, jpg, gif, png)",
    ("Image", "URL")
)
if upload_type == "Image":
    # File uploader for attachment
    uploaded_file = st.file_uploader("Upload an attachment")
else:
    # Text input for image URL
    image_url = st.text_input("Image URL")

# Button to trigger the pairing process
if st.button("Pair"):
    if upload_type == "Image" and uploaded_file is not None:
        base64_file = b64encode(uploaded_file.read()).decode("utf-8")
        image_urls = [f"data:image/png;base64,{base64_file}"]
    elif upload_type == "URL" and image_url:
        image_urls = [image_url]
    else:
        image_urls = None
    
    # Example processing (this is where the pairing logic would go)
    if pairing_type == "Food Pairing":
        chain = recommend_food(
            query=description,
            image_urls=image_urls,
        )
    else:
        chain = recommend_wine(
            query=description,
            image_urls=image_urls,

        )

    response = chain.invoke({})
    st.write(response)
