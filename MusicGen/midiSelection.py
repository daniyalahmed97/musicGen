import os
import pandas as pd
import pretty_midi

# Paths
csv_path = "Data/pop_songs_data.csv"
midi_root = "Data/clean_midi"

# Load the pop songs CSV
df = pd.read_csv(csv_path)

# Column to store track count
df["Track Count"] = 0  # Default value


def clean_filename(name):
    """Clean song or artist name to match filename/folder, handle NaN/float values safely."""
    if isinstance(name, str):
        return name.strip().rstrip('.')
    return ""



# Iterate through the DataFrame
for index, row in df.iterrows():
    artist = clean_filename(row["Artist Name"])
    song = clean_filename(row["Song Name"])

    if not artist or not song:
        print(f"⚠️ Skipping row {index} due to missing artist or song name.")
        continue

    artist_dir = os.path.join(midi_root, artist)

    if not os.path.isdir(artist_dir):
        print(f"❌ Artist folder not found: {artist}")
        continue

    # Try to find the matching MIDI file
    matching_file = None
    for file in os.listdir(artist_dir):
        if file.lower().endswith(".mid") and song.lower() in file.lower():
            matching_file = os.path.join(artist_dir, file)
            break

    if not matching_file:
        print(f"❌ MIDI file not found for: {artist} - {song}")
        continue

    try:
        midi_data = pretty_midi.PrettyMIDI(matching_file)
        track_count = len(midi_data.instruments)  # Count instrument tracks
        df.at[index, "Track Count"] = track_count
        print(f"✅ {artist} - {song} → {track_count} tracks")
    except Exception as e:
        print(f"⚠️ Error reading {matching_file}: {e}")
        df.at[index, "Track Count"] = "Error"

# Save the updated CSV
df.to_csv("pop_songs_data_with_tracks.csv", index=False)
print("\n🎉 Updated CSV saved as 'pop_songs_data_with_tracks.csv'")
