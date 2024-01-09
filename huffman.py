import re
import numpy as np
from PIL import Image

print("Huffman Compression Program")
print("===============================================================")

h = int(input("Press 1 to choose a color image file, or 2 for the default grayscale case: "))

if h == 1:
    file_name = input("Enter the file name: ")
    input_string = np.asarray(Image.open(file_name), np.uint8)
    shape = input_string.shape
    print("Entered string is:", input_string)
    a = input_string
    input_string = str(input_string.flatten().tolist())

elif h == 2:
    array = np.arange(0, 737280, 1, np.uint8)
    input_string = np.reshape(array, (1024, 720))
    print("Entered string is:", input_string)
    a = input_string
    input_string = str(input_string.flatten().tolist())

else:
    print("Invalid input provided")

letters = []
only_letters = []
for letter in input_string:
    if letter not in letters:
        frequency = input_string.count(letter)
        letters.append(frequency)
        letters.append(letter)
        only_letters.append(letter)

nodes = []
while len(letters) > 0:
    nodes.append(letters[0:2])
    letters = letters[2:]
nodes.sort()
huffman_tree = []
huffman_tree.append(nodes)

def combine_nodes(nodes_list):
    position = 0
    new_node = []
    if len(nodes_list) > 1:
        nodes_list.sort()
        nodes_list[position].append("1")
        nodes_list[position + 1].append("0")
        combined_node1 = (nodes_list[position][0] + nodes_list[position + 1][0])
        combined_node2 = (nodes_list[position][1] + nodes_list[position + 1][1])
        new_node.append(combined_node1)
        new_node.append(combined_node2)
        new_nodes = []
        new_nodes.append(new_node)
        new_nodes = new_nodes + nodes_list[2:]
        nodes_list = new_nodes
        huffman_tree.append(nodes_list)
        combine_nodes(nodes_list)
    return huffman_tree

new_nodes = combine_nodes(nodes)

huffman_tree.sort(reverse=True)
print("Huffman tree with merged pathways:")

check_list = []
for level in huffman_tree:
    for node in level:
        if node not in check_list:
            check_list.append(node)
        else:
            level.remove(node)

counter = 0
for level in huffman_tree:
    print("Level", counter, ":", level)
    counter += 1
print()

letter_binary = []
if len(only_letters) == 1:
    letter_code = [only_letters[0], "0"]
    letter_binary.append(letter_code * len(input_string))
else:
    for letter in only_letters:
        code = ""
        for node in check_list:
            if len(node) > 2 and letter in node[1]:
                code = code + node[2]
        letter_code = [letter, code]
        letter_binary.append(letter_code)
print(letter_binary)
print("Binary code generated:")
for letter in letter_binary:
    print(letter[0], letter[1])

bit_string = ""
for character in input_string:
    for item in letter_binary:
        if character in item:
            bit_string = bit_string + item[1]
binary = "0b" + bit_string
print("Your message as binary is:")

uncompressed_file_size = len(input_string) * 7
compressed_file_size = len(binary) - 2
print("Original file size:", uncompressed_file_size, "bits. Compressed size:", compressed_file_size)
print("This results in a saving of", uncompressed_file_size - compressed_file_size, "bits")
output = open("compressed.txt", "w+")
print("Compressed file generated as compressed.txt")
output.write(bit_string)

bit_string = str(binary[2:])
uncompressed_string = ""
code = ""
for digit in bit_string:
    code = code + digit
    position = 0
    for letter in letter_binary:
        if code == letter[1]:
            uncompressed_string = uncompressed_string + letter_binary[position][0]
            code = ""
        position += 1

print("Decoded UNCOMPRESSED data:")
if h == 1:
    temp = re.findall(r'\d+', uncompressed_string)
    result = list(map(int, temp))
    result = np.array(result)
    result = result.astype(np.uint8)
    result = np.reshape(result, shape)
    print(result)
    print("Check if the input and output array shapes match or not.")
    print("Input image dimensions:", shape)
    print("Output image dimensions:", result.shape)
    data = Image.fromarray(result)
    data.save('uncompressed.png')
    if np.array_equal(a, result):
        print("Success")
if h == 2:
    temp = re.findall(r'\d+', uncompressed_string)
    result = list(map(int, temp))
    print(result)
    result = np.array(result)
    result = result.astype(np.uint8)
    result = np.reshape(result, (1024, 720))
    print(result)
    data = Image.fromarray(result)
    data.save('uncompressed.png')
    print("Success")

# Save compressed image
compressed_data = np.array([int(bit_string[i:i + 8], 2) for i in range(0, len(bit_string), 8)], dtype=np.uint8)
compressed_image = np.reshape(compressed_data, shape)
compressed_image = Image.fromarray(compressed_image)
compressed_image.save('compressed_image')
