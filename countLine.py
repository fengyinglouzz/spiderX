import os

def run(filename):
    if not os.path.exists(filename):
        return 0
    myfile = open(filename, encoding='utf-8')
    return len(myfile.readlines())

if __name__ == '__main__':
    run()

