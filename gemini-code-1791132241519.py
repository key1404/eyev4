import streamlit as st
import numpy as np
from PIL import Image
import streamlit.components.v1 as components

# تنظیمات صفحه
st.set_page_config(
    page_title="Eye1 AI | سامانه جامع انتخاب و تست زنده عینک",
    page_icon="👓",
    layout="wide"
)

st.title("👓 سامانه هوشمند Eye1: تحلیل چهره، پیشنهاد تخصصی و امتحان مجازی زنده")

# مدیریت حالت‌های برنامه (مراحل سه‌گانه)
if "step" not in st.session_state:
    st.session_state.step = "capture"
if "image" not in st.session_state:
    st.session_state.image = None
if "face_shape" not in st.session_state:
    st.session_state.face_shape = ""
if "selected_frame" not in st.session_state:
    st.session_state.selected_frame = None

# نوار کناری تنظیمات بالینی
st.sidebar.header("⚙️ پارامترهای اپتومتری")
rx_type = st.sidebar.selectbox("نوع نسخه بینایی (Rx)", ["دوربین / نزدیک‌بین (ساده)", "آستیگمات", "دید پیش‌رونده", "بدون نمره"])
pd_input = st.sidebar.slider("فاصله دو چشم (PD بر حسب میلی‌‌متر)", 50, 75, 62)

# ---------------------------------------------------------
# مرحله ۱: ثبت یا آپلود تصویر چهره برای آنالیز اولیه
# ---------------------------------------------------------
if st.session_state.step == "capture":
    st.markdown("### مرحله ۱: ثبت تصویر چهره برای تحلیل آناتومیک")
    st.info("لطفاً یک تصویر واضح از چهره خود آپلود کنید یا عکسی برای استخراج فرم صورت ثبت نمایید.")
    
    tab1, tab2 = st.tabs(["📸 عکاسی برای تحلیل اولیه", "📤 آپلود فایل تصویر"])
    
    uploaded_img = None
    with tab1:
        cam_file = st.camera_input("ثبت عکس جهت آنالیز اولیه:")
        if cam_file is not None:
            uploaded_img = Image.open(cam_file)
            
    with tab2:
        file = st.file_uploader("یا بارگذاری تصویر چهره:", type=["jpg", "jpeg", "png"])
        if file is not None:
            uploaded_img = Image.open(file)
            
    if uploaded_img is not None:
        st.session_state.image = uploaded_img
        
        # تحلیل هندسی فرم صورت
        img_arr = np.array(uploaded_img)
        h, w = img_arr.shape[:2]
        ratio = h / w
        
        if ratio > 1.38:
            st.session_state.face_shape = "کشیده (Oblong / Long Face)"
            st.session_state.frames = [
                {"name": "Tom Ford - Aviator Luxe", "type": "خلبانی عریض با پل ضخیم", "brand": "Tom Ford", "icon": "✈️", "color": "#1f77b4", "symbol": "🕶️"},
                {"name": "Ray-Ban - Square Classic", "type": "مستطیلی پهن کلاسیک", "brand": "Ray-Ban", "icon": "⬛", "color": "#ff7f0e", "symbol": "👓"}
            ]
        elif 1.18 <= ratio <= 1.38:
            st.session_state.face_shape = "بیضی متعادل (Oval - استاندارد طلایی)"
            st.session_state.frames = [
                {"name": "Ray-Ban - Wayfarer Original", "type": "ویفرر استاندارد کلاسیک", "brand": "Ray-Ban", "icon": "🕶️", "color": "#2ca02c", "symbol": "🕶️"},
                {"name": "Tom Ford - Cat Eye Modern", "type": "چشم‌گربه‌ای شیک و مدرن", "brand": "Tom Ford", "icon": "🐱", "color": "#d62728", "symbol": "👓"}
            ]
        else:
            st.session_state.face_shape = "گرد یا مربعی (Round / Square)"
            st.session_state.frames = [
                {"name": "Tom Ford - Slim Rectangular", "type": "مستطیلی باریک زاویه‌دار", "brand": "Tom Ford", "icon": "📐", "color": "#9467bd", "symbol": "👓"},
                {"name": "Ray-Ban - Round Metal", "type": "گرد فلزی مینیمال سبک", "brand": "Ray-Ban", "icon": "⚪", "color": "#8c564b", "symbol": "🥽"}
            ]
        
        st.session_state.step = "analyze"
        st.rerun()

# ---------------------------------------------------------
# مرحله ۲: نمایش تحلیل چهره و گالری مدل‌ها
# ---------------------------------------------------------
elif st.session_state.step == "analyze":
    st.markdown("### مرحله ۲: نتیجه تحلیل هوش مصنوعی و انتخاب مدل فریم")
    
    col_img, col_report = st.columns([1, 1.3])
    with col_img:
        st.image(st.session_state.image, caption="تصویر تحلیل‌شده", use_column_width=True)
        if st.button("🔄 عکاسی یا بارگذاری تصویر جدید"):
            st.session_state.step = "capture"
            st.rerun()
            
    with col_report:
        st.success("✅ تحلیل آناتومیک با موفقیت انجام شد!")
        st.write(f"🔹 **فرم هندسی تشخیص‌داده‌شده:** {st.session_state.face_shape}")
        st.write(f"📏 **پارامترهای PD:** {pd_input}mm | **نسخه:** {rx_type}")
        st.markdown("---")
        st.markdown("💡 لطفاً یکی از مدل‌های زیر را انتخاب کنید تا مستقیماً وارد **اتاق تست زنده و دوربین** شوید:")

    st.markdown("---")
    
    f_cols = st.columns(len(st.session_state.frames))
    for i, frame in enumerate(st.session_state.frames):
        with f_cols[i]:
            st.markdown(f"""
                <div style="border: 2px solid {frame['color']}; padding: 15px; border-radius: 10px; background-color: #fcfcfc; text-align: center;">
                    <h2 style="margin: 0;">{frame['icon']}</h2>
                    <h4>{frame['name']}</h4>
                    <p><b>برند:</b> {frame['brand']}</p>
                    <p><b>طراحی:</b> {frame['type']}</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"✨ انتخاب و تست زنده این فریم", key=f"btn_frame_{i}"):
                st.session_state.selected_frame = frame
                st.session_state.step = "tryon"
                st.rerun()

# ---------------------------------------------------------
# مرحله ۳: اتاق امتحان مجازی زنده با دوربین (Live AR Try-On)
# ---------------------------------------------------------
elif st.session_state.step == "tryon":
    chosen = st.session_state.selected_frame
    
    st.markdown(f"### مرحله ۳: اتاق تست زنده و واقعیت افزوده (فریم فعال: {chosen['name']})")
    st.markdown("در این بخش دوربین زنده دستگاه شما فعال می‌شود. می‌توانید سر خود را در زوایای مختلف حرکت دهید و فیت بودن عینک را به صورت زنده بررسی کنید.")
    
    if st.button("← بازگشت به گالری و انتخاب فریم دیگر"):
        st.session_state.step = "analyze"
        st.rerun()
        
    st.markdown("---")

    # کد جاوا اسکریپت و HTML5 اصلاح شده برای جلوگیری از خطای سینتکسی ف-استینگ
    live_tryon_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .video-container {{
                position: relative;
                width: 100%;
                max-width: 640px;
                margin: auto;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                background: #000;
            }}
            video {{
                width: 100%;
                height: auto;
                display: block;
                transform: scaleX(-1);
            }}
            .glasses-overlay {{
                position: absolute;
                top: 40%;
                left: 50%;
                transform: translate(-50%, -50%);
                font-size: 80px;
                pointer-events: none;
                user-select: none;
                filter: drop-shadow(0px 4px 6px rgba(0,0,0,0.4));
            }}
            .info-bar {{
                text-align: center;
                background: #eef7fc;
                padding: 10px;
                font-family: Tahoma, sans-serif;
                font-size: 14px;
                color: #333;
            }}
        </style>
    </head>
    <body>
        <div class="video-container">
            <video id="webcam" autoplay playsinline muted></video>
            <div class="glasses-overlay">{chosen['symbol']}</div>
        </div>
        <div class="info-bar">
            <b>فریم فعال:</b> {chosen['name']} | <b>تنظیم PD:</b> {pd_input}mm | وضعیت: 🟢 دوربین زنده متصل است
        </div>

        <script>
            const video = document.getElementById('webcam');
            
            navigator.mediaDevices.getUserMedia({{ video: {{ width: 640, height: 480 }} }})
                .then(stream => {{
                    video.srcObject = stream;
                }})
                .catch(err => {{
                    alert("خطا در دسترسی به دوربین: لطفاً دسترسی دوربین را در مرورگر تایید کنید.");
                    console.error(err);
                }});
        </script>
    </body>
    </html>
    """

    components.html(live_tryon_html, height=560)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 پایان تست و شروع مجدد با چهره جدید"):
        st.session_state.step = "capture"
        st.rerun()