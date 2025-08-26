import sqlite3
import random
from faker import Faker
from datetime import datetime, timedelta

# Inisialisasi Faker untuk data palsu
fake = Faker('id_ID')

def create_and_seed_database(db_name='my-database.db'):
    """
    Creates a new SQLite database with 5 tables and populates them with
    sample data.
    """
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        print(f"Database {db_name} created successfully.")

        # --- DDL: Membuat tabel ---
        print("Creating tables...")
        
        # 1. data_user_profile
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS data_user_profile (
                user_id INTEGER PRIMARY KEY,
                name TEXT,
                gender TEXT,
                age INTEGER,
                location TEXT
            );
        """)

        # 2. data_product_rating
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS data_product_rating (
                rating_id INTEGER PRIMARY KEY,
                user_id INTEGER,
                product_id INTEGER,
                rating INTEGER,
                FOREIGN KEY (user_id) REFERENCES data_user_profile(user_id)
            );
        """)

        # 3. data_user_history_visit_product
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS data_user_history_visit_product (
                history_id INTEGER PRIMARY KEY,
                user_id INTEGER,
                product_id INTEGER,
                visit_count INTEGER,
                FOREIGN KEY (user_id) REFERENCES data_user_profile(user_id)
            );
        """)

        # 4. data_product_reviews
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS data_product_reviews (
                review_id INTEGER PRIMARY KEY,
                user_id INTEGER,
                product_id INTEGER,
                review_text TEXT,
                review_date TEXT,
                FOREIGN KEY (user_id) REFERENCES data_user_profile(user_id)
            );
        """)

        # 5. data_product_transaction_buy
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS data_product_transaction_buy (
                transaction_id INTEGER PRIMARY KEY,
                user_id INTEGER,
                product_id INTEGER,
                transaction_value REAL,
                transaction_date TEXT,
                FOREIGN KEY (user_id) REFERENCES data_user_profile(user_id)
            );
        """)

        # 6. data_product_category_tag_source_country (Diperbarui)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS data_product_category_tag_source_country (
                product_id INTEGER PRIMARY KEY,
                product_name TEXT,
                category TEXT,
                tag TEXT,
                source_country TEXT,
                price REAL,
                brand TEXT
            );
        """)

        conn.commit()
        print("Tables created successfully.")

        # --- DML: Memasukkan data sampel (300 baris) ---
        print("Inserting sample data (300 rows per table)...")
        
        # Data untuk produk (Diperbarui)
        products = []
        categories = ['Elektronik', 'Fashion', 'Makanan', 'Otomotif', 'Kecantikan']
        tags = ['Terlaris', 'Terbaru', 'Diskon', 'Gratis Ongkir']
        countries = ['Indonesia', 'China', 'Korea Selatan', 'Jepang', 'Amerika Serikat']
        
        for i in range(1, 301):
            product_name = fake.word().capitalize() + " " + str(random.randint(10, 99))
            category = random.choice(categories)
            tag = random.choice(tags)
            country = random.choice(countries)
            price = round(random.uniform(10000, 1000000), 2)
            brand = fake.company()
            products.append((i, product_name, category, tag, country, price, brand))
        
        cursor.executemany("INSERT INTO data_product_category_tag_source_country VALUES (?, ?, ?, ?, ?, ?, ?)", products)

        # Data untuk user dan interaksi (Diperbarui)
        for i in range(1, 301):
            user_id = i
            
            # data_user_profile (Diperbarui dengan kolom name)
            name = fake.name()
            gender = random.choice(['Male', 'Female'])
            age = random.randint(18, 60)
            location = fake.city()
            cursor.execute("INSERT INTO data_user_profile VALUES (?, ?, ?, ?, ?)", (user_id, name, gender, age, location))

            # data_product_rating (2-4 rating per user)
            for _ in range(random.randint(2, 4)):
                product_id = random.randint(1, 300)
                rating = random.randint(1, 5)
                cursor.execute("INSERT INTO data_product_rating (user_id, product_id, rating) VALUES (?, ?, ?)", (user_id, product_id, rating))

            # data_user_history_visit_product (2-5 kunjungan per user)
            for _ in range(random.randint(2, 5)):
                product_id = random.randint(1, 300)
                visit_count = random.randint(1, 50)
                cursor.execute("INSERT INTO data_user_history_visit_product (user_id, product_id, visit_count) VALUES (?, ?, ?)", (user_id, product_id, visit_count))

            # data_product_reviews (1-3 review per user)
            for _ in range(random.randint(1, 3)):
                product_id = random.randint(1, 300)
                review_text = fake.sentence()
                review_date = (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d')
                cursor.execute("INSERT INTO data_product_reviews (user_id, product_id, review_text, review_date) VALUES (?, ?, ?, ?)", (user_id, product_id, review_text, review_date))

            # data_product_transaction_buy (1-2 transaksi per user)
            for _ in range(random.randint(1, 2)):
                product_id = random.randint(1, 300)
                transaction_value = round(random.uniform(50000, 5000000), 2)
                transaction_date = (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d')
                cursor.execute("INSERT INTO data_product_transaction_buy (user_id, product_id, transaction_value, transaction_date) VALUES (?, ?, ?, ?)", (user_id, product_id, transaction_value, transaction_date))

        conn.commit()
        print("Sample data inserted successfully.")
        
    except sqlite3.Error as e:
        print(f"An SQLite error occurred: {e}")
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    # Pastikan library faker sudah terinstal
    # pip install faker
    create_and_seed_database()