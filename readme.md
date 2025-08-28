# AI Recommendation System

In the digital age, personalization is key. When we open YouTube, we are immediately presented with videos that match our interests. Spotify plays new songs we'll love, and e-commerce platforms like Tokopedia or Shopee display products we are likely to buy. This is all thanks to an **AI recommendation system**.

This system works like a very smart personal assistant, observing our past behavior (such as videos we watch, songs we listen to, or products we buy) to predict what we'll want next. Its goal is simple: to make the user experience more relevant, efficient, and enjoyable. This architecture I've built mimics that process. By combining user and product data, the system can train an AI model to provide accurate recommendations, similar to how large platforms operate.


## 🧠 Collaborative Filtering (CF) Algorithm

**Collaborative Filtering (CF)** is the most common and powerful recommendation system technique, which is used in this AI model. The basic idea is very simple: If two people (like you and your friend) have had similar tastes in the past, it's highly likely they will have similar tastes in the future. This algorithm doesn't care about the specific features of the product itself; instead, it focuses on **user behavior patterns**.

This system uses a **Model-Based Collaborative Filtering** approach with the **SVD (Singular Value Decomposition)** algorithm. SVD is a matrix factorization technique that predicts user preferences by breaking down a large user-product interaction matrix into a more efficient representation.


## 🛠️ AI Recommendation System Architecture

The system is divided into two main parts: **ETL (Extract, Transform, Load)** and **AI (Artificial Intelligence)**.

### 1\. The ETL Process (Data Pipeline)

This process is responsible for preparing the data to be used by the AI model.

  - **Database and Seeding:** This system uses a SQL database. You can create and populate the database with sample data using the `create_and_seed_db.py` script.

    The database schema consists of tables such as `data_user_profile`, `data_product_reviews`, `data_product_rating`, `data_product_transaction_buy`, and `data_user_history_visit_product`.

  - **Data Extraction, Transformation, and Loading:** The `etl.py` script will take data from the tables above, combine it, and process it into a single CSV file named `data-training.csv`.

    The result is the `data-training.csv` file, which contains all the important information for training the model.


### 2\. The AI Process (Machine Learning)

This part is the "brain" of the system, where recommendations are made.

  - **Installing Dependencies:** Make sure all necessary dependencies are installed from the `requirements.txt` file.

  - **Model Training:** The `data-training.csv` file is used by `training.py` to train the Collaborative Filtering model with the SVD algorithm. Once training is complete, the model is saved as `system-recomendation.pkl`.

  - **Watchdog (Automated Training):** The `watcher.py` script continuously monitors the `data-training.csv` file. If the file changes, Watchdog will automatically trigger the model training process, ensuring the recommendations are always relevant with the latest data.


## 🚀 API and Demonstration

The system is exposed through a **Restful API**, which allows external applications (like mobile or web apps) to request recommendations.

  - **API Service:** Run the `app.py` script to start the API server. This script will load the `system-recomendation.pkl` model and begin serving requests.

  - **API Testing:** You can test the API functionality by sending a `GET` request to the `/recommend/{user_id}` endpoint. For example, `http://127.0.0.1:5000/recommend?user_id=3`.

  - **Recommendation Results:** The API will return recommendations in JSON format, including the products predicted to be liked by the user along with their details, as well as the user's profile data.

This system is designed to be scalable and adaptable, making it a solid foundation for various applications that require product personalization.
