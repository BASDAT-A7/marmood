from datetime import datetime
from django.db import connection
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from functions.general import query_result

def show_paket(request):
    paket = query_result(f"""
                    SELECT 
                        P.jenis AS jenis_paket,
                        COALESCE(harga, 0) AS harga
                    FROM 
                        paket AS P
                    GROUP BY 
                        P.jenis, harga;
                    """)
    context = {
        'paket': paket,
    }
    return render(request, "paket.html", context)

def detailed_paket(request, jenis_paket):
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with connection.cursor() as cursor:
        cursor.execute("SELECT jenis, harga FROM paket WHERE jenis = %s", [jenis_paket])
        result = cursor.fetchone()
        if result is None:
            raise Http404("Paket does not exist.")
        paket = {
            'jenis_paket': result[0],
            'harga': result[1]
        }
    context = {
        'current_date': current_date,
        'paket': paket
    }
    return render(request, 'detailedpaket.html', context)
    
def riwayat_transaksi(request):
    email = request.COOKIES.get('email')
    riwayat_transaksi = query_result(f"""
                                    SELECT jenis_paket, timestamp_dimulai, timestamp_berakhir, metode_bayar, nominal
                                    FROM TRANSACTION AS T 
                                    JOIN PAKET AS P ON T.jenis_paket = P.jenis
                                    WHERE T.email = %s;
                                    """, [email]) 
    context = {
        'riwayat_transaksi': riwayat_transaksi
    }
    return render(request, 'riwayattransaksi.html', context)

import uuid
from django.shortcuts import render, redirect
from django.db import connection

# def process_payment(request):
#     if request.method == 'POST':


#         roles = request.COOKIES['role']
#         list_role = roles.split(" ")
#         if "Premium" not in list_role:

#             transaction_id = uuid.uuid4()
#             jenis_paket = request.POST.get('jenis_paket')
#             nominal = request.POST.get('nominal')
#             metode_bayar = request.POST.get('metode_bayar')
#             email = request.COOKIES.get('email')
#             timestamp_dimulai = request.POST.get('timestamp_dimulai')
#             timestamp_berakhir = request.POST.get('timestamp_berakhir')

#             with connection.cursor() as cursor:
#                 cursor.execute("""
#                     INSERT INTO TRANSACTION (id, jenis_paket, email, timestamp_dimulai, timestamp_berakhir, metode_bayar, nominal) 
#                     VALUES (%s, %s, %s, %s, %s, %s, %s)
#                 """, [str(transaction_id), jenis_paket, email, timestamp_dimulai, timestamp_berakhir, metode_bayar, nominal])

#                 cursor.execute("""
#                     INSERT INTO PREMIUM (email) VALUES (%s)
#                 """, [email])
#                 connection.commit()

#             return redirect('paket:riwayat_transaksi')  
#         else:
#             return redirect('paket:show_paket')
#     else:
#         return redirect('paket:show_paket')

def process_payment(request): #dengan trigger
    if request.method == 'POST':
        roles = request.COOKIES['role']
        list_role = roles.split(" ")
        if "Premium" not in list_role:
            transaction_id = uuid.uuid4()
            jenis_paket = request.POST.get('jenis_paket')
            nominal = request.POST.get('nominal')
            metode_bayar = request.POST.get('metode_bayar')
            email = request.COOKIES.get('email')
            timestamp_dimulai = request.POST.get('timestamp_dimulai')
            timestamp_berakhir = request.POST.get('timestamp_berakhir')

            try:
                with connection.cursor() as cursor:
                    cursor.callproc('AddPremiumSubscription', [
                        email, jenis_paket, timestamp_dimulai, timestamp_berakhir, metode_bayar, nominal
                    ])
                    connection.commit()
                return redirect('paket:riwayat_transaksi')
            except Exception as e:
                error_message = str(e)  # Get the error message
                return render(request, 'error.html', {'error_message': error_message})
        else:
            return redirect('paket:show_paket')
    else:
        return redirect('paket:show_paket')
