import uuid
import random
import string

def generate_random_string(length):
    # Generate a random string of specified length consisting of ASCII letters and digits
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_file(filename, num_lines, string_length):
    with open(filename, 'w') as file:
        for _ in range(num_lines):
            # Generate a distinct UUID
            unique_id = str(uuid.uuid4())
            # Generate a random string of specified length
            random_str = generate_random_string(string_length)
            # Write the UUID and random string to the file, separated by a comma
            file.write(f"{unique_id},{random_str}\n")

# Generate a file with 120 lines, each containing a distinct UUID and a random string of 512 characters
generate_file('data.txt', 240, 512)