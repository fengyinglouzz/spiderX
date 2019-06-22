import spiderman
import countLine

if __name__ == '__main__':
    for i in range(1, 10):
        start = "18-12-0" + str(i) + "-12"
        end = "18-12-0" + str(i) + "-14"
        spiderman.run("四川 平安", start, end, "四川 平安" + str(i))
    for i in range(10, 32):
        start = "18-12-" + str(i) + "-12"
        end = "18-12-" + str(i) + "-14"
        spiderman.run("四川 平安", start, end, "四川 平安" + str(i))

    # countList = []
    # for i in range(1, 18):
    #     filename = "results/平安" + str(i) + ".txt"
    #     substr = '%i'%(i) + ':%s' %(countLine.run(filename))
    #     countList.append(substr)
    # print(countList)
