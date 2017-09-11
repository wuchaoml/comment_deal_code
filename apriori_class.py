from common import pickleDump, pickleLoad


class ProductFeature(object):
    """docstring for ProductFeature"""

    def __init__(self, noun_list):
        super(ProductFeature, self).__init__()
        # 名词列表
        self.noun_list = list(map(set, noun_list))
        # 名词的所有候选项集的集合
        self.noun_C1_list = []
        # 满足最小支持度的频繁1项集
        self.support_L1_list = []
        # 满足最小支持度的频繁1项集以及对应的支持度字典
        self.support_data = {}
        # 最小支持度
        self.minSupport = 0.01
        # 最小置信度
        self.minConf = 0.05
        # 各阶频繁项集的列表
        self.freaquent_item_list = []
        self.big_rule_list = []
        # 直接创建最初的候选集
        self.createC1()

    def createC1(self):
        '''构建所有候选项的集合'''
        list_C1 = []
        for noun_line_list in self.noun_list:
            for word in noun_line_list:
                if [word] not in list_C1:
                    list_C1.append([word])
        list_C1.sort()
        self.noun_C1_list = list(map(frozenset, list_C1))
        self.support_L1_list, self.support_data = self.scanD(
            self.noun_C1_list)
        pickleDump('noun_C1_list', self.noun_C1_list)
        pickleDump('support_L1_list', self.support_L1_list)

    def scanD(self, frequent_item):
        '''扫描频繁项集并提取满足最小支持度的数据'''
        ssCnt = {}
        support_min_list = []
        support_min_data = {}
        for tid in self.noun_list:
            for can in frequent_item:
                if can.issubset(tid):
                    ssCnt[can] = ssCnt.get(can, 0) + 1
        num_noun_line = float(len(self.noun_list))
        for key in ssCnt.keys():
            support = ssCnt[key] / num_noun_line
            if support >= self.minSupport:
                support_min_list.insert(0, key)
            support_min_data[key] = support
        return support_min_list, support_min_data

    def aprioriGen(self, Lk, k):
        # 根据前一次的频繁项集和k值创建候选项集
        retList = []
        lenLk = len(Lk)
        '''
        没有使用两两之间求并集的方式来创建候选项集，因为有很多重复的，效率较低
        采用的是判断前一次的频繁项集之间前k-2项是否相同
        （其实就是除掉最后一项是否相同，因为k比前一次的频繁项集元素数多一）
        相同的话那代表最后一项绝对不同，直接求并集就可以，减少了重复计算的次数'''
        for i in range(lenLk):
            for j in range(i + 1, lenLk):
                L1 = list(Lk[i])[:k - 2]
                L2 = list(Lk[j])[:k - 2]
                L1.sort()
                L2.sort()
                if L1 == L2:
                    retList.append(Lk[i] | Lk[j])
        # 返回的就是k次的候选项集
        return retList

    def apriori(self):
        # apriori算法不断的循环寻找频繁项集，直到没有更高阶的频繁项集
        self.freaquent_item_list = [self.support_L1_list]
        k = 2
        while(len(self.freaquent_item_list[k - 2]) > 0):
            Ck = self.aprioriGen(self.freaquent_item_list[k - 2], k)
            Lk, supK = self.scanD(Ck)
            # 将每阶频繁项集中高于最低支持度的项加入到满足最小支持度的字典中
            self.support_data.update(supK)
            self.freaquent_item_list.append(Lk)
            print('%d freaquent item list is done!' % (k - 1))
            print(self.freaquent_item_list[k - 2])
            k += 1
        pickleDump('freaquent_item_list', self.freaquent_item_list)
        pickleDump('support_data', self.support_data)

    def generateRules(self):
        for i in range(1, len(self.freaquent_item_list)):
            for freqSet in self.freaquent_item_list[i]:
                H1 = [frozenset([item]) for item in freqSet]
                if (i > 1):
                    self.rulesFromConseq(freqSet, H1)
                else:
                    self.calcConf(freqSet, H1)

    def calcConf(self, freqSet, H):
        prunedH = []
        for conseq in H:
            conf = self.support_data[freqSet] / \
                self.support_data[freqSet - conseq]
            if conf >= self.minConf:
                print(freqSet - conseq, '-->', conseq, 'conf:', conf)
                self.big_rule_list.append((freqSet - conseq, conseq, conf))
                prunedH.append(conseq)
        return prunedH

    def rulesFromConseq(self, freqSet, H):
        m = len(H[0])
        if (len(freqSet) > (m + 1)):
            Hmp1 = self.aprioriGen(H, m + 1)
            Hmp1 = self.calcConf(freqSet, Hmp1)
            if (len(Hmp1) > 1):
                self.rulesFromConseq(freqSet, Hmp1)


def main():

    noun_list = pickleLoad('phone_noun_list')
    product_feature = ProductFeature(noun_list)
    product_feature.apriori()
    product_feature.generateRules()


if __name__ == '__main__':
    main()
