import pickle


def pickleDump(pickle_file_name, object_name):
    '''序列化保存变量对象'''
    with open('../pickleFile/%s.pickle' % (pickle_file_name), 'wb') as f:
        pickle.dump(object_name, f)


def pickleLoad(pickle_file_name):
    '''序列化读取变量对象'''
    with open('../pickleFile/%s.pickle' % (pickle_file_name), 'rb') as f:
        return pickle.load(f)


def phoneFeatureLoad():
    phone_feature_list = []
    with open('../source/phone_feature.txt', 'r') as f:
        while True:
            feature_word = f.readline().strip()
            if feature_word != '':
                phone_feature_list.append(feature_word)
            else:
                break
    return phone_feature_list


def sentimentWordLoad():
    '''加载情感词语列表'''
    negative_list = []
    positive_list = []
    with open('../source/negative_list.txt', 'r') as f:
        while True:
            negative_word = f.readline().strip()
            if negative_word != '':
                negative_list.append(negative_word)
            else:
                break
        # 情感词汇去重处理
        negative_list = list(set(negative_list))

    with open('../source/positive_list.txt', 'r') as f:
        while True:
            positive_word = f.readline().strip()
            if positive_word != '':
                positive_list.append(positive_word)
            else:
                break
        positive_list = list(set(positive_list))

    return [negative_list, positive_list]
