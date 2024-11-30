import random
import time

# This file is for testing purposes only

def randomize_marbles(input_file, output_file):
    lines = randomize_lines(input_file)
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for i, line in enumerate(lines):
            if(not i==len(lines)-1):
                line = line + "\n"
            outfile.write(line)

def randomize_lines(input_file):
    lines = None
    with open(input_file, 'r') as infile:
        lines = infile.read().splitlines() 
    random.seed(time.time())
    random.shuffle(lines)
    return lines

if __name__ == "__main__":
    # Usage
    output_filename = './marbles_output.txt'
    input_filename = './marbles_output.txt'

    randomize_marbles(input_filename, output_filename)

    print(f"Randomized lines from {input_filename} and saved to {output_filename}.")
