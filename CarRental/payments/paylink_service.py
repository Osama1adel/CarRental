# payments/paylink_service.py (تعديل لإضافة تصدير paylink)
from paylink import Paylink, PaylinkProduct
from django.conf import settings

# تهيئة كائن Paylink في وضع الاختبار (يجب أن يتم تصديره)
paylink = Paylink.test() # <--- هذا هو المتغير الذي يجب تصديره

def create_paylink_invoice(booking, callback_url):
    """
    تنشئ فاتورة Paylink وترجع رقم العملية ورابط الدفع.
    """
    
    # ... (بقية الكود الخاص بجلب البيانات وإنشاء الفاتورة) ...
    # ...
    
    # تأكد من أنك تستخدم المتغيرات التي قمنا بتعديلها لجلب رقم الهاتف بأمان
    client_name = booking.user.first_name or booking.user.username 
    client_mobile = "0500000000" 
    
    try:
        profile = booking.user.userprofile 
        if profile.phone_number:
            client_mobile = profile.phone_number
    except:
        pass
    
    # ... (بقية الكود)

    invoice_details = paylink.add_invoice(
        # ...
        client_mobile=client_mobile,
        # ...
    )

    return {
        'transaction_no': invoice_details.transactionNo,
        'payment_url': invoice_details.url
    }