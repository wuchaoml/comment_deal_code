from common import *
import pandas as pd
import numpy as np
# import subprocess
import matplotlib.pyplot as plot
# from matplotlib.font_manager import FontManager
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score, confusion_matrix, roc_curve
from sklearn import ensemble
from sklearn.linear_model import enet_path


# matplotlib.rcParams['font.family'] = 'SimHei'
# fm = FontManager()
# mat_fonts = set(f.name for f in fm.ttflist)
# output = subprocess.check_output(
#     'fc-list :lang=zh -f "%{family}\n"', shell=True)
# zh_fonts = set(f.split(',', 1)[0] for f in output.decode('utf-8').split('\n'))
# available = mat_fonts & zh_fonts
# print ('*' * 10, '可用的字体', '*' * 10)
# for f in available:
#     print (f)


class machineLearning(object):
    """docstring for machineLearning"""

    def __init__(self, feature_pair):
        super(machineLearning, self).__init__()
        # 特征对列表
        self.feature_pair = feature_pair
        # 对每一条评论的每一个特征最终分数进行统计以后的列表
        self.feature_score = []
        # 每一条评论的特征向量矩阵
        self.feature_matrix = []
        # dataframe格式的评论数据
        self.feature_dataframe = None
        # 训练集和测试集
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None
        # 各级评分数据条数的统计
        self.score_num_total = {}
        # self.artificial_score = []
        # self.loadArtificialScore()
        self.featureScoreTotal()
        self.featureMatrix()
        # self.algorithmSVM()
        self.ensembleRF()

    # def featureScoreTotal(self):
    #     '''评论每一个特征具体得分的统计'''
    #     for feature_pair_line in self.feature_pair:
    #         feature_score_line = feature_pair_line[0:1]
    #         # 用来记录’'total'特征的得分
    #         total_score = 0
    #         # 用来记录评论中的'total'特征的索引
    #         total_index = []
    #         if len(feature_pair_line) > 0:
    #             for feature_one in feature_pair_line[1:]:
    #                 feature = feature_one[0]
    #                 # 每一个特征的最终得分由形容词，程度副词和否定词的乘积得出
    #                 score = feature_one[1][1] * feature_one[2] * feature_one[3]
    #                 # 用来将每条评论的'total'特征的所有得分进行累加作为为最终每条评论的'total'特征的得分
    #                 if feature == 'total':
    #                     total_score += score
    #                     total_index.append(
    #                         feature_pair_line.index(feature_one))
    #                 feature_score_line.append([feature, score])
    #         # 用来删除每条评论中中特征是'total'的元素
    #         for index in total_index[::-1]:
    #             del feature_score_line[index]
    #         # 将每条评论的最终'total'特征加入到列表中
    #         feature_score_line.append(['total', total_score])
    #         self.feature_score.append(feature_score_line)
    #     # pickleDump('feature_score', self.feature_score)
    #     # print(self.feature_score)

    def featureScoreTotal(self):
        '''评论每一个特征具体得分的统计'''
        for feature_pair_line in self.feature_pair:
            feature_score_line = feature_pair_line[0:2]
            # 用来记录’'total'特征的得分
            total_score = 0
            # 用来记录评论中的'total'特征的索引
            total_index = []
            if len(feature_pair_line) > 0:
                for feature_one in feature_pair_line[2:]:
                    feature = feature_one[0]
                    # 每一个特征的最终得分由形容词，程度副词和否定词的乘积得出
                    score = feature_one[1][1] * feature_one[2] * feature_one[3]
                    # 用来将每条评论的'total'特征的所有得分进行累加作为为最终每条评论的'total'特征的得分
                    if feature == 'total':
                        total_score += score
                        total_index.append(
                            feature_pair_line.index(feature_one))
                    feature_score_line.append([feature, score])
            # 用来删除每条评论中中特征是'total'的元素
            for index in total_index[::-1]:
                del feature_score_line[index]
            # 将每条评论的最终'total'特征加入到列表中
            feature_score_line.append(['total', total_score])
            self.feature_score.append(feature_score_line)
        # pickleDump('feature_score', self.feature_score)
        # print(self.feature_score)

    # def featureMatrix(self):
    #     '''将评论的列表处理成矩阵的形式'''
    #     item_feature_list = phoneFeatureLoad()
    #     item_feature_list.append('total')
    #     # 添加网上评分列
    #     item_feature_list.append('score')
    #     matrix_column_num = len(item_feature_list)
    #     for feature_line in self.feature_score:
    #         # 根据列生成一行全为0的列表
    #         feature_matrix_line = [0 for i in range(matrix_column_num)]
    #         # 根据特征将对应行列的值0替换成特征所对应的分数
    #         for feature in feature_line[1:]:
    #             index = item_feature_list.index(feature[0])
    #             feature_matrix_line[index] = feature[1]
    #         feature_matrix_line[-1] = feature_line[0]
    #         if feature_line[0] in self.score_num_total:
    #             self.score_num_total[feature_line[0]] += 1
    #         else:
    #             self.score_num_total[feature_line[0]] = 0
    #         self.feature_matrix.append(feature_matrix_line)
    #     # print(self.feature_matrix)
    #     self.feature_matrix = np.array(self.feature_matrix)
    #     self.feature_dataframe = pd.DataFrame(
    #         self.feature_matrix, columns=item_feature_list)
    #     self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
    #         self.feature_dataframe[item_feature_list[0:-1]], self.feature_dataframe[item_feature_list[-1]], test_size=0.3, random_state=33)
    #     print(len(self.feature_matrix))
    #     # print(self.y_test.value_counts())
    #     # print(self.y_train.value_counts())

    def featureMatrix(self):
        '''将评论的列表处理成矩阵的形式'''
        item_feature_list = phoneFeatureLoad()
        item_feature_list.append('total')
        # 添加专家打分数据列
        item_feature_list.append('artificial_score')
        # 添加网上评分列
        item_feature_list.append('score')
        matrix_column_num = len(item_feature_list)
        for feature_line in self.feature_score:
            # 根据列生成一行全为0的列表
            feature_matrix_line = [0 for i in range(matrix_column_num)]
            if len(feature_line[2:]) <= 2:
                continue
            # 根据特征将对应行列的值0替换成特征所对应的分数
            for feature in feature_line[2:]:
                index = item_feature_list.index(feature[0])
                feature_matrix_line[index] = feature[1]
            feature_matrix_line[-2] = feature_line[1]
            feature_matrix_line[-1] = feature_line[0]
            # 统计各级评分评论的条数
            if feature_line[1] in self.score_num_total:
                self.score_num_total[feature_line[1]] += 1
            else:
                self.score_num_total[feature_line[1]] = 1
            self.feature_matrix.append(feature_matrix_line)
        # print(self.feature_matrix)
        self.feature_matrix = np.array(self.feature_matrix)
        self.feature_dataframe = pd.DataFrame(
            self.feature_matrix, columns=item_feature_list)
        self.feature_dataframe.loc['row_sum'] = self.feature_dataframe.apply(
            lambda x: x.sum())
        self.feature_dataframe.drop(self.feature_dataframe.loc['row_sum']
                                    [self.feature_dataframe.loc['row_sum'] == 0.0].index, axis=1, inplace=True)
        self.feature_dataframe.drop('row_sum', axis=0, inplace=True)

        self.feature_dataframe.iloc[list(self.feature_dataframe[(self.feature_dataframe['artificial_score']
                                                                 == 1) | (self.feature_dataframe['artificial_score'] == 2)].index), -2] = 1
        self.feature_dataframe.iloc[list(self.feature_dataframe[self.feature_dataframe['artificial_score']
                                                                == 3].index), -2] = 2
        self.feature_dataframe.iloc[list(self.feature_dataframe[(self.feature_dataframe['artificial_score']
                                                                 == 4) | (self.feature_dataframe['artificial_score'] == 5)].index), -2] = 3
        # self.feature_dataframe[(self.feature_dataframe['artificial_score'] == 1) | (
        #     self.feature_dataframe['artificial_score'] == 2)]['artificial_score'] = 1
        # self.feature_dataframe[(
        #     self.feature_dataframe['artificial_score'] == 1)]['artificial_score'] = 2
        # self.feature_dataframe[(self.feature_dataframe['artificial_score'] == 4) | (
        #     self.feature_dataframe['artificial_score'] == 5)]['artificial_score'] = 3
        # print(self.feature_dataframe.loc['row_sum']
        #       [self.feature_dataframe.loc['row_sum'] == 0.0].index)
        # self.feature_dataframe.drop('score', axis=1, inplace=True)
        # 将数据进行分割，测试集占总数据的30%
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.feature_dataframe[self.feature_dataframe.columns[0:-2]], self.feature_dataframe[self.feature_dataframe.columns[-2]], test_size=0.3, random_state=33)
        # print(self.y_test.value_counts())
        # print(self.y_train.value_counts())
        print(self.score_num_total)
        # for i in self.feature_matrix:
        #     if i[-1] == 5:
        #         print(i)
        # print(self.feature_dataframe.describe())

    def algorithmSVM(self):
        '''支持向量积模型'''

        # 对数据进行正则化
        ss = StandardScaler()
        self.X_train = ss.fit_transform(self.X_train)
        self.X_test = ss.transform(self.X_test)
        # 训练模型
        lsvc = LinearSVC()
        lsvc.fit(self.X_train, self.y_train)
        y_predict = lsvc.predict(self.X_test)
        print(lsvc.score(self.X_test, self.y_test))
        print(classification_report(self.y_test,
                                    y_predict, target_names=['1', '2', '3']))

    def ensembleRF(self):
        '''集成学习（随机森林）'''
        # 多分类的时候类别标识必须是0,1,2...
        self.y_train -= 1
        self.y_test -= 1
        miss_class_error = []
        # 随机森林中决策数的数量
        ntree_list = range(400, 700, 10)
        for itrees in ntree_list:
            depth = None
            max_feat = 'auto'
            comment_rf_model = ensemble.RandomForestClassifier(
                n_estimators=itrees, max_depth=depth, max_features=max_feat, oob_score=False, random_state=531)
            comment_rf_model.fit(self.X_train, self.y_train)

            prediction = comment_rf_model.predict(self.X_test)
            correct = accuracy_score(self.y_test, prediction)
            miss_class_error.append(1.0 - correct)

        print(len(self.y_test))
        print(len(prediction))

        plot.plot(ntree_list, miss_class_error)
        plot.show()
        feature_importance = comment_rf_model.feature_importances_
        feature_importance = feature_importance / feature_importance.max()
        sorted_idx = np.argsort(feature_importance)
        barPost = np.arange(sorted_idx.shape[0]) + .5
        plot.barh(barPost, feature_importance[sorted_idx], align='center')
        plot.yticks(barPost, self.feature_dataframe.columns[sorted_idx])
        plot.show()
        print('Missclassification Error')
        print(miss_class_error)
        p_list = prediction.tolist()
        confusion_mat = confusion_matrix(self.y_test, p_list)
        print('Confusion Matrix')
        print(confusion_mat)

    # def loadArtificialScore(self):
    #     num = 0
    #     with open('../save_txt/comment_score.txt') as f:
    #         while True:
    #             comment = f.readline()
    #             num += 1
    #             if len(comment) != 0:
    #                 comment_list = comment.split('\t')
    #                 try:
    #                     score = int(comment_list[1])
    #                 except Exception as e:
    #                     print(num)
    #                 else:
    #                     self.artificial_score.append(score)
    #             else:
    #                 break
    #     print(len(self.artificial_score))


def main():
    feature_pair = pickleLoad('feature_digit_pair')
    # print(len(feature_pair))
    # good_num = 0
    # for i in feature_pair:
    #     if i[0] == '4':
    #         good_num += 1

    # print(good_num)
    machine_learning = machineLearning(feature_pair)


if __name__ == '__main__':
    main()
