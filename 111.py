
import jieba.analyse

content = open('text.txt', 'r').read()

tags = jieba.analyse.extract_tags(content, withWeight=True, topK=10)
for tag in tags:
    print("tag: %s\t\t weight: %f" % (tag[0], tag[1]))
