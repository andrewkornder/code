import os


def main():
    if os.name == 'posix':
        print('os is mac')
        os.system('python timer.py')
        os.system('python wordlegame.py')
    elif os.name == 'nt':
        print('os is windows')
        os.system('start timer.py')
        os.system('start testallposs.py')


if __name__ == "__main__":
    main()
