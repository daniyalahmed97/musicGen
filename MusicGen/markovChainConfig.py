from music21 import converter, note, chord, stream
from collections import defaultdict, Counter
import random
import os

def extract_note_sequence_from_midi(file_path):
    midi_data = converter.parse(file_path)
    part = midi_data.parts[0]  # assume monophonic melody
    notes = []
    for el in part.flat.notes:
        if isinstance(el, note.Note):
            notes.append((el.nameWithOctave, float(el.quarterLength)))
        elif isinstance(el, chord.Chord):
            top = max(el.pitches, key=lambda p: p.midi)
            notes.append((top.nameWithOctave, float(el.quarterLength)))
    return notes

def load_training_sequences(folder_path):
    all_sequences = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.mid') or filename.endswith('.midi'):
            path = os.path.join(folder_path, filename)
            try:
                seq = extract_note_sequence_from_midi(path)
                all_sequences.append(seq)
            except Exception as e:
                print(f"Error with {filename}: {e}")
    return all_sequences

def train_markov_chain(sequences):
    transitions = defaultdict(Counter)
    for seq in sequences:
        for i in range(len(seq) - 1):
            transitions[seq[i]][seq[i + 1]] += 1
    return transitions

def normalize_markov_chain(chain):
    normalized = {}
    for state, counter in chain.items():
        total = sum(counter.values())
        normalized[state] = [(n, count / total) for n, count in counter.items()]
    return normalized

def extract_seed_from_file(seed_path, bars=4, time_signature=4):
    notes = extract_note_sequence_from_midi(seed_path)
    bars_accum = []
    current_time = 0.0
    for n in notes:
        if current_time >= bars * time_signature:
            break
        bars_accum.append(n)
        current_time += n[1]
    return bars_accum


def sample_next_state(prob_list):
    states, probs = zip(*prob_list)
    return random.choices(states, weights=probs)[0]

def generate_melody(chain, seed, total_bars=16, time_signature=4):
    current_state = seed[-1]
    result = seed[:]
    total_time = sum(d for _, d in result)
    max_time = total_bars * time_signature

    while total_time < max_time:
        if current_state not in chain:
            current_state = random.choice(list(chain.keys()))
        current_state = sample_next_state(chain[current_state])
        result.append(current_state)
        total_time += current_state[1]
    return result

def save_melody_to_midi(melody, filename):
    s = stream.Part()
    for pitch, dur in melody:
        n = note.Note(pitch, quarterLength=dur)
        s.append(n)
    s.write('midi', fp=filename)

