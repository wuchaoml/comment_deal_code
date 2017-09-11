from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time


class jingDong(object):
    """docstring for jingDong"""

    def __init__(self):
        super(jingDong, self).__init__()
        self.driver = webdriver.PhantomJS(
            service_log_path=r"/home/python3/anaconda3/lib/python3.6/site-packages/selenium/webdriver/phantomjs/watchlog.log")
        self.page_num = 1
        self.comment_num = 0
        self.goods = 'mi6'

    def loadPage(self):
        self.driver.get('https://item.jd.com/4099139.html#comment')
        time.sleep(5)
        # soup = bs(self.driver.page_source, 'lxml')
        # self.driver.find_element_by_clstg_name('shangpin|keycount|product|zhongping').click()
        self.driver.find_element_by_xpath("//li[@clstag='shangpin|keycount|product|zhongping']").click()
        time.sleep(2)
        while True:
            soup = bs(self.driver.page_source, 'lxml')
            # comments = soup.find_all(
            #     'div', {'class': 'comment-column J-comment-column'})
            comments = soup.find('div', id='comment-4').find_all('div', class_='comment-column J-comment-column')
            for item in comments:
                comment_level = item.find('div')['class']
                comment_text = item.find('p', {'class': 'comment-con'})
                self.saveFile(comment_level, comment_text)
            try:
                element = self.driver.find_element_by_xpath(
                    "//div[@id='comment']//div[@id='comment-4']//div[@class='ui-page']//a[@clstag='shangpin|keycount|product|pinglunfanye-nextpage']")
            except Exception as e:
                break
            else:
                print('%d page is OK!' % (self.page_num))
            finally:
                self.page_num += 1
                print('Comment total : %d ' % (self.comment_num))
                self.driver.quit()
            # if soup.find('a', {'class': 'ui-pager-next'}) == None:
            #     print('This goods is OK!')
            #     break
            
            
            # self.driver.find_element_by_class_name('ui-pager-next').click()
        
        # self.driver.save_screenshot('/home/python3/python/jingdong.png')
        

    def saveFile(self, comment_level, comment_text):
        self.comment_num += 1
        star = int(str(comment_level[1])[-1])
        # with open('%s_%d_star.txt' % (self.goods, star), 'a') as f:
        #     f.write(str(star) + '\t' + comment_text.get_text() + '\n')
        with open('phone_comment.txt', 'a') as f:  # % (self.goods)
            f.write(comment_text.get_text())
            f.write('\n')


def main():
    jingdong = jingDong()
    jingdong.loadPage()


if __name__ == '__main__':
    main()
