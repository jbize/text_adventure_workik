import os
import json
import argparse

# Instructions: This script opens all "scene" JSON objects from the ./scenes/ directory.
# It will accept the following command line options:
#     --help:-h usage and help
#     --all:-A for all outputs
#     --scenes:-s for missing scenes
#     --images:-b for missing background_image
#     --audio:-a for missing audio_file
# It will provide help/usage if no arguments are provided.
# if --all or --scenes:
#     It will list all "abbrev" files in the "options" list that cannot be found in the ./scenes/ directory along with the "text"
#     add 2 blank lines to output
# if --all or --images:
#     It will list all "background_image" files that cannot be found in the ./static/images/ directory along with the scene description.
#     add 2 blank lines to output
# if --all or --audio:
#     It will list all "audio_file" files that cannot be found in the ./static/audio/ directory along with the scene description.

# Directory paths
scenes_dir = './scenes'
images_dir = './static/images'
audio_dir = './static/audio'

# Lists to store missing files with their corresponding scene descriptions or texts
missing_options = []
missing_images = []
missing_audio = []

# Function to print help/usage message
def print_help():
    print('Usage: python script.py [options]')
    print('Options:')
    print('  --help, -h      Show this help message and exit')
    print('  --all, -A       Check all missing files')
    print('  --scenes, -s    Check missing scene files')
    print('  --images, -b    Check missing background_image files')
    print('  --audio, -a     Check missing audio_file files')

# Parse command line arguments
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('--help', '-h', action='store_true')
parser.add_argument('--all', '-A', action='store_true')
parser.add_argument('--scenes', '-s', action='store_true')
parser.add_argument('--images', '-b', action='store_true')
parser.add_argument('--audio', '-a', action='store_true')
args = parser.parse_args()

# Check for help or no arguments
if args.help or not any([args.all, args.scenes, args.images, args.audio]):
    print_help()
    exit()

# Iterate through the scenes directory
for filename in os.listdir(scenes_dir):
    if filename.endswith('.json'):
        file_path = os.path.join(scenes_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            options = data.get('options', [])
            background_image = data.get('background_image')
            audio_file = data.get('audio_file')
            description = data.get('description', 'No description available')

            # Check for missing "abbrev" files in the "options" list
            if args.all or args.scenes:
                for option in options:
                    abbrev = option.get('abbrev')
                    text = option.get('text', 'No text available')
                    if abbrev and not os.path.exists(os.path.join(scenes_dir, f"{abbrev}.json")):
                        missing_options.append((abbrev, text))

            # Check if the background image file exists in the images directory
            if (args.all or args.images) and background_image and not os.path.exists(os.path.join(images_dir, background_image)):
                missing_images.append((background_image, description))

            # Check if the audio file exists in the audio directory
            if (args.all or args.audio) and audio_file and not os.path.exists(os.path.join(audio_dir, audio_file)):
                missing_audio.append((audio_file, description))

# Function to print results with blank lines
def print_results(type, results):
    if results:
        print(f"Missing {type} files with descriptions:")
        for item, description in results:
            print(f"{type.title()}: {item} - Description: {description}")
        print("\n\n")
    else:
        print(f"All {type} files are present.\n\n")

# Output missing files based on selected options
if args.all or args.scenes:
    print_results('abbrev', missing_options)
if args.all or args.images:
    print_results('background_image', missing_images)
if args.all or args.audio:
    print_results('audio_file', missing_audio)

