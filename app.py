import streamlit as st
from PIL import Image
import os
from dotenv import load_dotenv

# Load environment variables (for future API integration)
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")  # Will be used later

from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
if api_key:
    print("API key loaded successfully")
else:
    print("API key not found")

# Placeholder for AI image analysis
def analyze_image(image=None):
    return {
        "area_m2": 100,  # Rooftop area in square meters
        "orientation_deg": 180,  # South-facing
        "shading_percent": 10,  # 10% shaded
        "obstructions": ["chimney"]
    }

# Calculate solar potential (kWh/year)
def calculate_solar_potential(area, orientation, shading, insolation=5):
    efficiency = 0.2  # 20% panel efficiency
    usable_area = area * (1 - shading / 100)
    annual_kwh = usable_area * insolation * 365 * efficiency
    return round(annual_kwh, 2)

# Calculate ROI
def calculate_roi(kwh, cost_per_watt=3, incentive=0.3, electricity_rate=0.12):
    system_size_w = kwh / (5 * 365) * 1000  # Convert kWh to system size
    total_cost = system_size_w * cost_per_watt
    cost_after_incentive = total_cost * (1 - incentive)
    payback_years = cost_after_incentive / (kwh * electricity_rate)
    return round(cost_after_incentive, 2), round(payback_years, 1)

# Streamlit app
st.title("Solar Rooftop Analysis Tool")

# Image upload
uploaded_file = st.file_uploader("Upload satellite image of rooftop", type=["png", "jpg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Rooftop Image", use_column_width=True)
    result = analyze_image(image)
else:
    st.write("No image uploaded. Using placeholder data: 100m², south-facing, 10% shading.")
    result = analyze_image()

# Display analysis results
st.write("### Rooftop Analysis")
st.json(result)

# Calculate and display solar potential
kwh = calculate_solar_potential(
    result["area_m2"], result["orientation_deg"], result["shading_percent"]
)
st.write(f"**Estimated Annual Energy Production**: {kwh} kWh")

# Calculate and display ROI
cost, payback = calculate_roi(kwh)
st.write(f"**Estimated Cost (after 30% incentive)**: ${cost}")
st.write(f"**Payback Period**: {payback} years")

# Installation recommendations
st.write("### Installation Recommendations")
st.write("- **Panel Type**: Monocrystalline (20% efficiency)")
st.write(f"- **Number of Panels**: ~{int(result['area_m2'] / 2)} (2m² per panel)")
st.write("- **Mounting**: Flush mount, south-facing")
st.write("- **Maintenance**: Annual cleaning, monitor via app")
st.write("- **Compliance**: Follow NEC 2020 standards, check local net metering policies")
