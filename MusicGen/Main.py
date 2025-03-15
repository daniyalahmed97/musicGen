import melodyRNNConfig
from MusicGen.melodyRNNConfig import generate_melody

bundle_path = "Data/magenta_models/basic_rnn.mag"
config = "basic_rnn"
seed_midi = "Data/magenta_models/sample.mid"

generate_melody(bundle_path, config)


