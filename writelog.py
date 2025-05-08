def write_log(message):
    with open('log.txt', 'a') as file:
        file.write(f"{message}\n")