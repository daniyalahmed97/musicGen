import os
import subprocess


def ensure_directory_exists(directory):
    """Ensures the output directory exists."""
    os.makedirs(directory, exist_ok=True)


def generate_melody_rnn(bundle_path, config, output_dir="/tmp/melody_rnn/generated", num_outputs=10, num_steps=128,
                        primer_melody="[60]"):
    """
    Generates a melody using Magenta's MelodyRNN CLI tool.

    :param bundle_path: Path to the .mag model file
    :param config: One of 'basic_rnn', 'lookback_rnn', or 'attention_rnn'
    :param output_dir: Directory to save generated MIDI files
    :param num_outputs: Number of melodies to generate
    :param num_steps: Number of time steps (128 ~ 8 bars)
    :param primer_melody: Seed melody as MIDI pitch numbers (e.g., "[60, 62, 64]")
    :return: Path to the generated MIDI files
    """
    bundle_path = os.path.abspath(bundle_path)
    output_dir = os.path.abspath(output_dir)

    ensure_directory_exists(output_dir)

    command = [
        "melody_rnn_generate",
        f"--config={config}",
        f"--bundle_file={bundle_path}",
        f"--output_dir={output_dir}",
        f"--num_outputs={num_outputs}",
        f"--num_steps={num_steps}",
        f"--primer_melody={primer_melody}"
    ]

    print("Running command:", " ".join(command))

    try:
        subprocess.run(command, check=True)
        print(f"Music generated successfully! Check the folder: {output_dir}")
        return output_dir
    except subprocess.CalledProcessError as e:
        print(f"Error running MelodyRNN: {e}")
        return None
