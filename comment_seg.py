import jieba
import jieba.posseg as pseg
from common import pickleDump, pickleLoad


class ProductReviews(object):
    """docstring for ProductReviews"""

    def __init__(self, product_comment_file_name):
        super(ProductReviews, self).__init__()
        # 评论文件的名称
        self.product_comment_file_name = product_comment_file_name
        # 停止词列表
        self.stop_words_list = []
        # 分词和词性标注后的列表
        self.words_posseg = []
        # 商品评论的数量
        self.line_num = 0
        # 名词列表
        self.noun_list = []
        self.level_num_total = {}
        self.comment_list_uniq = []

    def stopWordsLoad(self, stop_words_name):
        '''加载停止词列表'''
        with open('%s.txt' % (stop_words_name), 'r') as f:
            while True:
                stop_word = f.readline().strip()
                if len(stop_word) != 0:
                    self.stop_words_list.append(stop_word)
                else:
                    break
        # pickleDump('stop_words_list', self.stop_words_list)
        print('Stop words is OK!')

    # def segSentence(self):
    #     '''分词以及词性标注'''
    #     with open('%s.txt' % (self.product_comment_file_name), 'r') as f:
    #         while True:
    #             line = f.readline().strip()
    #             if len(line) != 0:
    #                 if line in self.comment_list_uniq:
    #                     continue
    #                 else:
    #                     self.comment_list_uniq.append(line)
    #                     # self.saveFile(line, 'comment_uniq')
    #                 line = line.split('\t')

    #                 # seg_list = jieba.cut(line, cut_all=False, HMM=True)

    #                 try:
    #                     words = pseg.cut(line[1])
    #                 except Exception as e:
    #                     continue
    #                 try:
    #                     line_score = int(line[0])
    #                     if line_score not in range(1, 6):
    #                         continue
    #                 except Exception as e:
    #                     continue
    #                 else:
    #                     self.level_num_total.setdefault(line_score, 0)
    #                     if self.level_num_total[line_score] >= 1500:
    #                         continue
    #                     self.level_num_total[line_score] += 1
    #                 self.line_num += 1
    #                 self.wordDeal(line_score, words)
    #                 # self.saveFile(line[0] + '\t' + line[1], 'comment_score')
    #             else:
    #                 print(len(self.words_posseg))
    #                 # print(self.words_posseg[3])
    #                 # pickleDump('words_posseg', self.words_posseg)
    #                 # pickleDump('noun_list', self.noun_list)
    #                 # pickleDump('comment_uniq', self.comment_list_uniq)
    #                 print(self.level_num_total)
    #                 break

    def segSentence(self):
        '''分词以及词性标注'''
        with open('%s.txt' % (self.product_comment_file_name), 'r') as f:
            while True:
                line = f.readline().strip()
                if len(line) != 0:
                    if line in self.comment_list_uniq:
                        continue
                    else:
                        self.comment_list_uniq.append(line)
                        # self.saveFile(line, 'comment_uniq')
                    line = line.split('\t')

                    # seg_list = jieba.cut(line, cut_all=False, HMM=True)

                    try:
                        line_score = int(line[0])
                        if line_score not in range(1, 6):
                            continue
                    except Exception as e:
                        continue
                    try:
                        line_artificial_score = int(line[1])
                        if line_artificial_score not in range(1, 6):
                            continue
                    except Exception as e:
                        continue
                    try:
                        words = pseg.cut(line[-1])
                    except Exception as e:
                        continue
                    self.level_num_total.setdefault(line_score, 0)
                    if self.level_num_total[line_score] >= 1500:
                        continue
                    self.level_num_total[line_score] += 1
                    self.line_num += 1
                    self.wordDeal(line_score, line_artificial_score, words)
                    self.saveFile(line[0] + '\t' + line[1] +
                                  '\t' + line[2], 'comment_score')
                else:
                    print(len(self.words_posseg))
                    pickleDump('artificial_comment', self.words_posseg)
                    # pickleDump('noun_list', self.noun_list)
                    # pickleDump('comment_uniq', self.comment_list_uniq)
                    print(self.level_num_total)
                    break

    def wordDeal(self, line_score, line_artificial_score, words):
        '''分词后的数据处理，去掉停止词以及提取其中的名词'''
        words_posseg_line = []
        noun_line_list = []
        for word, flag in words:
            # 判断是否是停止词
            if word not in self.stop_words_list:
                if flag in ['n', 'nz', 'nl', 'ng', 'v', 'vn']:
                    noun_line_list.append(word)
                words_posseg_line.append((word, flag))
            else:
                continue
        self.words_posseg.append(
            [line_score, line_artificial_score, words_posseg_line])
        self.noun_list.append(noun_line_list)
        # if self.line_num == 1000:
        #     pickleDump('noun_list_small', self.noun_list)
        # 保存文件
        # self.saveFile(noun_line_list, 'noun_word_total')
        # self.saveFile([line_score, words_posseg_line], 'seg_comment')
        print('The %d line deal with is done!' % (self.line_num))

    # def wordDeal(self, line_score, words):
    #     '''分词后的数据处理，去掉停止词以及提取其中的名词'''
    #     words_posseg_line = []
    #     noun_line_list = []
    #     for word, flag in words:
    #         # 判断是否是停止词
    #         if word not in self.stop_words_list:
    #             if flag in ['n', 'nz', 'nl', 'ng', 'v', 'vn']:
    #                 noun_line_list.append(word)
    #             words_posseg_line.append((word, flag))
    #         else:
    #             continue
    #     self.words_posseg.append([line_score, words_posseg_line])
    #     self.noun_list.append(noun_line_list)
    #     # if self.line_num == 1000:
    #     #     pickleDump('noun_list_small', self.noun_list)
    #     # 保存文件
    #     # self.saveFile(noun_line_list, 'noun_word_total')
    #     # self.saveFile([line_score, words_posseg_line], 'seg_comment')
    #     print('The %d line deal with is done!' % (self.line_num))

    def saveFile(self, words_line, file_name):
        '''以字符串的形式保存文件函数'''
        with open('../save_txt/%s.txt' % (file_name), 'a') as f:
            f.write(str(words_line))
            f.write('\n')


def main():
    jieba.load_userdict('../source/dict.txt.big')
    # phone_product_reviews = ProductReviews('../source/phone_score_comment')
    phone_product_reviews = ProductReviews('../save_txt/comment_score')
    phone_product_reviews.stopWordsLoad('../source/stop_word')
    phone_product_reviews.segSentence()
    print('Comment deal with is OK!')


if __name__ == '__main__':
    main()
