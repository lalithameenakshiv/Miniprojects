import streamlit as st
import tempfile
import os
import sys
import importlib.util
import pandas as pd
from pathlib import Path

app_dir = Path(__file__).resolve().parent

def load_local_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

_detector = load_local_module("local_detector", app_dir / "detector.py")
_youtube = load_local_module("local_youtube", app_dir / "youtube.py")

VehicleDetector = _detector.VehicleDetector
download_youtube_video = _youtube.download_youtube_video


# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Traffic Vision AI",
    page_icon="🚦",
    layout="wide"
)


# ---------------- HEADER ---------------- #

st.title("🚦 Traffic Vision AI")
st.subheader(
    "AI-Powered Intelligent Traffic Video Analytics System"
)

st.write(
    """
    Vehicle Detection • Classification • Counting • Traffic Density Analysis
    """
)

st.divider()


# ---------------- SIDEBAR ---------------- #

st.sidebar.title("⚙ Settings")

source = st.sidebar.radio(
    "Select Input Source",
    [
        "Upload Video",
        "YouTube Video"
    ]
)

if "video_path" not in st.session_state:
    st.session_state.video_path = None

if "youtube_url" not in st.session_state:
    st.session_state.youtube_url = ""


# ---------------- VIDEO INPUT ---------------- #

if source == "Upload Video":

    uploaded_file = st.file_uploader(
        "📂 Upload Traffic Video",
        type=[
            "mp4",
            "avi",
            "mov"
        ]
    )

    if uploaded_file is not None:

        temp = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp4"
        )

        temp.write(uploaded_file.read())
        temp.close()

        st.session_state.video_path = temp.name

        st.success("Video uploaded successfully")


else:

    st.session_state.youtube_url = st.text_input(
        "🔗 Enter YouTube Traffic Video URL",
        value=st.session_state.youtube_url,
        key="youtube_url_input"
    )

    if st.button("Download Video"):

        if st.session_state.youtube_url:

            with st.spinner("Downloading YouTube video..."):
                st.session_state.video_path = download_youtube_video(
                    st.session_state.youtube_url
                )

            st.success("Video downloaded successfully")

        else:
            st.warning("Please enter YouTube URL")


# ---------------- ANALYSIS ---------------- #

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if st.session_state.video_path:
    video_path = st.session_state.video_path

    st.divider()

    if st.button("🚀 Start AI Traffic Analysis"):
        detector = VehicleDetector()
        output_video = "processed_output.mp4"

        with st.spinner("YOLOv8 Model Processing Frames..."):
            result = detector.process_video(video_path, output_video)

        st.session_state.analysis_result = result
        st.success("Analysis Completed Successfully!")

    if st.session_state.analysis_result is not None:
        result = st.session_state.analysis_result
        st.divider()

        # ---------------- METRICS ---------------- #
        st.subheader("📊 Traffic Analytics")
        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric("🚗 Cars", result["Car"])


        col2.metric(
            "🏍 Motorcycles",
            result["Motorcycle"]
        )


        col3.metric(
            "🚌 Buses",
            result["Bus"]
        )


        col4.metric(
            "🚚 Trucks",
            result["Truck"]
        )


        col5.metric(
            "Total Vehicles",
            result["Total"]
        )



        st.divider()



        # ---------------- DATAFRAME ---------------- #

        st.subheader(
            "Vehicle Classification"
        )


        df = pd.DataFrame(
            {
                "Vehicle Type":
                [
                    "Car",
                    "Motorcycle",
                    "Bus",
                    "Truck"
                ],

                "Count":
                [
                    result["Car"],
                    result["Motorcycle"],
                    result["Bus"],
                    result["Truck"]
                ]
            }
        )


        st.dataframe(
            df,
            use_container_width=True
        )



        # ---------------- CHART ---------------- #

        st.subheader(
            "Vehicle Distribution"
        )


        st.bar_chart(
            df.set_index(
                "Vehicle Type"
            )
        )



        # ---------------- DENSITY ---------------- #

        st.subheader(
            "🚦 Traffic Density"
        )


        total = result["Total"]


        if total < 30:

            density = "🟢 LOW"


        elif total < 80:

            density = "🟡 MEDIUM"


        else:

            density = "🔴 HIGH"



        st.info(
            f"Current Traffic Density : {density}"
        )



        st.divider()



        # ---------------- VIDEO OUTPUT ---------------- #

        st.subheader(
            "🎥 Processed Traffic Video"
        )


        if os.path.exists(
            result["Output Video"]
        ):


            with open(
                result["Output Video"],
                "rb"
            ) as video:


                st.video(
                    video.read()
                )



        st.success(
            "🚦 Traffic Vision AI Report Generated"
        )



else:

    st.info(
        "Upload a traffic video or provide YouTube URL to start analysis"
    )