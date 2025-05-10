def write_log(message):
    try:
        with open('log.txt', 'a') as file:
            file.write(f"{message}\n")
    except FileNotFoundError:
        with open('log.txt', 'w') as file:
            file.write(f"{message}\n")