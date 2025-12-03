# payments/paylink_service.py
from paylink import Paylink, PaylinkProduct
from django.conf import settings

# تهيئة كائن Paylink في وضع الاختبار
paylink = Paylink.test()

def create_paylink_invoice(booking, callback_url):
    """
    تنشئ فاتورة Paylink وترجع رقم العملية ورابط الدفع.
    """
    # بما أن نموذج Booking لديك يحتوي على سيارة واحدة، سننشئ منتجاً واحداً
    # يجب التأكد من وجود حقل daily_price في مودل Car
    
    # تحويل اسم العميل، يجب التأكد من وجود حقل الاسم في مودل المستخدم
    client_name = booking.user.get_full_name() or booking.user.username 
    
    # Paylink يتوقع قائمة منتجات حتى لو كانت منتجاً واحداً
    products = [
        PaylinkProduct(
            title=booking.car.name,
            price=float(booking.car.daily_price),
            qty=booking.duration_days # استخدام خاصية duration_days من مودل Booking
        )
    ]
    
    invoice_details = paylink.add_invoice(
        amount=float(booking.total_price), # استخدام total_price المحسوب
        client_mobile="0500000000", # يجب استبدال هذا برقم هاتف العميل
        client_name=client_name,
        order_number=str(booking.id), 
        products=products,
        callback_url=callback_url, 
        currency='SAR'
    )

    return {
        'transaction_no': invoice_details.transactionNo,
        'payment_url': invoice_details.url
    }