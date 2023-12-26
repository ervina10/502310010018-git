# Import library
import pandas as pd

# Load dataset
goodreads_data = pd.read_csv(r'C:\xampp\htdocs\PM\TM11 _Rekomendasi/goodreads_data.csv', encoding='ISO-8859-1')
print(goodreads_data.head())

# Drop unnecessary columns
columns_to_drop = ['Author', 'Description', 'Num_Ratings', 'URL']
goodreads_data = goodreads_data.drop(columns=columns_to_drop)

# Print the shape and head of the DataFrame
print(goodreads_data.shape)
print(goodreads_data.head())

# User Ratings
userRatings = goodreads_data.pivot_table(index=None, columns=['Book'], values='Avg_Rating')

# Remove NaN values and set a threshold
userRatings = userRatings.dropna(thresh=10, axis=1).fillna(0, axis=1)

print("Before: ", userRatings.shape)
userRatings = userRatings.dropna(thresh=10, axis=1).fillna(0, axis=1)
print("After: ", userRatings.shape)

# Matrix correlation
corrMatrix = userRatings.corr(method='pearson')

# Calculate similarity
def get_similar(genres, rating):
    similar_ratings = corrMatrix[genres] * (rating - 2.5)
    similar_ratings = similar_ratings.sort_values(ascending=False)
    return similar_ratings

# ...

def recommend_books_by_genre(genre_input):
    # Filter books based on the input genre
    genre_books = goodreads_data[goodreads_data['Genres'].apply(lambda x: genre_input.lower() in x.lower())]

    # Sort the books by Avg_Rating in descending order
    genre_books = genre_books.sort_values(by='Avg_Rating', ascending=False)

    # Take the top 5 recommendations
    top_recommendations = genre_books.head(5)['Book'].tolist()
    return top_recommendations

# User input for genre
user_genre_input = input("Masukkan genre buku yang Anda suka: ")

# Get recommendations based on the input genre
genre_recommendations = recommend_books_by_genre(user_genre_input)

# Display top 5 recommendations with book names
print("\nTop 5 Rekomendasi Buku Berdasarkan Genre", user_genre_input, ":")
for i, book in enumerate(recommend_books_by_genre(user_genre_input), 1):
    print(f"{i}. {book}")