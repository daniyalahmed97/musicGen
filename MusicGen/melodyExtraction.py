from mido import MidiFile, MidiTrack, Message
from collections import defaultdict
import numpy as np

C3_MIDI_NOTE = 48  # MIDI note number for C3


def analyze_track(track, track_index):
    """Analyze a track to determine its monophonic nature, pitch distribution, and phrase structure."""
    note_count = 0
    above_c3_count = 0
    active_notes = set()
    time_stamps = []
    note_sequences = []

    current_time = 0
    for msg in track:
        current_time += msg.time  # Track time progression
        if msg.type == 'note_on' and msg.velocity > 0:
            note_count += 1
            if msg.note >= C3_MIDI_NOTE:
                above_c3_count += 1
            active_notes.add(msg.note)
            note_sequences.append(msg.note)
            time_stamps.append(current_time)
        elif msg.type in ['note_off', 'note_on'] and msg.velocity == 0:
            if msg.note in active_notes:
                active_notes.remove(msg.note)

    # Determine monophony level (lower is better)
    polyphony_score = sum(len(active_notes) > 1 for active_notes in
                          [set(note_sequences[i:i + 2]) for i in range(len(note_sequences) - 1)])

    # Percentage of notes above C3
    above_c3_percentage = (above_c3_count / note_count) if note_count > 0 else 0

    # Identify repeating phrases (4-bar or 8-bar structures)
    phrase_similarity = 0
    if len(note_sequences) > 8:
        split_point = len(note_sequences) // 2
        segment1, segment2 = note_sequences[:split_point], note_sequences[split_point:]
        matching_notes = sum(1 for a, b in zip(segment1, segment2) if a == b)
        phrase_similarity = matching_notes / min(len(segment1), len(segment2))

    print(f"Track {track_index}:")
    print(f"  Total Notes: {note_count}")
    print(f"  Notes above C3: {above_c3_count} ({above_c3_percentage:.2%})")
    print(f"  Monophonic Score: {polyphony_score} (Lower is better)")
    print(f"  Phrase Repetition Similarity: {phrase_similarity:.2%}")
    print("-" * 50)

    return {
        "track": track,
        "index": track_index,
        "polyphony_score": polyphony_score,
        "above_c3_percentage": above_c3_percentage,
        "phrase_similarity": phrase_similarity
    }


def find_melody_track(midi_file_path, output_midi_path):
    """Identifies the melody track based on monophony, note range, and phrase structure, and saves it as a new MIDI file."""
    midi_data = MidiFile(midi_file_path)
    track_analyses = []

    print("\nAnalyzing Tracks...\n")

    for track_index, track in enumerate(midi_data.tracks):
        analysis = analyze_track(track, track_index)
        track_analyses.append(analysis)

    # Sort tracks based on: most monophonic, most notes above C3, most phrase repetition
    track_analyses.sort(
        key=lambda x: (x["polyphony_score"], -x["above_c3_percentage"], -x["phrase_similarity"])
    )

    print("\nSorted Track Scores:")
    for i, t in enumerate(track_analyses):
        print(
            f"{i + 1}. Track {t['index']} | Monophonic: {t['polyphony_score']} | Above C3: {t['above_c3_percentage']:.2%} | Phrases: {t['phrase_similarity']:.2%}")

    # Select the best candidate that meets all criteria
    melody_track = None
    for track_data in track_analyses:
        if track_data["above_c3_percentage"] >= 0.75 and track_data["phrase_similarity"] >= 0.75:
            melody_track = track_data["track"]
            print(f"\nSelected Track {track_data['index']} as the Melody Track!\n")
            break

    if melody_track is None:
        print("\nNo track meets all melody criteria. Selecting the most monophonic track as a fallback.")
        melody_track = track_analyses[0]["track"]
        print(f"Fallback: Selected Track {track_analyses[0]['index']} as the Melody Track!\n")

    # Create a new MIDI file with only the identified melody track
    output_midi = MidiFile()
    new_melody_track = MidiTrack()
    output_midi.tracks.append(new_melody_track)

    for msg in melody_track:
        new_melody_track.append(msg)  # Copy all messages exactly

    output_midi.save(output_midi_path)
    print(f"Melody track isolated and saved to {output_midi_path}")
    return output_midi_path


# Example Usage:
midi_file_path = "Data/clean_midi/Alphaville/Big in Japan.mid"  # Replace with actual MIDI file
melody_output_path = "isolated_melody.mid"
find_melody_track(midi_file_path, melody_output_path)
