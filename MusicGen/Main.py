import melodyRNNConfig
from MusicGen.melodyRNNConfig import generate_melody
import markovChainConfig as markov

# Configuration

rnn_output_path = 'MusicGen/RNNOutputs'
vae_output_path = "MusicGen/VAEOutputs"
markov_output_path = "MusicGen/MarkovOutputs"

seed_midi_directory = "MusicGen/Seed Melodies/MIDI Files"

# Import Midi Seed Files




# Convert Seed Files to Sequences



# Run Melody RNN generation



# Run Music VAE generation





bundle_path = "Data/magenta_models/basic_rnn.mag"
config = "basic_rnn"
seed_midi = "Data/magenta_models/sample.mid"

generate_melody(bundle_path, config)


#
# # Load and train on corpus
# training_sequences = markov.load_training_sequences('training_midis/')
# chain_counts = markov.train_markov_chain(training_sequences)
# chain = markov.normalize_markov_chain(chain_counts)
#
# # Extract seed
# seed = markov.extract_seed_from_file('seeds/seed1.mid', bars=4)
#
# # Generate new melody
# generated = generate_melody(chain, seed, total_bars=16)
#
# # Save
# markov.save_melody_to_midi(generated, 'generated_seed1_output.mid')

