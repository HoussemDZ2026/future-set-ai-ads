import streamlit as st
from database import db
from datetime import datetime, timedelta

# 1. إعداد كلمة سر بسيطة للوحة التحكم
ADMIN_PASSWORD = "Houssam_Future_Set_2026" # يمكنك تغييرها لاحقاً

def show_admin_panel():
    st.header("🔐 لوحة تحكم مدير Future Set")
    
    password = st.text_input("أدخل كلمة سر المدير:", type="password")
    
    if password == ADMIN_PASSWORD:
        st.success("تم الدخول بنجاح!")
        st.divider()
        
        # خيار إضافة أو تفعيل مستخدم
        st.subheader("➕ إضافة/تجديد اشتراك مستخدم")
        user_id = st.text_input("معرف المستخدم (مثلاً رقم الهاتف):")
        days = st.number_input("عدد أيام الاشتراك:", min_value=1, value=30)
        
        if st.button("تفعيل الاشتراك"):
            if user_id:
                # حساب تاريخ الانتهاء
                expiry_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
                
                # حفظ في Firebase
                db.collection('users').document(user_id).set({
                    'expiry_date': expiry_date,
                    'last_updated': datetime.now()
                })
                st.balloons()
                st.success(f"تم تفعيل المستخدم {user_id} بنجاح حتى تاريخ {expiry_date}")
            else:
                st.error("يرجى إدخال معرف المستخدم!")

        st.divider()
        # خيار عرض قائمة المشتركين
        st.subheader("📋 قائمة المشتركين الحاليين")
        if st.button("تحديث القائمة"):
            users = db.collection('users').stream()
            for user in users:
                data = user.to_dict()
                st.write(f"👤 **ID:** {user.id} | **ينتهي في:** {data.get('expiry_date')}")
    
    elif password != "":
        st.error("كلمة السر خاطئة!")
