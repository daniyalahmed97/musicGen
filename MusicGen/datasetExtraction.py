import os
import shutil
import pandas as pd

# Paths
csv_path = "pop_songs_data_with_tracks.csv"
midi_root = "Data/clean_midi"
output_folder = "SelectedPopMIDIs"
output_csv = "top_300_pop_songs.csv"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Load the dataset
df = pd.read_csv(csv_path)

# Ensure 'Track Count' and 'Pop Count' columns exist and are valid integers
df = df[df["Track Count"].apply(lambda x: str(x).isdigit())]
df["Track Count"] = df["Track Count"].astype(int)
df["Pop Count"] = pd.to_numeric(df["Pop Count"], errors="coerce").fillna(0).astype(int)

# Filter out MIDI files with fewer than 3 tracks
filtered_df = df[df["Track Count"] >= 3]

# Sort by Pop Count in descending order
filtered_df = filtered_df.sort_values(by="Pop Count", ascending=False)

# Take top 300 songs
top_300_df = filtered_df.head(300)

# Save filtered CSV
top_300_df.to_csv(output_csv, index=False)
print(f"✅ Saved top 300 songs to {output_csv}")


# Clean helper
def clean_filename(name):
    if isinstance(name, str):
        return name.strip().rstrip('.')
    return ""


# Copy matching MIDI files
copied_count = 0
for _, row in top_300_df.iterrows():
    artist = clean_filename(row["Artist Name"])
    song = clean_filename(row["Song Name"])

    artist_dir = os.path.join(midi_root, artist)
    if not os.path.isdir(artist_dir):
        print(f"⚠️ Artist folder not found: {artist}")
        continue

    matched = False
    for file in os.listdir(artist_dir):
        if file.lower().endswith(".mid") and song.lower() in file.lower():
            src_path = os.path.join(artist_dir, file)
            dest_path = os.path.join(output_folder, file)
            shutil.copyfile(src_path, dest_path)
            copied_count += 1
            matched = True
            break

    if not matched:
        print(f"❌ MIDI file not found for: {artist} - {song}")

print(f"\n🎵 Copied {copied_count} MIDI files to '{output_folder}'")
