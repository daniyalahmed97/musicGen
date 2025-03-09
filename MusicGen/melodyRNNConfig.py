import os
import magenta.music as mm
from magenta.models.melody_rnn import melody_rnn_sequence_generator
from magenta.models.shared import sequence_generator_bundle


# Path to the pre-trained model
MODEL_BUNDLE_PATH = "magenta_models/basic_rnn.mag"

# Load the model
bundle = sequence_generator_bundle.read_bundle_file(MODEL_BUNDLE_PATH)
generator = melody_rnn_sequence_generator.MelodyRnnSequenceGenerator(
    model=mm.melody_rnn_model.MelodyRnnModel(),
    details=mm.melody_rnn_model.MELODY_RNN_MODEL,
    steps_per_quarter=4,
    bundle=bundle
)
generator.initialize()

# Create a seed melody
seed_sequence = music_pb2.NoteSequence()
mm.testing_lib.add_track_to_sequence(
    seed_sequence, 0, [(60, 80, 0.0, 0.5), (62, 80, 0.5, 1.0), (64, 80, 1.0, 1.5)]
)  # MIDI Notes: C, D, E

# Generate the next 8 bars (~128 steps)
generation_args = generator_pb2.GeneratorOptions()
generation_args.generate_sections.add(
    start_time=seed_sequence.total_time,
    end_time=seed_sequence.total_time + 8.0
)  # Extends melody by 8 bars

generated_sequence = generator.generate(seed_sequence, generation_args)

# Save the output as a MIDI file
mm.sequence_proto_to_midi_file(generated_sequence, "generated_melody.mid")

print("Generated melody saved as 'generated_melody.mid'")
