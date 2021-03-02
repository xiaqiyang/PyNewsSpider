import pymongo

# 导入文本分类模块
import sys
sys.path.append(r'E:\news_hotspot_crawler-master\text_classification')
import predict

cnn_model = predict.CnnModel()

class SinaHotspotPipeline(object):
        def __init__(self):
            # 链接数据库
            self.client = pymongo.MongoClient(host='127.0.0.1', port=27017)
            self.db = self.client['SinaNews']  # 获得数据库的句柄

            self.coll1 = self.db['体育']  # 获得collection的句柄
            self.coll2 = self.db['娱乐']
            self.coll3 = self.db['家居']
            self.coll4 = self.db['房产']
            self.coll5 = self.db['教育']
            self.coll6 = self.db['时尚']
            self.coll7 = self.db['时政']
            self.coll8 = self.db['游戏']
            self.coll9 = self.db['科技']
            self.coll0 = self.db['财经']

        def process_item(self, item, spider):

            postItem = dict(item)  # 把item转化成字典形式
            keyword = cnn_model.predict(postItem['abstract'])  # 对文本分类并记录关键词
            postItem['keywords'] = keyword

            if keyword == '体育':
                self.coll1.insert(postItem)  # 向数据库插入一条记录
            elif keyword == '娱乐':
                self.coll2.insert(postItem)
            elif keyword == '家居':
                self.coll3.insert(postItem)
            elif keyword == '房产':
                self.coll4.insert(postItem)
            elif keyword == '教育':
                self.coll5.insert(postItem)
            elif keyword == '时尚':
                self.coll6.insert(postItem)
            elif keyword == '时政':
                self.coll7.insert(postItem)
            elif keyword == '游戏':
                self.coll8.insert(postItem)
            elif keyword == '科技':
                self.coll9.insert(postItem)
            elif keyword == '财经':
                self.coll0.insert(postItem)

            return item  # 在控制台输出原item数据


# 新华网pipelines
class XinhuaHotspotPipeline(object):
    def __init__(self):
        # 链接数据库
        self.client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        self.db = self.client['XinhuaNews']  # 获得数据库的句柄

        self.coll1 = self.db['体育']  # 获得collection的句柄
        self.coll2 = self.db['娱乐']
        self.coll3 = self.db['家居']
        self.coll4 = self.db['房产']
        self.coll5 = self.db['教育']
        self.coll6 = self.db['时尚']
        self.coll7 = self.db['时政']
        self.coll8 = self.db['游戏']
        self.coll9 = self.db['科技']
        self.coll0 = self.db['财经']

    def process_item(self, item, spider):

        postItem = dict(item)  # 把item转化成字典形式
        keyword = cnn_model.predict(postItem['abstract'])  # 对文本分类并记录关键词
        postItem['keywords'] = keyword

        if keyword == '体育':
            self.coll1.insert(postItem)  # 向数据库插入一条记录
        elif keyword == '娱乐':
            self.coll2.insert(postItem)
        elif keyword == '家居':
            self.coll3.insert(postItem)
        elif keyword == '房产':
            self.coll4.insert(postItem)
        elif keyword == '教育':
            self.coll5.insert(postItem)
        elif keyword == '时尚':
            self.coll6.insert(postItem)
        elif keyword == '时政':
            self.coll7.insert(postItem)
        elif keyword == '游戏':
            self.coll8.insert(postItem)
        elif keyword == '科技':
            self.coll9.insert(postItem)
        elif keyword == '财经':
            self.coll0.insert(postItem)

        return item  # 会在控制台输出原item数据，可以选择不写


# 凤凰网pipelines
class FengHuangHotspotPipeline(object):
    def __init__(self):
        # 链接数据库
        self.client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        self.db = self.client['FengHuangNews']  # 获得数据库的句柄

        self.coll1 = self.db['体育']  # 获得collection的句柄
        self.coll2 = self.db['娱乐']
        self.coll3 = self.db['家居']
        self.coll4 = self.db['房产']
        self.coll5 = self.db['教育']
        self.coll6 = self.db['时尚']
        self.coll7 = self.db['时政']
        self.coll8 = self.db['游戏']
        self.coll9 = self.db['科技']
        self.coll0 = self.db['财经']

    def process_item(self, item, spider):

        postItem = dict(item)  # 把item转化成字典形式
        keyword = cnn_model.predict(postItem['abstract'])  # 对文本分类并记录关键词
        postItem['keywords'] = keyword

        if keyword == '体育':
            self.coll1.insert(postItem)  # 向数据库插入一条记录
        elif keyword == '娱乐':
            self.coll2.insert(postItem)
        elif keyword == '家居':
            self.coll3.insert(postItem)
        elif keyword == '房产':
            self.coll4.insert(postItem)
        elif keyword == '教育':
            self.coll5.insert(postItem)
        elif keyword == '时尚':
            self.coll6.insert(postItem)
        elif keyword == '时政':
            self.coll7.insert(postItem)
        elif keyword == '游戏':
            self.coll8.insert(postItem)
        elif keyword == '科技':
            self.coll9.insert(postItem)
        elif keyword == '财经':
            self.coll0.insert(postItem)

        return item  # 会在控制台输出原item数据，可以选择不写



