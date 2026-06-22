import streamlit as st
import streamlit.components.v1 as components
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import cv2
import mediapipe as mp
import pickle
import av

# Load model
with open("sign_model.pkl", "rb") as f:
    model = pickle.load(f)

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

st.title("AI-Based Sign Language to Speech & Text Translator")
st.write("Show a hand sign to the camera below.")

if "last_sign" not in st.session_state:
    st.session_state["last_sign"] = ""

if "spoken_sign" not in st.session_state:
    st.session_state["spoken_sign"] = ""


class SignProcessor(VideoProcessorBase):
    def __init__(self):
        self.hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        result = self.hands.process(rgb)

        if result.multi_hand_landmarks:
            for handLms in result.multi_hand_landmarks:

                mp_draw.draw_landmarks(
                    img,
                    handLms,
                    mp_hands.HAND_CONNECTIONS
                )

                landmark_list = []

                for lm in handLms.landmark:
                    landmark_list.extend([lm.x, lm.y, lm.z])

                prediction = str(model.predict([landmark_list])[0])

                st.session_state["last_sign"] = prediction

                cv2.putText(
                    img,
                    prediction,
                    (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.2,
                    (0, 255, 0),
                    3,
                )

        return av.VideoFrame.from_ndarray(img, format="bgr24")


webrtc_streamer(
    key="sign-language",
    video_processor_factory=SignProcessor,
)

if st.session_state["last_sign"]:

    st.success(f"Detected Sign: {st.session_state['last_sign']}")

    if st.session_state["spoken_sign"] != st.session_state["last_sign"]:

        components.html(
            f"""
            <script>
            const text = "{st.session_state['last_sign']}";
            const speech = new SpeechSynthesisUtterance(text);
            speech.lang = "en-US";
            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(speech);
            </script>
            """,
            height=0,
        )

        st.session_state["spoken_sign"] = st.session_state["last_sign"]
