import spiderman
import countLine

if __name__ == '__main__':
    for i in range(1, 10):
        start = "18-12-0" + str(i) + "-12"
        end = "18-12-0" + str(i) + "-14"
        spiderman.run("经历", start, end, "经历" + str(i))
    for i in range(10, 32):
        start = "18-12-" + str(i) + "-12"
        end = "18-12-" + str(i) + "-14"
        spiderman.run("经历", start, end, "经历" + str(i))

    # countList = []
    # for i in range(1, 19):
    #     filename = "results/四川" + str(i) + ".txt"
    #     countList.append(countLine.run(filename))
    # print(countList)
