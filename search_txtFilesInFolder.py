import os
import sys
import re

def search_files(pattern, directory):
    context_length = 200  # Number of characters around the match
    log_file = "search_logs.txt"  # Log file path

    # Get absolute path of the directory
    directory = os.path.abspath(directory)

    # Check if the directory exists
    if not os.path.isdir(directory):
        print("Invalid directory path.")
        return

    # Compile the pattern as a regular expression
    regex = re.compile(pattern)

    # Iterate over all text files in the directory
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".txt"):
                file_path = os.path.join(root, filename)
                with open(file_path, "r") as file:
                    content = file.read()

                # Search for the pattern in the file contents
                matches = regex.finditer(content)

                if matches:
                    print(f"\nPattern found in file: {file_path}")
                    with open(log_file, "a") as log:
                        for match in matches:
                            start_index = match.start() - context_length
                            if start_index < 0:
                                start_index = 0
                            end_index = match.end() + context_length
                            if end_index > len(content):
                                end_index = len(content)

                            context = content[start_index:end_index]

                            # Log the match and context
                            log.write(f"Match: {match.group()}\n")
                            log.write("Context:\n")
                            log.write(f"{context}\n\n")

                            print(f"Match: {match.group()}")
                            print("Context:")
                            print(context)
                            print()
                else:
                    print(f"Pattern not found in file: {file_path}")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        pattern = sys.argv[1]
        directory = os.getcwd()  # Use current working directory
    elif len(sys.argv) == 3:
        pattern = sys.argv[1]
        directory = sys.argv[2]
    else:
        print("Usage: python search_script.py <pattern> [directory]")
        sys.exit(1)

    search_files(pattern, directory)
