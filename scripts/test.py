import threading


def read_commands():
    try:
        while True:
            command = input()
            print(f'message: {command}')
    except EOFError:
        print("interrupted")


def main():
    t = threading.Thread(target=read_commands)
    t.start()
    t.join()
    print('done')


main()
