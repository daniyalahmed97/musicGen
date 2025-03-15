import pandas as pd

# Load the CSV into a DataFrame
input_file = "Data/midi_songs_cleaned_with_genres.csv"
df = pd.read_csv(input_file)

# Create a copy for pop songs
pop_songs = df.copy()

# Function to count occurrences of "pop" in the Genre Tags column
def count_pop_occurrences(genre_tags):
    if not isinstance(genre_tags, str):
        return 0
    genres = genre_tags.lower().split(", ")
    return sum(1 for genre in genres if "pop" in genre)

# Apply the function and store the count in a new column
pop_songs["Pop Count"] = pop_songs["Genre Tags"].apply(count_pop_occurrences)

# Drop rows where "pop" appears only once
#pop_songs = pop_songs[pop_songs["Pop Count"] > 1]

# Sort the DataFrame by "Pop Count" in descending order
pop_songs = pop_songs.sort_values(by="Pop Count", ascending=False)

# Drop the "Pop Count" column before saving
#pop_songs = pop_songs.drop(columns=["Pop Count"])

# Save the filtered data to a new CSV file
output_file = "Data/pop_songs_data.csv"
pop_songs.to_csv(output_file, index=False)

print(f"✅ Pop songs data saved to {output_file}")
