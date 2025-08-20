import pandas as pd
from surprise import dump

# 1. Muat model yang telah dilatih
try:
    # Menggunakan dump.load untuk memuat model dari file
    _, loaded_model = dump.load('recs_model.pkl')
    print("Model berhasil dimuat dari 'recs_model.pkl'")
except FileNotFoundError:
    print("Error: File model 'recs_model.pkl' tidak ditemukan. Pastikan Anda sudah melatih model dan menyimpannya.")
    exit()

# 2. Asumsi: Dapatkan daftar produk yang belum dilihat/dirating oleh pengguna
# Dalam aplikasi nyata, Anda akan mengambil data ini dari database
# Ini adalah daftar produk dummy (contoh)
all_products = ['P100', 'P200', 'P300', 'P400', 'P500', 'P600']
user_rated_products = ['P100', 'P500']  # Contoh produk yang sudah dirating user

# Produk yang belum dirating oleh pengguna
products_to_predict = [p for p in all_products if p not in user_rated_products]

# 3. Menerima input ID pengguna
# Dalam aplikasi, input ini bisa dari form web, API request, dll.
user_id_input = '101'
print(f"\nUser ID yang akan direkomendasikan: {user_id_input}")

# 4. Membuat prediksi rating untuk produk yang belum dirating
predictions = []
for product_id in products_to_predict:
    # Memprediksi rating yang mungkin diberikan user untuk setiap produk
    predicted_rating = loaded_model.predict(user_id_input, product_id)
    predictions.append((predicted_rating.iid, predicted_rating.est))

# 5. Mengurutkan prediksi dari rating tertinggi ke terendah
# dan mengambil 3 produk teratas sebagai rekomendasi
predictions.sort(key=lambda x: x[1], reverse=True)
top_recommendations = predictions[:3]

# 6. Menampilkan hasil
print("\nTop 3 Rekomendasi Produk untuk Anda:")
for product_id, predicted_rating in top_recommendations:
    print(f"  - Produk ID: {product_id} (Prediksi Rating: {predicted_rating:.2f})")