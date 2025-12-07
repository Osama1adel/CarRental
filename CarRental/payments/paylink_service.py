# from paylink import Paylink, PaylinkProduct
# from django.conf import settings


# paylink = Paylink.test()

# def create_paylink_invoice(booking, callback_url):

#     client_name = booking.user.first_name or booking.user.username 
#     client_mobile = "0500000000" 
    
#     try:
#         profile = booking.user.userprofile 
#         if profile.phone_number:
#             client_mobile = profile.phone_number
#     except:
#         pass
    

#     invoice_details = paylink.add_invoice(
#         client_mobile=client_mobile,
#     )

#     return {
#         'transaction_no': invoice_details.transactionNo,
#         'payment_url': invoice_details.url
#     }