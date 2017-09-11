from common import pickleLoad, pickleDump, sentimentWordLoad


class sentimentAnalysis(object):
    """docstring for sentimentAnalysis"""

    def __init__(self, feature_pair):
        super(sentimentAnalysis, self).__init__()
        self.feature_pair = feature_pair
        # 负面情感词语列表
        # 正面情感词语列表
        self.negative_list, self.positive_list = sentimentWordLoad()
        # print(self.feature_pair[2])

    def sentimentJudge(self):
        '''对评价提取的特征情感词对的情感倾向进行区分'''
        for comment_line in self.feature_pair:
            if len(comment_line) > 1:
                for feature_pair in comment_line[2:]:
                    if feature_pair[1] in self.negative_list:
                        feature_pair[1] = (feature_pair[1], -1)
                    elif feature_pair[1] in self.positive_list:
                        feature_pair[1] = (feature_pair[1], 1)
                    else:
                        feature_pair[1] = (feature_pair[1], 0)

        pickleDump('feature_digit_pair', self.feature_pair)


def main():
    feature_pair = pickleLoad('feature_pair')
    comment_sentiment_analysis = sentimentAnalysis(feature_pair)
    comment_sentiment_analysis.sentimentJudge()


if __name__ == '__main__':
    main()
