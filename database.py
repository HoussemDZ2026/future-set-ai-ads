import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os
import json

# 1. إعداد الاتصال بـ Firebase
def initialize_db():
    # سنقوم بتخزين مفتاح Firebase كـ "Secret" في Hugging Face للأمان
    if not firebase_admin._apps:
        # جلب معلومات المفتاح من البيئة (سأعلمك كيف تضعها لاحقاً)
        key_dict = json.loads(os.getenv("FIREBASE_SERVICE_ACCOUNT"))
        cred = credentials.Certificate(key_dict)
        firebase_admin.initialize_app(cred)
    return firestore.client()

db = initialize_db()

# 2. دالة التحقق من اشتراك المستخدم
def check_user_subscription(user_id):
    try:
        user_ref = db.collection('users').document(user_id)
        doc = user_ref.get()
        
        if doc.exists:
            user_data = doc.to_dict()
            expiry_date_str = user_data.get('expiry_date') # التنسيق: YYYY-MM-DD
            
            # تحويل النص إلى تاريخ ومقارنته بالوقت الحالي
            expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d')
            if expiry_date > datetime.now():
                return True, f"اشتراكك ساري المفعول حتى {expiry_date_str}"
            else:
                return False, "انتهت مدة اشتراكك. يرجى التواصل مع الإدارة للتجديد."
        else:
            return False, "معرف المستخدم غير موجود. يرجى التسجيل أولاً."
    except Exception as e:
        return False, f"خطأ في الاتصال بقاعدة البيانات: {str(e)}"
