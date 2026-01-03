import streamlit as st
import requests
import json
import time
import pandas as pd

st.set_page_config(page_title="SimpliRoute Engine", layout="wide")

st.title("🚛 SimpliRoute Micro-Engine Simulator")
st.markdown("### High-Performance Route Optimization System")

# Constants
API_URL = "http://localhost:8000/api/v1/optimize"

# Sidebar
st.sidebar.header("Configuration")
st.sidebar.info("This dashboard interacts with the FastAPI async backend.")

# Input area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Input Delivery Points")
    default_input = [
        {"lat": -34.6037, "lng": -58.3816, "address": "Obelisco, Buenos Aires"},
        {"lat": -34.5828, "lng": -58.4319, "address": "Plaza Italia, Palermo"},
        {"lat": -34.6177, "lng": -58.3685, "address": "Puerto Madero, CABA"},
        {"lat": -34.6358, "lng": -58.3654, "address": "La Boca, CABA"}
    ]
    
    input_text = st.text_area("JSON Input", value=json.dumps(default_input, indent=2), height=250)
    
    if st.button("🚀 Optimize Route", type="primary"):
        try:
            stops = json.loads(input_text)
            payload = {"stops": stops}
            
            with st.spinner("🤖 AI Engine is calculating optimal route... (Simulating processing)"):
                # Call API
                # We use session to keep connection open (simulation of robust clien)
                with requests.Session() as s:
                    response = s.post(API_URL, json=payload)
                
            if response.status_code == 200:
                data = response.json()
                
                st.success(f"Route optimized in {data['execution_time_seconds']:.4f} seconds!")
                
                with col2:
                    st.subheader("2. Optimization Results")
                    metric_col1, metric_col2 = st.columns(2)
                    metric_col1.metric("Total Distance", f"{data['total_distance_km']} km")
                    metric_col2.metric("Calculation Time", f"{data['execution_time_seconds']} s")
                    
                    st.write("**Optimized Sequence:**")
                    for i, addr in enumerate(data['optimized_order'], 1):
                        st.write(f"{i}. {addr}")
                        
                # Map
                st.subheader("3. Visualization")
                # Streamlit map expects lat/lon or lat/lng columns
                map_data = pd.DataFrame([{"lat": s["lat"], "lon": s["lng"]} for s in stops])
                st.map(map_data)
                
                with st.expander("View Raw Protocol Response"):
                    st.json(data)
                    
            else:
                st.error(f"Error calling API: {response.text}")
                
        except json.JSONDecodeError:
            st.error("Invalid JSON format. Please check your input.")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to backend. Is uvicorn running? Try: `uvicorn src.api.main:app --reload`")
