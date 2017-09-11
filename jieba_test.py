import apriori
import comment_deal
import common
import jieba


def main():
    jieba.load_userdict('../source/dict.txt.big')
    phone_product_reviews = ProductReviews('../source/phone_comment')
    phone_product_reviews.stopWordsLoad('../source/stop_word')
    phone_product_reviews.segSentence()
    print('Comment deal with is OK!')

    product_feature = ProductFeature(phone_product_reviews.noun_list)
    product_feature.apriori()
    for i in product_feature.freaquent_item_list:
        print(str(i))


if __name__ == '__main__':
    main()
