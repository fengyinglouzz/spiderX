import spiderman
import countLine

if __name__ == '__main__':

    keywordList = ["九寨沟"]
    for i in range(8, 10):
        start = "17-08-0" + str(i) + "-21"
        end = "17-08-0" + str(i) + "-23"
        spiderman.run(keywordList, start, end, ''.join(keywordList) + str(i))

    # 一个或者两个字符串
    # keywordList = ["四川", "地震"]
    # for i in range(1, 10):
    #     start = "18-12-0" + str(i) + "-12"
    #     end = "18-12-0" + str(i) + "-14"
    #     spiderman.run(keywordList, start, end, ''.join(keywordList) + str(i))
    # for i in range(10, 32):
    #     start = "18-12-" + str(i) + "-12"
    #     end = "18-12-" + str(i) + "-14"
    #     spiderman.run(keywordList, start, end, ''.join(keywordList) + str(i))

    # countList = []
    # for i in range(1, 32):
    #     filename = "results/四川地震" + str(i) + ".txt"
    #     substr = '%i'%(i) + ':%s'%(countLine.run(filename))
    #     countList.append(substr)
    # print(countList)
