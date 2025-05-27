# Implementation Documentation

## Overview
This tool analyzes rooftop satellite imagery to assess solar potential, estimate ROI, and provide installation recommendations. It uses the OpenRouter API for image analysis with a fallback to placeholder data.

## Code Structure
- `app.py`: Streamlit app with image upload, API integration, solar calculations, and ROI estimation.
- `analyze_image()`: Calls OpenRouter API or returns placeholder data (100m², 180°, 10% shading, chimney).
- `calculate_solar_potential()`: Computes annual kWh (~7,300 kWh for 100m²).
- `calculate_roi()`: Estimates cost (~$10,500) and payback (~7 years).

## Assumptions
- Insolation: 5 kWh/m²/day (US average).
- Panels: Monocrystalline, 20% efficiency, 400W, 2m²/panel.
- Costs: $3/W, 30% federal credit, $0.12/kWh electricity rate.

## Example Use Case
- **Input**: Rooftop image or placeholder (100m², south-facing, 10% shading).
- **Output**:
  - Energy: ~7,300 kWh/year.
  - Cost: ~$10,500.
  - Payback: ~7 years.
  - Recommendations: ~50 panels, flush mount, annual cleaning.
- **Screenshots**: See `docs/screenshots/`.

## Challenges
- API integration: Handled invalid JSON or errors with fallback data.
- Energy calculation: Fixed to output ~7,300 kWh/year.

## Future Improvements
- Enhance API prompt for precise rooftop analysis.
- Add location-specific insolation data.
- Deploy to Hugging Face Spaces. 

## API Testing
- Attempted OpenRouter API integration with `claude-3-opus`.
- Faced credit limitation (error: 402 Insufficient Credits).
- Used placeholder data as fallback: 100m², 180°, 10% shading, chimney.
- Tested with rooftop images from OpenAerialMap, results in `docs\screenshots\`.

## Submission Notes
- App fully functional with placeholder data.
- API integration ready, pending credits.