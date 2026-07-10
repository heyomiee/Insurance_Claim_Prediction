import streamlit as st
import pandas as pd
import pickle
import base64
import os

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Insurance Charges Prediction",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# PATHS
# =====================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IMAGE_DIR = os.path.join(BASE_DIR, "..", "01_images")

MODEL_PATH = os.path.join(BASE_DIR, "insurance_model.sav")

CSS_PATH = os.path.join(BASE_DIR, "style.css")

# =====================================================
# LOAD CSS
# =====================================================

with open(CSS_PATH) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# =====================================================
# LOAD MODEL
# =====================================================

model = pickle.load(open(MODEL_PATH, "rb"))

# =====================================================
# BACKGROUND IMAGE
# =====================================================

def get_base64(file):
    with open(file, "rb") as img:
        return base64.b64encode(img.read()).decode()

background = get_base64(
    os.path.join(IMAGE_DIR, "background.jpg.jpeg")
)

st.markdown(
f"""
<style>

[data-testid="stAppViewContainer"]{{
background-image:url("data:image/jpeg;base64,{background}");
background-size:cover;
background-position:center;
background-repeat:no-repeat;
background-attachment:fixed;
}}

[data-testid="stHeader"]{{
background:transparent;
}}

</style>
""",
unsafe_allow_html=True,
)

# =====================================================
# SIDEBAR
# =====================================================

logo = os.path.join(IMAGE_DIR, "logo.png.jpeg")

st.sidebar.image(logo, width=120)

st.sidebar.markdown(
"""
<h2 style="text-align:center;color:#0A3DA8;">
Insurance App
</h2>
""",
unsafe_allow_html=True,
)

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "🎯 Prediction",
        "ℹ️ About"
    ],
    index=1
)

# =====================================================
# HOME PAGE
# =====================================================

if page == "🏠 Home":

    st.markdown("""
<div class="glass">

<h1>Insurance Charges Prediction</h1>

<br>

<h3>
Predict Medical Insurance Charges using Machine Learning
</h3>

<br>

✔ Random Forest Model

<br><br>

✔ Beautiful Streamlit Dashboard

<br><br>

✔ Fast Prediction

<br><br>

✔ Easy To Use

</div>
""", unsafe_allow_html=True)

# =====================================================
# ABOUT PAGE
# =====================================================

elif page == "ℹ️ About":

    st.markdown("""
<div class="glass">

<h1>About Project</h1>

<hr>

<h3>Technology Used</h3>

<ul>

<li>Python</li>

<li>Pandas</li>

<li>Scikit-Learn</li>

<li>Random Forest</li>

<li>Streamlit</li>

</ul>

</div>
""", unsafe_allow_html=True)

# =====================================================
# PREDICTION PAGE
# =====================================================

else:

    col1, col2 = st.columns([8,1])

    with col1:

        st.markdown(
            "<h1 class='title'>Insurance Charges Prediction</h1>",
            unsafe_allow_html=True
        )

    with col2:

        doctor = os.path.join(
            IMAGE_DIR,
            "doctor.png.jpeg"
        )

        st.image(doctor, width=140)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
<div class="input-box">

<h1 class="white-title">
Enter Details
</h1>
""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:

        age = st.number_input(
            "Age",
            min_value=18,
            max_value=100,
            value=25
        )

    with c2:

        bmi = st.number_input(
            "BMI",
            min_value=10.0,
            max_value=60.0,
            value=25.0
        )

    with c3:

        children = st.number_input(
            "Children",
            min_value=0,
            max_value=10,
            value=0
        )

    c4, c5, c6 = st.columns(3)

    with c4:

        sex = st.selectbox(
            "Sex",
            ["Male","Female"]
        )

    with c5:

        smoker = st.selectbox(
            "Smoker",
            ["No","Yes"]
        )

    with c6:

        region = st.selectbox(
            "Region",
            [
                "Southwest",
                "Southeast",
                "Northwest",
                "Northeast"
            ]
        )

    st.markdown("</div>", unsafe_allow_html=True)
        # =====================================================
    # PREDICTION BUTTON
    # =====================================================

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🔍 Predict Insurance Charges", use_container_width=True):

        # -----------------------------
        # Feature Engineering
        # -----------------------------

        is_feamle = 1 if sex == "Female" else 0
        is_smoker = 1 if smoker == "Yes" else 0
        region_southeast = 1 if region == "Southeast" else 0
        bmi_category_Obese = 1 if bmi >= 30 else 0

        # -----------------------------
        # Create Model Input
        # -----------------------------

        input_df = pd.DataFrame([{
            "age": age,
            "is_feamle": is_feamle,
            "bmi": bmi,
            "children": children,
            "is_smoker": is_smoker,
            "region_southeast": region_southeast,
            "bmi_category_Obese": bmi_category_Obese
        }])

        # -----------------------------
        # Prediction
        # -----------------------------

        prediction = model.predict(input_df)[0]

        st.markdown("<br>", unsafe_allow_html=True)

        left, right = st.columns([4,1])

        with left:

            st.markdown(
                f"""
<div class="result-card">

<h2 class="result-title">
Predicted Insurance Charges
</h2>

<h1 class="result-price">
₹ {prediction:,.2f}
</h1>

</div>
""",
                unsafe_allow_html=True
            )

        with right:

            shield = os.path.join(
                IMAGE_DIR,
                "shield.png.jpeg"
            )

            st.image(shield, width=170)

        st.success("Prediction Completed Successfully 🎉")
        st.balloons()

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("""
<div style="text-align:center;color:white;font-size:18px;">
Made with ❤️ using Streamlit & Machine Learning
</div>
""", unsafe_allow_html=True)