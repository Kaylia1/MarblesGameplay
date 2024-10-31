import random

# This file is for testing purposes only

def randomize_lines(input_file, output_file):
    lines = None
    with open(input_file, 'r') as infile:
        lines = infile.read().splitlines() 

    random.shuffle(lines)
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for i, line in enumerate(lines):
            if(not i==len(lines)-1):
                line = line + "\n"
            outfile.write(line)

# Usage
output_filename = './data/marbles_output.txt'
input_filename = './data/marbles_output.txt'

randomize_lines(input_filename, output_filename)

print(f"Randomized lines from {input_filename} and saved to {output_filename}.")
