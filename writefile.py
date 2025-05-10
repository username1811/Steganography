def write_file(file, message):
    try:
        with open(file, 'a') as file:
            file.write(f"{message}\n")
    except FileNotFoundError:
        with open(file, 'w') as file:
            file.write(f"{message}\n")