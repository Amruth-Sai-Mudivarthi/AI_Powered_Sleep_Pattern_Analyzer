import streamlit as st
import joblib
import pandas as pd
import numpy as np
from PIL import Image
from io import BytesIO
import requests

# Configure page
st.set_page_config(
    page_title="Sleep Pattern Analyzer",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.sleepfoundation.org/',
        'About': 'Sleep Pattern Analyzer helps you understand how your lifestyle affects your sleep.'
    }
)

# Helper functions
def load_online_image(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raise error for bad status codes
        return Image.open(BytesIO(response.content))
    except Exception as e:
        st.error(f"Failed to load online image: {str(e)}")
        # Create a placeholder image
        placeholder = Image.new('RGB', (400, 200), color='#4a8cff')
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(placeholder)
        font = ImageFont.load_default()
        draw.text((50, 80), "Sleep Analysis App", fill="white")
        return placeholder

# Function definitions for data transformations 
def extract_screen_time(value):
    if value == '0-1 hrs':
        return 0.5
    elif value == '1-2 hrs':
        return 1.5
    elif value == '2-3 hrs':
        return 2.5
    elif value == '3-4 hrs':
        return 3.5
    elif value == '4-5 hrs':
        return 4.5
    else:  # 'more than 5'
        return 5.5

meal_mapping = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'more than 5': 6
}

exercise_mapping = {
    'no': 0,
    'sometimes': 0.5,
    'yes': 1
}

# Replace with your online image URLs
sleep_img_url = "https://ysm-res.cloudinary.com/image/upload/c_limit,f_auto,h_630,q_auto,w_1200/v1/yms/prod/5d491542-079c-4d25-bfeb-2364229534f7"
logo_img_url = "https://img.freepik.com/premium-vector/sleeping-sticker-logo-icon-vector-pillow-sleep-image-person-having-dreamful-slumber-bed-pillow-with-some-sleeping-sound-rest-relaxation-restoration-vector-eps-10_399089-1071.jpg"

# Load images
sleep_img = load_online_image(sleep_img_url)
logo_img = load_online_image(logo_img_url)

@st.cache_resource
def load_model():
    model = joblib.load('sleep_model.pkl')
    preprocessor = joblib.load('preprocessor.pkl')
    return model, preprocessor

try:
    model, preprocessor = load_model()
    model_loaded = True
except Exception as e:
    st.warning("⚠️ Model files not found. Running in demo mode.")
    model_loaded = False

# Custom CSS with enhanced styling
st.markdown("""
<style>
    /* Main Theme */
    :root {
        --primary: #3a86ff;
        --primary-light: #83b7ff;
        --secondary: #6c757d;
        --success: #28a745;
        --warning: #ffc107;
        --danger: #dc3545;
        --light: #f8f9fa;
        --dark: #343a40;
    }
    
    /* Page Layout */
    .main {
        background-color: #f8f9fa;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Header Styling */
    h1, h2, h3 {
        color: white !important;  /* Change from #2b5797 to black */
        font-weight: 600;
    }
 p, li, div {
        color: aqua;
    }
    
    /* Form Elements */
    .stButton>button {
        background-color: var(--primary);
        color: white;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: var(--primary-light);
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }
    
    .stSelectbox, .stNumberInput {
        border-radius: 8px;
    }
    
    /* Cards */
    .card {
        background-color: gray;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin: 15px 0;
        border-left: 5px solid var(--primary);
    }
    
    .info-card {
        background-color: #339933;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #3a86ff;
    }
    
    .warning-card {
        background-color: #fff8e1;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #ffc107;
    }
    
    .success-card {
        background-color: #e8f5e9;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #28a745;
    }
    
    .danger-card {
        background-color: #ffebee;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #dc3545;
    }
    
    /* Recommendation Cards */
    .recommendation-container {
        display: flex;
        flex-wrap: wrap;
        gap: 15px;
        margin-top: 20px;
    }
    
    .recommendation-card {
        background-color: #339933;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        flex: 1;
        min-width: 200px;
        border-top: 5px solid var(--primary);
        transition: transform 0.3s ease;
    }
    
    .recommendation-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }
    
    /* Progress Bars */
    .progress-container {
        margin: 20px 0;
    }
    
    .progress-bar {
        height: 10px;
        border-radius: 5px;
        background-color: #339933;
        margin-bottom: 10px;
        overflow: hidden;
    }
    
    .progress-value {
        height: 100%;
        border-radius: 5px;
        transition: width 1s ease-in-out;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    
    /* Custom Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #339933;
        border-radius: 6px 6px 0 0;
        padding: 10px 16px;
        box-shadow: 0 -2px 5px rgba(0,0,0,0.05);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #3a86ff !important;
        color: white !important;
    }
    
    /* Additional Utilities */
    .text-center {
        text-align: center;
    }
    
    .mt-4 {
        margin-top: 1.5rem;
    }
    
    .mb-4 {
        margin-bottom: 1.5rem;
    }
    
    /* Tooltip customization */
    .tooltip {
        position: relative;
        display: inline-block;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background-color: #339933;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
</style>
""", unsafe_allow_html=True)

# App header
st.markdown("""
<div style="padding: 20px; margin-bottom: 20px; border-radius: 15px; 
            background: linear-gradient(90deg, #3a86ff 0%, #83b7ff 100%); 
            box-shadow: 0 4px 12px rgba(0,0,0,0.15); display: flex; align-items: center;">
    <div style="margin-right: 20px;">
        <img src="https://img.freepik.com/premium-vector/sleeping-sticker-logo-icon-vector-pillow-sleep-image-person-having-dreamful-slumber-bed-pillow-with-some-sleeping-sound-rest-relaxation-restoration-vector-eps-10_399089-1071.jpg" width="80px" style="border-radius: 50%; background: white; padding: 5px;">
    </div>
    <div>
        <h1 style="color: white; margin: 0; padding: 0;">Sleep Pattern Analyzer</h1>
        <p style="color: white; margin: 0; padding: 0;">Analyze your habits and improve your sleep</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Main content area
tab1, tab2, tab3 = st.tabs(["💤 Sleep Prediction", "📊 Track Progress", "📚 Sleep Resources"])

with tab1:
    # Layout with columns
    left_col, right_col = st.columns([1, 2])
    
    with left_col:
        st.image(sleep_img, use_column_width=True)
        
        # Info box
        st.markdown("""
        <div class="info-card">
            <h3 style="margin-top:0;">About Sleep Quality</h3>
            <p style="color: black;">Good sleep is essential for your physical health and emotional wellbeing. This tool helps you understand how lifestyle factors affect your sleep duration and quality.</p>
            <p style="color: black;"><strong>Recommended sleep hours:</strong> 7-9 hours for adults</p>
        </div>
        """, unsafe_allow_html=True)
    
    with right_col:
        st.markdown("### Your Sleep Profile")
        
        with st.form("sleep_form"):
            # Create tabbed sections in the form
            form_tab1, form_tab2, form_tab3 = st.tabs(["😀 Personal", "🏠 Environment", "🍽️ Lifestyle"])
            
            with form_tab1:
                age = st.number_input('Age', min_value=18, max_value=100, value=30, help="Your current age")
                gender = st.selectbox('Gender', ['Male', 'Female', 'Other'], help="Your gender identity")
                physical_illness = st.radio('Do you have any physical illness?', 
                                        ['no', 'yes'], 
                                        horizontal=True, 
                                        help="Select 'yes' if you have any chronic conditions")
            
            with form_tab2:
                sleep_direction = st.selectbox('Bed orientation', 
                                          ['north', 'south', 'east', 'west'], 
                                          help="Direction your head points when sleeping")
                
                screen_time = st.slider('Screen time before bed (hours)', 
                                     min_value=0.0, max_value=5.0, value=2.0, step=0.5, 
                                     help="Hours spent on electronic devices before sleeping")
                
                # Convert slider value to categories for model prediction
                screen_time_category = '0-1 hrs'
                if screen_time <= 1:
                    screen_time_category = '0-1 hrs'
                elif screen_time <= 2:
                    screen_time_category = '1-2 hrs'
                elif screen_time <= 3:
                    screen_time_category = '2-3 hrs'
                elif screen_time <= 4:
                    screen_time_category = '3-4 hrs'
                elif screen_time <= 5:
                    screen_time_category = '4-5 hrs'
                else:
                    screen_time_category = 'more than 5'
                
                bluelight = st.toggle('Use blue light filter on devices', 
                                   help="Do you use blue light filters on electronic devices?")
                bluelight_val = 'yes' if bluelight else 'no'
            
            with form_tab3:
                meals = st.radio('Meals per day', 
                              ['one', 'two', 'three', 'four', 'five', 'more than 5'], 
                              horizontal=True,
                              help="How many meals do you typically eat daily?")
                
                exercise_options = {
                    'no': 'I rarely exercise',
                    'sometimes': 'I exercise 1-2 times weekly',
                    'yes': 'I exercise 3+ times weekly'
                }
                exercise = st.select_slider(
                    'Exercise frequency', 
                    options=list(exercise_options.keys()),
                    format_func=lambda x: exercise_options[x],
                    help="Your typical exercise frequency"
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    smoke_drink = st.radio('Do you smoke or drink alcohol?', 
                                       ['no', 'yes'], 
                                       help="Regular consumption of alcohol or tobacco")
                
                with col2:
                    beverage = st.selectbox('Evening beverage', 
                                         ['none of the above', 'Tea', 'Coffee', 'Tea and Coffee both'], 
                                         help="What do you typically drink in the evening?")
            
            # Submit button with improved styling
            submitted = st.form_submit_button(
                "✨ Predict My Sleep Quality", 
                type="primary",
                use_container_width=True,
                help="Click to get your sleep prediction"
            )

    # Prediction and results
    if submitted:
        with st.spinner("Analyzing your sleep factors..."):
            # Progress bar animation
            import time
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            
            # Simulate model prediction if model not loaded
            if not model_loaded:
                # Demo prediction based on inputs
                if screen_time > 3 or smoke_drink == 'yes':
                    prediction = 5.5 + (0.5 if bluelight_val == 'yes' else 0) + (0.5 if exercise == 'yes' else 0)
                elif exercise == 'yes' and screen_time < 2:
                    prediction = 7.5
                else:
                    prediction = 6.5
            else:
                # Real prediction with model
                input_data = pd.DataFrame({
                    'Age': [age],
                    'Gender': [gender],
                    'meals/day': [meals],
                    'physical illness': [physical_illness],
                    'screen time': [screen_time_category],
                    'bluelight filter': [bluelight_val],
                    'sleep direction': [sleep_direction],
                    'exercise': [exercise],
                    'smoke/drink': [smoke_drink],
                    'beverage': [beverage],
                    'screen_time_numeric': [0],
                    'meals_numeric': [0],
                    'exercise_numeric': [0],
                    'screen_exercise_interaction': [0],
                    'meals_screen_interaction': [0]
                })
                
                # Apply transformations
                input_data['screen_time_numeric'] = input_data['screen time'].apply(lambda x: extract_screen_time(x))
                input_data['meals_numeric'] = input_data['meals/day'].map(meal_mapping)
                input_data['physical illness'] = input_data['physical illness'].map({'yes': 1, 'no': 0})
                input_data['bluelight filter'] = input_data['bluelight filter'].map({'yes': 1, 'no': 0})
                input_data['smoke/drink'] = input_data['smoke/drink'].map({'yes': 1, 'no': 0})
                input_data['exercise_numeric'] = input_data['exercise'].map(exercise_mapping)
                input_data['screen_exercise_interaction'] = input_data['screen_time_numeric'] * input_data['exercise_numeric']
                input_data['meals_screen_interaction'] = input_data['meals_numeric'] * input_data['screen_time_numeric']
                
                features_for_prediction = input_data[['Age', 'Gender', 'meals_numeric', 'physical illness', 'screen_time_numeric',
                                                'bluelight filter', 'sleep direction', 'exercise_numeric', 'smoke/drink',
                                                'beverage', 'screen_exercise_interaction', 'meals_screen_interaction']]
                
                prediction = model.predict(features_for_prediction)[0]
        
        # Remove progress bar after completion
        progress_bar.empty()
        
        # Results section with enhanced UI
        st.markdown("""
        <div class="card fade-in" style="margin-top: 30px;">
            <h2 style="margin-top: 0;">🌙 Your Sleep Analysis Results</h2>
            <hr>
        """, unsafe_allow_html=True)
        
        col_res1, col_res2 = st.columns([1, 2])
        
        with col_res1:
            # Emoji indicator based on sleep quality
            emoji = "😴" if prediction >= 7 else "😐" if prediction >= 6 else "😫"
            
            st.markdown(f"""
            <div style="text-align: center; padding: 20px;">
                <div style="font-size: 60px; margin-bottom: 10px;">{emoji}</div>
                <div style="font-size: 36px; font-weight: bold; color: {'#28a745' if prediction >= 7 else '#ffc107' if prediction >= 6 else '#dc3545'};">
                    {prediction:.1f} hours
                </div>
                <div style="font-size: 18px; margin-top: 5px;">Predicted Sleep</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Quality indicator
            quality_label = "Excellent" if prediction >= 7 else "Moderate" if prediction >= 6 else "Poor"
            quality_color = "#28a745" if prediction >= 7 else "#ffc107" if prediction >= 6 else "#dc3545"
            
            st.markdown(f"""
            <div style="background-color: {quality_color}; color: white; text-align: center; padding: 10px; border-radius: 8px; margin-top: 10px;">
                <div style="font-weight: bold; font-size: 18px;">Sleep Quality: {quality_label}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_res2:
            # Sleep quality meter with animation
            st.markdown(f"""
            <div style="margin-top: 20px;">
                <div style="font-weight: bold; margin-bottom: 10px;">Sleep Duration Scale</div>
                <div style="background:#e0e0e0; height:24px; border-radius:12px; margin-bottom:10px; overflow: hidden;">
                    <div style="background:linear-gradient(90deg, #dc3545 0%, #ffc107 50%, #28a745 100%); 
                        width:{min(100, (prediction/9)*100)}%; height:24px; border-radius:12px; 
                        transition: width 1s ease-in-out;"></div>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom: 20px;">
                    <span style="color: #dc3545; font-weight: bold;">4h (Poor)</span>
                    <span style="color: #ffc107; font-weight: bold;">6h (Moderate)</span>
                    <span style="color: #28a745; font-weight: bold;">8h+ (Excellent)</span>
                </div>
            """, unsafe_allow_html=True)
            
            # Factors affecting sleep
            st.markdown("""
            <div style="margin-top: 10px;">
                <div style="font-weight: bold; margin-bottom: 10px;">Key Factors Affecting Your Sleep:</div>
                <ul style="margin-top: 5px; padding-left: 20px;">
            """, unsafe_allow_html=True)
            
            # Dynamically generate factors
            factors = []
            if screen_time > 3:
                factors.append(f"<li>High screen time ({screen_time} hours) before bed</li>")
            if smoke_drink == 'yes':
                factors.append("<li>Smoking or alcohol consumption</li>")
            if exercise == 'no':
                factors.append("<li>Lack of regular exercise</li>")
            if bluelight_val == 'no' and screen_time > 2:
                factors.append("<li>Extended screen use without blue light filter</li>")
            if beverage in ['Coffee', 'Tea and Coffee both']:
                factors.append("<li>Evening caffeine consumption</li>")
            
            # If no negative factors, add positive ones
            if not factors:
                if exercise == 'yes':
                    factors.append("<li>Regular exercise is helping your sleep quality</li>")
                if bluelight_val == 'yes':
                    factors.append("<li>Using blue light filter is beneficial</li>")
                if screen_time < 2:
                    factors.append("<li>Limited screen time before bed is ideal</li>")
            
            for factor in factors:
                st.markdown(factor, unsafe_allow_html=True)
            
            st.markdown("</ul></div>", unsafe_allow_html=True)
        
        # Close the card div
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Recommendations section with better UI
        st.markdown("""
        <div class="card fade-in" style="margin-top: 30px;">
            <h2 style="margin-top: 0;">💡 Personalized Recommendations</h2>
            <p>Based on your inputs, here are tailored suggestions to improve your sleep:</p>
            <hr>
            <div class="recommendation-container">
        """, unsafe_allow_html=True)
        
        # Screen time recommendations
        if screen_time > 2:
            st.markdown("""
            <div class="recommendation-card">
                <div style="font-size: 24px; margin-bottom: 10px;">📱</div>
                <h3 style="margin-top: 0;">Reduce Screen Time</h3>
                <ul>
                    <li>Aim to put devices away 1 hour before bed</li>
                    <li>Enable night mode/blue light filters</li>
                    <li>Try reading a physical book instead</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Exercise recommendations
        if exercise != 'yes':
            st.markdown("""
            <div class="recommendation-card">
                <div style="font-size: 24px; margin-bottom: 10px;">🏃</div>
                <h3 style="margin-top: 0;">Increase Physical Activity</h3>
                <ul>
                    <li>Start with 20-30 minutes daily</li>
                    <li>Morning exercise can improve sleep quality</li>
                    <li>Even light activities like walking help</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Nutrition recommendations
        if meal_mapping.get(meals, 3) > 3 or beverage in ['Coffee', 'Tea and Coffee both']:
            st.markdown("""
            <div class="recommendation-card">
                <div style="font-size: 24px; margin-bottom: 10px;">🍽️</div>
                <h3 style="margin-top: 0;">Adjust Eating Habits</h3>
                <ul>
                    <li>Finish dinner 2-3 hours before bed</li>
                    <li>Avoid caffeine after 2 PM</li>
                    <li>Consider lighter evening meals</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Substance recommendations
        if smoke_drink == 'yes':
            st.markdown("""
            <div class="recommendation-card">
                <div style="font-size: 24px; margin-bottom: 10px;">🚭</div>
                <h3 style="margin-top: 0;">Limit Substances</h3>
                <ul>
                    <li>Reduce alcohol, especially before bed</li>
                    <li>Avoid smoking near bedtime</li>
                    <li>Consider herbal tea alternatives</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Sleep hygiene recommendations (always show)
        st.markdown("""
        <div class="recommendation-card">
            <div style="font-size: 24px; margin-bottom: 10px;">🛏️</div>
            <h3 style="margin-top: 0;">Sleep Environment</h3>
            <ul>
                <li>Keep bedroom cool (65-68°F/18-20°C)</li>
                <li>Use blackout curtains for darkness</li>
                <li>Maintain a consistent sleep schedule</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Close recommendations container
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        # Sleep tracking suggestion
        st.markdown("""
        <div class="info-card fade-in" style="margin-top: 30px;">
            <h3 style="margin-top: 0;">Track Your Progress</h3>
            <p>Switch to the "Track Progress" tab to monitor your sleep improvement over time.</p>
        </div>
        """, unsafe_allow_html=True)

# Progress tracking tab
with tab2:
    st.markdown("""
    <div class="card">
        <h2 style="margin-top: 0;">📊 Track Your Sleep Progress</h2>
        <p>Regularly monitor your sleep to see improvements over time.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sample tracking interface
    with st.expander("Sleep Tracking Dashboard", expanded=True):
        # Placeholder for tracking data (would be saved in a real app)
        if 'sleep_data' not in st.session_state:
            st.session_state.sleep_data = [
                {'date': '2025-03-24', 'hours': 6.2, 'quality': 3},
                {'date': '2025-03-25', 'hours': 6.5, 'quality': 3},
                {'date': '2025-03-26', 'hours': 6.8, 'quality': 4},
                {'date': '2025-03-27', 'hours': 7.0, 'quality': 4},
                {'date': '2025-03-28', 'hours': 7.2, 'quality': 4},
                {'date': '2025-03-29', 'hours': 7.5, 'quality': 5},
                {'date': '2025-03-30', 'hours': 7.3, 'quality': 4},
            ]
        
        track_col1, track_col2 = st.columns([2, 1])
        
        with track_col1:
            # Create chart data
            chart_data = pd.DataFrame(
                st.session_state.sleep_data,
                columns=['date', 'hours', 'quality']
            )
            
            # Display line chart
            st.line_chart(
                chart_data.set_index('date')['hours'], 
                use_container_width=True,
                height=250
            )
        
        with track_col2:
            # Add new sleep entry form
            st.markdown("### Add Today's Sleep")
            
            sleep_date = st.date_input("Date", value=pd.to_datetime('2025-03-31'))
            sleep_hours = st.number_input("Hours slept", min_value=0.0, max_value=12.0, value=7.0, step=0.1)
            sleep_quality = st.slider("Sleep quality (1-5)", min_value=1, max_value=5, value=4)
            
            if st.button("Add Entry", use_container_width=True):
                new_entry = {
                    'date': sleep_date.strftime('%Y-%m-%d'),
                    'hours': sleep_hours,
                    'quality': sleep_quality
                }
                st.session_state.sleep_data.append(new_entry)
                st.success("Sleep entry added!")
                st.rerun()
    
    # Weekly sleep stats
    st.markdown("""
    <div class="card">
        <h3 style="margin-top: 0;">Weekly Sleep Stats</h3>
    </div>
    """, unsafe_allow_html=True)
    
    stat_col1, stat_col2, stat_col3 = st.columns(3)
    with stat_col1:
        avg_hours = sum(entry['hours'] for entry in st.session_state.sleep_data) / len(st.session_state.sleep_data)
        st.metric("Average Sleep", f"{avg_hours:.1f} hours", delta="+0.6 hrs", delta_color="normal")
    
    with stat_col2:
        avg_quality = sum(entry['quality'] for entry in st.session_state.sleep_data) / len(st.session_state.sleep_data)
        st.metric("Average Quality", f"{avg_quality:.1f}/5", delta="+0.8", delta_color="normal")
                                        


    
    with stat_col3:
        good_nights = sum(1 for entry in st.session_state.sleep_data if entry['hours'] >= 7)
        st.metric("Good Sleep Nights", f"{good_nights}/{len(st.session_state.sleep_data)}", delta="+2", delta_color="normal")
    
    # Sleep improvement tips based on data
    if avg_hours < 7:
        st.markdown("""
        <div class="warning-card">
            <h4 style="margin-top: 0;">💡 Improvement Opportunity</h4>
            <p>Your average sleep is below the recommended 7 hours. Try implementing the personalized recommendations to improve.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="success-card">
            <h4 style="margin-top: 0;">🎉 Good Progress!</h4>
            <p>You're averaging the recommended sleep duration. Keep up the good habits!</p>
        </div>
        """, unsafe_allow_html=True)

# Resources tab
with tab3:
    st.markdown("""
    <div class="card">
        <h2 style="margin-top: 0;">📚 Sleep Resources & Education</h2>
        <p>Learn more about the science of sleep and how to improve your rest.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Resources in expandable sections
    with st.expander("📝 Sleep Science Basics", expanded=True):
        st.markdown("""
        <div style="padding: 0 10px;">
            <h4>The Sleep Cycle</h4>
            <p>Sleep consists of multiple 90-minute cycles, each containing:</p>
            <ul>
                <li><strong>NREM Stage 1:</strong> Light sleep, easily awakened</li>
                <li><strong>NREM Stage 2:</strong> Body temperature drops, heart rate slows</li>
                <li><strong>NREM Stage 3:</strong> Deep sleep, body repairs tissues</li>
                <li><strong>REM Sleep:</strong> Brain activity increases, dreaming occurs</li>
            </ul>
            <h4>Sleep and Health</h4>
            <p>Quality sleep is linked to:</p>
            <ul>
                <li>Improved immune function</li>
                <li>Better cognitive performance</li>
                <li>Emotional regulation</li>
                <li>Weight management</li>
                <li>Lower risk of chronic diseases</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("🌿 Natural Sleep Remedies"):
        st.markdown("""
        <div style="padding: 0 10px;">
            <h4>Herbal Sleep Aids</h4>
            <p>These natural remedies may help with sleep:</p>
            <ul>
                <li><strong>Valerian Root:</strong> May improve sleep quality</li>
                <li><strong>Lavender:</strong> Aromatherapy benefits for relaxation</li>
                <li><strong>Chamomile Tea:</strong> Traditional calming beverage</li>
                <li><strong>Magnesium:</strong> Helps regulate sleep hormones</li>
            </ul>
            <p><em>Note: Consult with a healthcare provider before trying supplements.</em></p>
            <h4>Relaxation Techniques</h4>
            <ul>
                <li><strong>Progressive Muscle Relaxation:</strong> Tensing and releasing muscle groups</li>
                <li><strong>4-7-8 Breathing:</strong> Inhale for 4, hold for 7, exhale for 8 seconds</li>
                <li><strong>Body Scan Meditation:</strong> Focusing awareness from head to toe</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("⚙️ Sleep Technology"):
        st.markdown("""
        <div style="padding: 0 10px;">
            <h4>Sleep Tracking Tools</h4>
            <ul>
                <li><strong>Wearable Devices:</strong> Fitness trackers with sleep monitoring</li>
                <li><strong>Smart Mattresses:</strong> Track movement, breathing, and heart rate</li>
                <li><strong>Sleep Apps:</strong> Monitor sleep cycles using phone sensors</li>
                <li><strong>Smart Lighting:</strong> Adjusts color temperature for better sleep</li>
            </ul>
            <h4>Recommended Features</h4>
            <ul>
                <li>Sleep cycle tracking</li>
                <li>Smart alarm (wakes you during light sleep)</li>
                <li>Sleep environment monitoring (temperature, noise)</li>
                <li>Sleep reports and trends</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with st.expander("❓ Common Sleep Questions"):
        st.markdown("""
        <div style="padding: 0 10px;">
            <h4>Frequently Asked Questions</h4>
            <p><strong>Q: How much sleep do I really need?</strong><br>
            A: Adults typically need 7-9 hours, but individual needs vary. Consistent energy throughout the day indicates adequate sleep.</p>
            <p><strong>Q: Is napping good or bad?</strong><br>
            A: Short naps (20-30 minutes) can be beneficial. Longer naps or napping late in the day may disrupt nighttime sleep.</p>
            <p><strong>Q: Does exercise timing affect sleep?</strong><br>
            A: Morning and afternoon exercise generally promotes better sleep. Vigorous exercise within 1-2 hours of bedtime may disrupt sleep for some people.</p>
            <p><strong>Q: What's the ideal bedroom temperature?</strong><br>
            A: 65-68°F (18-20°C) is optimal for most people. A slightly cool room promotes better sleep.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Interactive sleep quiz
    st.markdown("""
    <div class="card mt-4">
        <h3 style="margin-top: 0;">🧠 Test Your Sleep Knowledge</h3>
        <p>Take this quick quiz to learn more about sleep science!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sample quiz
    with st.form("sleep_quiz"):
        st.markdown("### Sleep Quiz")
        
        q1 = st.radio(
            "1. How many stages are in a complete sleep cycle?",
            ["2 stages", "3 stages", "4 stages", "5 stages"]
        )
        
        q2 = st.radio(
            "2. Which of these is NOT a benefit of quality sleep?",
            ["Improved memory", "Decreased calorie needs", "Better immune function", "Emotional regulation"]
        )
        
        q3 = st.radio(
            "3. What is the recommended bedroom temperature for optimal sleep?",
            ["60-62°F (15-16°C)", "65-68°F (18-20°C)", "72-75°F (22-24°C)", "78-80°F (25-27°C)"]
        )
        
        quiz_submitted = st.form_submit_button("Check My Answers")
    
    if quiz_submitted:
        score = 0
        if q1 == "4 stages":
            score += 1
        if q2 == "Decreased calorie needs":
            score += 1
        if q3 == "65-68°F (18-20°C)":
            score += 1
        
        # Display score
        if score == 3:
            st.markdown("""
            <div class="success-card">
                <h4 style="margin-top: 0;">🎉 Perfect Score: 3/3</h4>
                <p>Excellent! You're a sleep science expert!</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="info-card">
                <h4 style="margin-top: 0;">Quiz Score: {score}/3</h4>
                <p>Here are the correct answers:</p>
                <ol>
                    <li>4 stages (NREM 1, NREM 2, NREM 3, and REM)</li>
                    <li>"Decreased calorie needs" is incorrect - sleep actually helps regulate metabolism</li>
                    <li>65-68°F (18-20°C) is the ideal temperature range for most people</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="background-color: #f0f4f8; padding: 20px; border-radius: 10px; margin-top: 40px; text-align: center;">
    <p style="margin: 0; color: #555;">
        Sleep Pattern Analyzer • Created for better sleep health • 
        <a href="https://www.sleepfoundation.org/" target="_blank">More Resources</a>
    </p>
</div>
""", unsafe_allow_html=True)

# Add a floating help button
st.markdown("""
<style>
.floating-help-button {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background-color: #3a86ff;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    display: flex;
    justify-content: center;
    align-items: center;
    color: white;
    font-size: 24px;
    cursor: pointer;
    z-index: 9999;
    transition: all 0.3s ease;
}
.floating-help-button:hover {
    transform: scale(1.1);
    background-color: #2a76ef;
}
</style>

<div class="floating-help-button" onclick="alert('Need help? Email support@sleeppredictor.app')">
    ?
</div>
""", unsafe_allow_html=True)