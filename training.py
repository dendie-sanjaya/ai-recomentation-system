import pandas as pd
from surprise import Dataset, Reader
from surprise.model_selection import train_test_split
from surprise import SVD
from surprise import accuracy

# 1. Muat data dari file CSV
# Karena kita hanya perlu user_id, product_id, dan rating, kita hanya baca kolom tersebut.
file_path = 'recs_data.csv'
df = pd.read_csv(file_path)

# 2. Persiapkan data untuk library Surprise
# Surprise memerlukan objek Reader untuk memahami format data.
# Parameter rating_scale menentukan skala rating (misalnya 1 sampai 5).
reader = Reader(rating_scale=(1, 5))

# Muat DataFrame ke dalam objek Dataset Surprise
data = Dataset.load_from_df(df[['user_id', 'product_id', 'product_rating']], reader)

# 3. Pisahkan data menjadi set pelatihan (trainset) dan pengujian (testset)
# test_size=0.2 berarti 20% data akan digunakan untuk pengujian.
trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

# 4. Pilih dan latih model Collaborative Filtering
# Kita akan menggunakan algoritma SVD (Singular Value Decomposition), yang sangat populer.
# Ini adalah salah satu model berbasis Matrix Factorization.
model = SVD(n_factors=50, n_epochs=20, lr_all=0.005, reg_all=0.02)
model.fit(trainset)

# 5. Prediksi dan evaluasi model
# Lakukan prediksi pada testset
predictions = model.test(testset)

# Hitung metrik evaluasi seperti RMSE (Root Mean Square Error)
# Semakin rendah nilai RMSE, semakin akurat modelnya.
rmse = accuracy.rmse(predictions)

print(f"Model berhasil dilatih dengan RMSE: {rmse}")

# 6. Contoh penggunaan model untuk prediksi rekomendasi
# Misal, kita ingin memprediksi rating yang akan diberikan user '101' untuk produk 'P500'
user_id = '101'
product_id = 'P500'

# Gunakan metode predict() untuk mendapatkan prediksi rating
predicted_rating = model.predict(user_id, product_id)
print(f"\nPrediksi rating user {user_id} untuk produk {product_id} adalah: {predicted_rating.est:.2f}")

# 7. Menyimpan model terlatih (opsional)
# Ini penting agar Anda tidak perlu melatih ulang model setiap kali program dijalankan.
from surprise import dump

dump.dump('recs_model.pkl', algo=model)
print("\nModel berhasil disimpan sebagai 'recs_model.pkl'")