import os
import subprocess

def generate_music_vae(bundle_path, config, output_dir="/tmp/music_vae/generated",
                        num_outputs=1, temperature=1.0, input_midi=None):
    """
    Generates music using Magenta's MusicVAE with an optional MIDI seed.

    :param bundle_path: Path to the .mag model file
    :param output_dir: Directory to save generated MIDI files
    :param num_outputs: Number of outputs to generate
    :param temperature: Controls randomness (higher = more variation)
    :param input_midi: Path to a seed MIDI file (if using a primer)
    :return: Path to generated MIDI files
    """
    bundle_path = os.path.abspath(bundle_path)
    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    command = [
        "music_vae_generate",
        f"--config={config}",
        f"--checkpoint_file={bundle_path}",
        f"--output_dir={output_dir}",
        f"--num_outputs={num_outputs}",
        f"--temperature={temperature}"
    ]

    if input_midi:
        input_midi = os.path.abspath(input_midi)
        command.append(f"--input_midi={input_midi}")

    print("Running command:", " ".join(command))

    try:
        subprocess.run(command, check=True)
        print(f"Music generated successfully! Check: {output_dir}")
        return output_dir
    except subprocess.CalledProcessError as e:
        print(f"Error running MusicVAE: {e}")
        return None
