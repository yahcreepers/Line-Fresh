from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import requests
import random


# 美食抽象類別
class Food(ABC):
    def __init__(self, area = 0):
        pass
    @abstractmethod
    def scrape(self):
        pass
 
 
# 愛食記爬蟲

class Node:
    def __init__(self ,data = None, ind = None, next = None):
        self.data = data
        self.ind = ind
        self.next = next

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
    def print(self):
        cur = self.tail
        while cur != None:
            print(cur.data, cur.ind)
            cur = cur.next
    def delete(self):
        self.tail = self.tail.next
    def Found_insert(self, data, ind):
        new = Node(data, ind)
        if self.tail == None:
            self.head = new
            self.tail = new
            return
        cur = self.tail.next
        pre = self.tail
        while cur != None and cur.data >= data:
            pre = cur
            cur = cur.next
        if cur == None:
            self.head = new
        new.next = pre.next
        pre.next = new
    def Not_Found_insert(self, data, ind):
        new = Node(data, ind)
        if self.tail == None:
            self.head = new
            self.tail = new
            return
        cur = self.tail.next
        pre = self.tail
        while cur != None and cur.data < data:
            pre = cur
            cur = cur.next
        if cur == None:
            self.head = new
        new.next = pre.next
        pre.next = new
class IFoodie(Food):
    def scrape(self):
        content = ""
        K = 0
        for i in range(1, 6):
            response = requests.get(
                "https://ifoodie.tw/explore/list/%E5%B8%AB%E5%A4%A7%E5%A4%9C%E5%B8%82?place=%E5%B8%AB%E5%A4%A7%E5%A4%9C%E5%B8%82&latlng=25.0245418548584%2C121.52936553955078" + "&page=" + str(i))
            soup = BeautifulSoup(response.content, "html.parser")
            # print(soup)
            # 爬取前五筆餐廳卡片資料
            cards = soup.find_all(
                'div', {'class': 'jsx-3440511973 restaurant-info'}, limit=100)
            for card in cards:
                title = card.find(  # 餐廳名稱
                    "a", {"class": "jsx-3440511973 title-text"}).getText()
     
                stars = card.find(  # 餐廳評價
                    "div", {"class": "jsx-1207467136 text"}).getText()
     
                address = card.find(  # 餐廳地址
                    "div", {"class": "jsx-3440511973 address-row"}).getText()
     
     
                #將取得的餐廳名稱、評價及地址連結一起，並且指派給content變數
                content += f"{title}\n{stars}顆星\n{address}\n0\n0\n0\n"
        return content
    def init(self):
        f = open("data.txt", 'r')
        lines = f.readlines()
        self.Data = [[] for i in range(len(lines)//6)]
        for i in range(len(lines)//6):
            for j in range(6):
                self.Data[i].append(lines[6*i+j][:-1])
        #print(Data, len(lines), len(Data))
        self.Data = sorted(self.Data, key = lambda d: d[2])
        #print(self.Data)
        #for i in range(len(self.Data)):
            #print(self.Data[i][2])
    def update(self):
        for i in range(len(self.Data)):
            self.Data[i][3] = random.randint(9, 100)
            self.Data[i][4] = random.randint(1, 15)
            self.Data[i][5] = random.randint(1, 5)
        #print(self.Data)
    def get_close(self, key):
        flag = 0
        pick = [0 for i in range(6)]
        ind = [0 for i in range(6)]
        l = 0
        link = LinkedList()
        ind = 0
        for i in range(len(self.Data)):
            if self.Data[i][0] == key:
                flag = 1
                ind = i
                link = LinkedList()
                l = 0
                break
            count = 0
            for j in self.Data[i][0]:
                if j in key:
                    count += 1
            if count != 0:
                link.Not_Found_insert(count, i)
                l += 1
            if l > 7:
                link.delete()
                l -= 1
        if(flag):
            start = (ind - 10) * (ind - 10 > 0)
            for i in range(10):
                if start + i != ind:
                    link.Found_insert(self.Data[start + i][4]*self.Data[start + i][5], start + i)
                    l += 1
                if l > 7:
                    link.delete()
                    l -= 1
                #print(self.Data[start + i][0], self.Data[start + i][4] * self.Data[start + i][5])
            new = Node(-1, ind)
            link.head.next = new
            link.head = new
            #print(new.ind, link.head.ind)
            l += 1
        #link.print()
        cur = link.tail
        #print(link.head.ind)
        self.link = link
        self.len = l
