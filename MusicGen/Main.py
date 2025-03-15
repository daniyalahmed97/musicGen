from musicVAEConfig import generate_music_vae
from MusicGen.melodyRNNConfig import generate_melody_rnn

bundle_path = "Data/magenta_models/VAE/hierdec-mel_16bar.tar"
config = "hierdec-mel_16bar"
seed_midi = "Data/Seed Melodies/Test/seedmelody.mid"

generate_music_vae(bundle_path, config=config, input_midi=seed_midi)




