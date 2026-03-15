import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
import urllib.parse

# 1. إعدادات الصفحة (لتظهر كتطبيق هاتف)
st.set_page_config(page_title="Future Set AI", page_icon="🚀", layout="centered")

# تحسين مظهر الواجهة بالـ CSS
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    .stImage { border-radius: 10px; box-shadow: 0px 4px 10px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 مساعد Future Set الذكي")
st.caption("توليد إعلانات احترافية (نص + صور) لمنصتك التعليمية")

# 2. جلب مفتاح Gemini (سنضعه لاحقاً في إعدادات Hugging Face)
# إذا كنت تجرب محلياً، تأكد من وضع المفتاح في البيئة
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.warning("⚠️ يرجى ضبط مفتاح GOOGLE_API_KEY في الإعدادات السرية.")
    st.stop()

# 3. دالة توليد الإعلان والصورة
def generate_future_set_ad(user_topic):
    # إعداد نموذج Gemini
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=API_KEY)
    
    # طلب النص الإعلاني (باللهجة الجزائرية)
    text_prompt = f"""
    أنت خبير تسويق محترف لمنصة Future Set التعليمية في الجزائر. 
    اكتب منشور إعلاني جذاب بالدرجة الجزائرية (مع لمسة فصحى) حول: {user_topic}.
    ركز على الفائدة العلمية والتميز. أضف رموز تعبيرية (Emojis).
    """
    ad_content = llm.invoke(text_prompt).content
    
    # طلب وصف للصورة (بالانجليزية لمحرك الصور)
    img_prompt_query = f"Create a high-quality artistic prompt for an educational advertisement about {user_topic}. Style: modern, bright, educational, 4k."
    img_description = llm.invoke(img_prompt_query).content
    
    # تحويل الوصف لرابط صورة مجاني من Pollinations
    encoded_prompt = urllib.parse.quote(img_description)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&seed=42"
    
    return ad_content, image_url

# 4. نظام الدردشة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "image" in msg:
            st.image(msg["image"])

# استقبال طلب المستخدم
if prompt := st.chat_input("مثلاً: دروس دعم في الرياضيات للثانوي"):
    # إضافة رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # معالجة الطلب من قبل الذكاء الاصطناعي
    with st.chat_message("assistant"):
        with st.spinner("جاري التفكير وتصميم الإعلان..."):
            try:
                text_result, img_result = generate_future_set_ad(prompt)
                
                # عرض النص
                st.markdown(text_result)
                # عرض الصورة
                st.image(img_result, caption="تصميم مقترح بواسطة Future Set AI")
                
                # حفظ في الذاكرة
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": text_result, 
                    "image": img_result
                })
            except Exception as e:
                st.error(f"حدث خطأ: {e}")
