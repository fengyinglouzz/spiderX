def run(filename):
    myfile = open(filename, encoding='utf-8')
    return len(myfile.readlines())

if __name__ == '__main__':
    run()

