from music21 import converter, note, chord

def extract_first_n_midi_pitches(file_path, n=4):
    """
    Extract the first n MIDI pitches from a MIDI file as a list of integers.
    Chords are represented by the top pitch.
    """
    midi_data = converter.parse(file_path)
    pitches = []

    for el in midi_data.flat.notes:
        if isinstance(el, note.Note):
            pitches.append(el.pitch.midi)
        elif isinstance(el, chord.Chord):
            top_note = max(el.pitches, key=lambda p: p.midi)
            pitches.append(top_note.midi)

        if len(pitches) >= n:
            break

    return pitches
