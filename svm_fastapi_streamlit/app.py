import streamlit as st
import requests

st.set_page_config(
    page_title="Wine Quality Prediction",
    page_icon="🍷",
    layout="wide"
)

# ===============================
# CUSTOM STYLE
# ===============================
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #2b0a10 0%, #1a0509 100%);
    }
    h1, h2, h3, p, label, span {
        color: #f5e6e8 !important;
    }
    div[data-testid="stMetricValue"] {
        color: #e8b4b8 !important;
    }
    .stButton>button {
        background-color: #7a1f2b;
        color: #f5e6e8;
        border-radius: 8px;
        border: 1px solid #b3384a;
        padding: 0.6em 2em;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #9c2a39;
        border: 1px solid #e8b4b8;
        color: #ffffff;
    }
    div[data-testid="stExpander"] {
        background-color: rgba(255,255,255,0.03);
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ===============================
# HEADER
# ===============================
st.markdown("<h1>🍷 Wine Quality Prediction</h1>", unsafe_allow_html=True)
st.markdown("<p>Prediksi kualitas Red Wine berdasarkan 11 parameter fisikokimia. "
            "Model akan menentukan apakah anggur tergolong <b>Good Quality</b> "
            "(skor penilaian ≥ 7) atau <b>Standard Quality</b>.</p>", unsafe_allow_html=True)

st.markdown("---")

# ===============================
# DEFINISI FITUR
# (label, satuan, min, max, default, step, deskripsi singkat)
# ===============================
feature_config = [
    ("Fixed Acidity", "g/dm³", 4.6, 15.9, 8.3, 0.1,
     "Kadar asam tetap (tartaric acid) — memengaruhi rasa asam dasar anggur."),
    ("Volatile Acidity", "g/dm³", 0.12, 1.58, 0.53, 0.01,
     "Kadar asam asetat — terlalu tinggi bisa menimbulkan rasa/aroma cuka."),
    ("Citric Acid", "g/dm³", 0.0, 1.0, 0.27, 0.01,
     "Asam sitrat — menambah kesegaran rasa pada anggur."),
    ("Residual Sugar", "g/dm³", 0.9, 15.5, 2.5, 0.1,
     "Sisa gula setelah fermentasi berhenti."),
    ("Chlorides", "g/dm³", 0.012, 0.611, 0.087, 0.001,
     "Kadar garam pada anggur."),
    ("Free Sulfur Dioxide", "mg/dm³", 1.0, 72.0, 15.9, 1.0,
     "SO2 bebas — mencegah pertumbuhan mikroba dan oksidasi."),
    ("Total Sulfur Dioxide", "mg/dm³", 6.0, 289.0, 46.5, 1.0,
     "Total SO2 (bebas + terikat) dalam anggur."),
    ("Density", "g/cm³", 0.9901, 1.0037, 0.9967, 0.0001,
     "Massa jenis, dipengaruhi kadar alkohol dan gula."),
    ("pH", "", 2.74, 4.01, 3.31, 0.01,
     "Tingkat keasaman anggur, umumnya berkisar 2.7–4.0."),
    ("Sulphates", "g/dm³", 0.33, 2.0, 0.66, 0.01,
     "Kadar sulfat — berkaitan dengan kadar SO2 sebagai antioksidan."),
    ("Alcohol", "% vol", 8.4, 14.9, 10.4, 0.1,
     "Persentase kadar alkohol dalam anggur."),
]

# ===============================
# INPUT FORM (3 kolom)
# ===============================
st.subheader("Parameter Anggur")

inputs = []
cols = st.columns(3)

for i, (label, unit, min_v, max_v, default_v, step, desc) in enumerate(feature_config):
    with cols[i % 3]:
        satuan = f" ({unit})" if unit else ""
        value = st.slider(
            f"{label}{satuan}",
            min_value=float(min_v),
            max_value=float(max_v),
            value=float(default_v),
            step=float(step),
            help=desc
        )
        inputs.append(value)

st.markdown("---")

# ===============================
# PREDIKSI
# ===============================
col_btn, _ = st.columns([1, 3])
with col_btn:
    predict_clicked = st.button("🔍 Predict Quality", use_container_width=True)

if predict_clicked:

    url = "http://127.0.0.1:8000/predict"

    with st.spinner("Menghitung prediksi..."):
        response = requests.post(
            url,
            json={
                "features": inputs
            }
        )

    hasil = response.json()
    prediction = hasil["prediction"]
    probability = hasil["probability"]

    st.markdown("### Hasil Prediksi")

    res_col1, res_col2 = st.columns(2)

    with res_col1:
        if prediction == 1:
            st.success("🍷 **Good Quality** — Anggur ini diprediksi memiliki kualitas baik!")
        else:
            st.warning("🥂 **Standard Quality** — Anggur ini diprediksi belum masuk kategori premium.")

    with res_col2:
        st.metric("Confidence", f"{probability:.2%}")
        st.progress(min(max(probability, 0.0), 1.0))
