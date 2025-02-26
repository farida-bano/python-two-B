import streamlit as st
from datetime import datetime

# Conversion Categories and Units
conversion_categories = {
    "Length": ["Meter to Foot", "Meter to Inch", "Meter to Mile", "Meter to Kilometer",
               "Foot to Meter", "Inch to Meter", "Mile to Meter", "Kilometer to Meter"],
    "Weight": ["Kilogram to Pound", "Pound to Kilogram", "Kilogram to Ounce", "Ounce to Kilogram"],
    "Temperature": ["Celsius to Fahrenheit", "Fahrenheit to Celsius"],
    "Time": ["Second to Minute", "Minute to Second", "Second to Hour", "Hour to Second",
             "Minute to Hour", "Hour to Minute"],
    "Volume": ["Liter to Gallon", "Gallon to Liter", "Liter to Milliliter", "Milliliter to Liter"]
}

unit_symbols = {
    "Meter": "m", "Foot": "ft", "Inch": "in", "Mile": "mi", "Kilometer": "km",
    "Kilogram": "kg", "Pound": "lb", "Ounce": "oz", "Celsius": "°C", "Fahrenheit": "°F",
    "Second": "s", "Minute": "min", "Hour": "hr", "Liter": "L", "Gallon": "gal", "Milliliter": "mL"
}

# Streamlit UI with enhanced styling
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #f0f4f8 0%, #e6eef7 100%);
        }
        .stTitle {
            color: #2c3e50;
            text-align: center;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        .stButton button {
            background: linear-gradient(145deg, #4CAF50 0%, #45a049 100%);
            color: white;
            border: none;
            padding: 12px 28px;
            font-size: 16px;
            border-radius: 12px;
            cursor: pointer;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(0,0,0,0.15);
        }
        .stSelectbox, .stNumberInput {
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
        }
        .stSelectbox:hover, .stNumberInput:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 6px rgba(0,0,0,0.12);
        }
        .history-box {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 20px;
            margin-top: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'conversion_type' not in st.session_state:
    st.session_state.conversion_type = None

# Title with improved styling
st.markdown("<h1 class='stTitle'>🚀 Advanced Unit Converter</h1>", unsafe_allow_html=True)

# Main converter container
with st.container():
    col1, col2 = st.columns([3, 1])
    with col1:
        category = st.selectbox("📦 Category", list(conversion_categories.keys()))
    
    # Initialize or update conversion type based on category
    if st.session_state.conversion_type not in conversion_categories[category]:
        st.session_state.conversion_type = conversion_categories[category][0]

    # Conversion type selection with symbols
    conversion_type = st.selectbox(
        "🔄 Conversion Type",
        conversion_categories[category],
        index=conversion_categories[category].index(st.session_state.conversion_type),
        format_func=lambda x: f"{x.split(' to ')[0]} ({unit_symbols[x.split(' to ')[0]]}) → {x.split(' to ')[1]} ({unit_symbols[x.split(' to ')[1]]})"
    )

    # Swap units button
    if st.button("🔁 Swap Units"):
        from_unit, to_unit = conversion_type.split(' to ')
        reversed_conv = f"{to_unit} to {from_unit}"
        if reversed_conv in conversion_categories[category]:
            st.session_state.conversion_type = reversed_conv
            st.experimental_rerun()

    # Dynamic input validation
    min_value = 0.0
    if category == "Temperature":
        min_value = -273.15 if "Celsius" in conversion_type else -459.67

    value = st.number_input(
        f"📥 Enter value ({conversion_type.split(' to ')[0]} {unit_symbols[conversion_type.split(' to ')[0]]}):",
        min_value=min_value,
        format="%.4f",
        help="Enter the value you want to convert"
    )

    # Precision selection
    precision = st.slider("🎯 Precision (decimal places):", 0, 6, 4)

    # Conversion logic
    def convert_value(category, conversion_type, value):
        conversions = {
            "Length": {
                "Meter to Foot": value * 3.28084,
                "Foot to Meter": value / 3.28084,
                "Meter to Inch": value * 39.3701,
                "Inch to Meter": value / 39.3701,
                "Meter to Mile": value / 1609.34,
                "Mile to Meter": value * 1609.34,
                "Meter to Kilometer": value / 1000,
                "Kilometer to Meter": value * 1000
            },
            "Weight": {
                "Kilogram to Pound": value * 2.20462,
                "Pound to Kilogram": value / 2.20462,
                "Kilogram to Ounce": value * 35.274,
                "Ounce to Kilogram": value / 35.274
            },
            "Temperature": {
                "Celsius to Fahrenheit": (value * 9/5) + 32,
                "Fahrenheit to Celsius": (value - 32) * 5/9
            },
            "Time": {
                "Second to Minute": value / 60,
                "Minute to Second": value * 60,
                "Second to Hour": value / 3600,
                "Hour to Second": value * 3600,
                "Minute to Hour": value / 60,
                "Hour to Minute": value * 60
            },
            "Volume": {
                "Liter to Gallon": value * 0.264172,
                "Gallon to Liter": value / 0.264172,
                "Liter to Milliliter": value * 1000,
                "Milliliter to Liter": value / 1000
            }
        }
        return conversions[category].get(conversion_type, None)

    # Convert button and result display
    if st.button("✨ Convert Now!"):
        result = convert_value(category, conversion_type, value)
        if result is not None:
            from_unit, to_unit = conversion_type.split(' to ')
            history_entry = {
                "from": f"{from_unit} ({unit_symbols[from_unit]})",
                "to": f"{to_unit} ({unit_symbols[to_unit]})",
                "value": value,
                "result": round(result, precision),
                "time": datetime.now().strftime("%H:%M:%S")
            }
            st.session_state.history.insert(0, history_entry)
            if len(st.session_state.history) > 5:
                st.session_state.history.pop()
            
            st.success(f"""
                🎉 **Converted Successfully!**  
                **{value:.4f} {from_unit} ({unit_symbols[from_unit]})**  
                =  
                **{result:.{precision}f} {to_unit} ({unit_symbols[to_unit]})**
            """)
        else:
            st.error("❌ Conversion failed. Please check your inputs.")

# History section
if st.session_state.history:
    with st.expander("📚 Conversion History (Last 5)"):
        for entry in st.session_state.history:
            st.markdown(f"""
                ⏰ {entry['time']}  
                {entry['value']} {entry['from']} → **{entry['result']}** {entry['to']}
                ---
            """)

# Additional features section
st.markdown("---")
st.markdown("### 🛠️ Features Overview")
features = """
- 🌐 **Multi-Category Support**: Convert between 5 different measurement categories
- 🔄 **Bidirectional Conversion**: Swap units with a single click
- 🎯 **Adjustable Precision**: Control decimal places from 0 to 6
- 📚 **Conversion History**: Track your last 5 conversions
- 📱 **Mobile Friendly**: Responsive design works on all devices
- 🎨 **Modern UI**: Beautiful gradients and smooth animations
"""
st.markdown(features)