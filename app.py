import streamlit as st

st.title("Solar Rooftop Analysis Tool")
st.write("Setup successful! Ready to build the solar analysis tool.")
uploaded_file = st.file_uploader("Upload a rooftop image (optional)", type=["png", "jpg"])
if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    st.write("Placeholder: Image uploaded. Analysis will be added here.")
