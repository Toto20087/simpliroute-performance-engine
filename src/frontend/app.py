import streamlit as st
import requests
import json
import time
import pandas as pd
import pydeck as pdk

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
    # Default Input (New Structure with Explicit Depot)
    default_input = {
        "depot": {
            "lat": -34.6037, 
            "lng": -58.3816, 
            "address": "Obelisco (Depot)"
        },
        "stops": [
            {"lat": -34.5828, "lng": -58.4319, "address": "Plaza Italia, Palermo"},
            {"lat": -34.6177, "lng": -58.3685, "address": "Puerto Madero, CABA"},
            {"lat": -34.6358, "lng": -58.3654, "address": "La Boca, CABA"}
        ]
    }
    
    input_text = st.text_area("JSON Input", value=json.dumps(default_input, indent=2), height=250)
    
    if st.button("🚀 Optimize Route", type="primary"):
        try:
            input_data = json.loads(input_text)
            
            # Logic to handle both Legacy (List) and New (Dict) formats
            if isinstance(input_data, list):
                payload = {"stops": input_data}
                stops = input_data
            elif isinstance(input_data, dict):
                payload = input_data
                stops = input_data.get("stops", [])
                
                # Critical: Add depot to 'stops' list so it appears in the visualization
                # and in the coordinate lookup map (addr_to_coords)
                if "depot" in input_data and input_data["depot"]:
                     stops = [input_data["depot"]] + stops
            else:
                st.error("Invalid JSON structure. Must be a List or a Dict.")
                st.stop()
            
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
                    metric_col1, metric_col2, metric_col3 = st.columns(3)
                    metric_col1.metric("Total Distance", f"{data['total_distance_km']} km")
                    metric_col2.metric("Est. Travel Time", f"{data['estimated_travel_time_minutes']} min")
                    metric_col3.metric("Calc Time", f"{data['execution_time_seconds']:.4f} s")
                    
                    st.write("**Optimized Sequence:**")
                    for i, addr in enumerate(data['optimized_order'], 1):
                        st.write(f"{i}. {addr}")
                        
                # Map
                st.subheader("3. Visualization (3D)")
                
                # Prepare PyDeck Data
                # Map optimized list back to coordinates for the line path
                addr_to_coords = {p["address"]: [p["lng"], p["lat"]] for p in stops}
                
                path_data = []
                point_data = []
                
                for addr in data['optimized_order']:
                    if addr in addr_to_coords:
                        coords = addr_to_coords[addr] # [lng, lat]
                        path_data.append(coords)
                        point_data.append({"coordinates": coords, "address": addr})
                
                # 1. Path Layer (Red Line)
                layer_path = pdk.Layer(
                    "PathLayer",
                    data=[{"path": path_data}],
                    get_path="path",
                    get_color=[255, 0, 0], 
                    width_scale=20,
                    width_min_pixels=3,
                    pickable=True
                )
                
                # 2. Scatter Layer (Blue Dots)
                layer_points = pdk.Layer(
                    "ScatterplotLayer",
                    data=point_data,
                    get_position="coordinates",
                    get_color=[0, 128, 255],
                    get_radius=200,
                    pickable=True
                )
                
                # View State
                view_state = pdk.ViewState(
                    latitude=stops[0]["lat"],
                    longitude=stops[0]["lng"],
                    zoom=12,
                    pitch=45
                )
                
                r = pdk.Deck(
                    layers=[layer_path, layer_points],
                    initial_view_state=view_state,
                    tooltip={"text": "{address}"}
                )
                st.pydeck_chart(r)
                
                with st.expander("View Raw Protocol Response"):
                    st.json(data)
                    
            else:
                st.error(f"Error calling API: {response.text}")
                
        except json.JSONDecodeError:
            st.error("Invalid JSON format. Please check your input.")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to backend. Is uvicorn running? Try: `uvicorn src.api.main:app --reload`")
