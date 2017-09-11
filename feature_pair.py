from common import *


class FeaturePair(object):
    """docstring for FeaturePair"""

    def __init__(self, words_list, item_feature_list):
        super(FeaturePair, self).__init__()
        # 评论分词后的列表
        self.words_list = words_list
        # 商品的特征列表
        self.item_feature_list = item_feature_list
        # 各条评论中提取出的特征列表
        self.comment_feature_list = []
        # 特征形容词对（分别是特征值（缺省为‘total），形容词，程度副词等级，否定词）
        self.feature_adj_pair = []
        # 评论计数（用于索引）
        self.comment_num = 0
        # 程度副词列表（most,very,more,-ish,insufficiently,over)
        self.adv_degree_list = []
        # 程度副词综合列表
        self.adv_degree_total = []
        # 否定词列表
        self.deny_word_list = []
        self.emotion_list = sentimentWordLoad()[0] + sentimentWordLoad()[1]
        # 加载程度副词列表
        self.advListLoad()
        # 加载否定词列表
        self.denyWordLoad()
        # 评论中特征值的提取
        self.featureExtract()

    # def commentUniq(self):
    #     words_list_unip = []
    #     for line in self.words_list:
    #         line[1] = tuple(line[1])
    #         line = tuple(line)
    #         words_list_unip.append(line)
    #     self.words_list = []
    #     words_list_unip = list(set(tuple(words_list_unip)))
    #     for line in words_list_unip:
    #         line = list(line)
    #         line[1] = list(line[1])
    #         self.words_list.append(line)
    #     pickleDump('comment_list_uniq', self.words_list)

    def advListLoad(self):
        '''加载程度副词列表'''
        with open('../source/adv_degree.txt', 'r') as f:
            while True:
                adv_level_list = []
                while True:
                    adv_word = f.readline()
                    if adv_word != '\n':
                        adv_word = adv_word.strip()
                        adv_level_list.append(adv_word)
                        self.adv_degree_total.append(adv_word)
                    else:
                        self.adv_degree_list.append(adv_level_list)
                        break
                if len(adv_level_list) == 0:
                    self.adv_degree_list.pop()
                    break

    def denyWordLoad(self):
        '''加载否定词列表'''
        with open('../source/deny_list.txt', 'r') as f:
            deny_word = f.read().strip()
            self.deny_word_list = deny_word.split('、')

    # def featureExtract(self):
    #     '''提取各条评论中的特征列表'''
    #     for words_list_line in self.words_list:
    #         line_feature_list = [
    #             feature for feature in words_list_line[1] if feature[0] in self.item_feature_list]
    #         self.comment_feature_list.append(line_feature_list)

    def featureExtract(self):
        '''提取各条评论中的特征列表'''
        for words_list_line in self.words_list:
            line_feature_list = [
                feature for feature in words_list_line[2] if feature[0] in self.item_feature_list]
            self.comment_feature_list.append(line_feature_list)

    def featureAdjPair(self):
        '''提取各条评论中的特征形容词对'''
        for line_feature_list in self.comment_feature_list:
            # 各条评论列表
            line_comment = self.words_list[self.comment_num]
            # 各条评论中的特征形容词对的列表
            line_feature_adj = []
            line_feature_adj.append(line_comment[0])
            line_feature_adj.append(line_comment[1])
            # 如果评论中含有特征则提取特征形容词对组成的元组
            if len(line_feature_list) != 0:
                for feature in line_feature_list:
                    feature_index = line_comment[-1].index(feature)
                    # list(filter(lambda feature_seg: feature_seg[0] == feature, line_comment))[0])
                    # 形容词标志，特征前后有形容词修饰则为True，否则为False，此时单独处理
                    adj_flag = False
                    # 在特征词的前后三个位置寻找形容词
                    for word_index in range(feature_index - 3, feature_index + 4):
                        # 防止索引越界
                        if (word_index < len(line_comment[-1])) & (word_index >= 0):
                            # if line_comment[-1][word_index][1] in ['a', 'an', 'ag', 'al']:
                            if line_comment[-1][word_index][0] in self.emotion_list:
                                adj_flag = True
                                degree_tuple = self.featureAdvPair(
                                    line_comment, word_index)
                                line_feature_adj.append(
                                    [feature[0], line_comment[-1][word_index][0], degree_tuple[0], degree_tuple[1]])
                        else:
                            continue
                    # 如果特征不存在形容词修饰，就当成中性处理
                    if adj_flag == False:
                        line_feature_adj.append([feature[0], 0, 0, 1])
            # 如果不含特征则直接提取形容词列表
            else:
                for word_index in range(0, len(line_comment[-1])):
                    # if line_comment[-1][word_index][1] in ['a', 'an', 'ag', 'al']:
                    if line_comment[-1][word_index][0] in self.emotion_list:
                        degree_tuple = self.featureAdvPair(
                            line_comment, word_index)
                        line_feature_adj.append(
                            ['total', line_comment[-1][word_index][0], degree_tuple[0], degree_tuple[1]])
            print(line_feature_adj)
            self.feature_adj_pair.append(line_feature_adj)
            self.comment_num += 1
        pickleDump('feature_pair', self.feature_adj_pair)

    def featureAdvPair(self, line_comment, word_index):
        '''根据提取到的形容词提取修饰的副词'''
        # 如果提取到的形容词前一位不是副词则判断是否是否定词
        if word_index - 1 >= 0:
            if line_comment[-1][word_index - 1][0] not in self.adv_degree_total:
                negative_degree = self.featureNegative(
                    line_comment, word_index, 'a')
                return (1, negative_degree)
            # 如果是副词则判断副词的程度并且判断副词的前一位是否是否定词
            else:
                for degree_list in self.adv_degree_list:
                    if line_comment[-1][word_index - 1][0] in degree_list:
                        negative_degree = self.featureNegative(
                            line_comment, word_index - 1, 'd')
                        return (5 - self.adv_degree_list.index(degree_list), negative_degree)
                negative_degree = self.featureNegative(
                    line_comment, word_index - 1, 'none')
                return (1, negative_degree)
        else:
            return (1, 1)

    def featureNegative(self, line_comment, word_index, word_class):
        '''根据提取到的形容词或副词提取修饰的否定词'''
        # 判断是否有否定词并判断其是对副词还是形容词进行的修饰
        # 如果是对形容词进行的修饰，则情感倾向是完全相反的
        # 如果是对副词进行的修饰，则副词的修饰程度有所减弱，暂定减少一半
        if word_class == 'd':
            if line_comment[-1][word_index - 1][0] in self.deny_word_list:
                return 0.5
            else:
                return 1
        elif word_class == 'a':
            if line_comment[-1][word_index - 1][0] in self.deny_word_list:
                return -1
            else:
                return 1
        else:
            return 0.5


def main():
    words_list = pickleLoad('artificial_comment')
    phone_feature_list = phoneFeatureLoad()
    feature_pair = FeaturePair(words_list, phone_feature_list)
    feature_pair.featureAdjPair()


if __name__ == '__main__':
    main()
