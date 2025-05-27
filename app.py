import streamlit as st
from PIL import Image
import os
from dotenv import load_dotenv
import requests
import base64
from io import BytesIO
import json

# Load environment variables
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Placeholder for AI image analysis (fallback)
def analyze_image_placeholder():
    return {
        "area_m2": 100,
        "orientation_deg": 180,
        "shading_percent": 10,
        "obstructions": ["chimney"]
    }

# OpenRouter API image analysis
def analyze_image(image=None):
    if image is None:
        return analyze_image_placeholder()
    
    try:
        # Convert PIL image to base64
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        # Call OpenRouter API
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "anthropic/claude-3-opus",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Analyze this rooftop image for solar potential. Return area (m²), orientation (degrees), shading (%), and obstructions in JSON format."
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{img_str}"}
                        }
                    ]
                }
            ]
        }
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            # Parse JSON response
            try:
                parsed_result = json.loads(content)
                # Validate required fields
                required = ["area_m2", "orientation_deg", "shading_percent", "obstructions"]
                if all(key in parsed_result for key in required):
                    return parsed_result
                else:
                    st.warning("API response missing required fields. Using placeholder data.")
                    return analyze_image_placeholder()
            except json.JSONDecodeError:
                st.warning("Invalid JSON from API. Using placeholder data.")
                return analyze_image_placeholder()
        else:
            st.error(f"API error: {response.text}")
            return analyze_image_placeholder()
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        return analyze_image_placeholder()

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
uploaded_file = st.file_uploader("Upload satellite image of rooftop", type=["png", "jpg", "jpeg"])

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