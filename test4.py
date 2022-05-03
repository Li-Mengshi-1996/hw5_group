# import urllib.request
# import csv
# import sys
# from queue import PriorityQueue
# import os
#
# ORIGIN = "cs5700cdnorigin.ccs.neu.edu"
#
#
# def get_content(port, path):
#     try:
#         url = "http://" + ORIGIN + ":" + str(port) + path
#         req = urllib.request.urlopen(url)
#         return req.read()
#     except:
#         return b''
#
#
# # result = dict()
#
# # with open('pageviews.csv', newline='') as pages:
# #     lines = csv.reader(pages, delimiter=',')
# #     i = 0
# #     for line in lines:
# #         print(i)
# #         i += 1
# #         path = "/" + line[0]
# #         freq = int(line[1])
# #         result[path] = sys.getsizeof(get_content(8080, path))
# #
# # print(sorted(result.items(), key=lambda kv: (kv[1], kv[0])))
#
# # t_file = open("result.txt", 'a+')
# # t_file.close()
# class Cache:
#     def __init__(self):
#         self.cache_dict = dict()
#         self.size = 20 * 1024 * 1024
#         self.current = 0
#         # self.size = 200000
#         self.freq_dict = self.init_freq()
#         self.pq = PriorityQueue()
#
#     def add(self, path, content):
#         self.cache_dict[path] = content
#         self.current += sys.getsizeof(content)
#
#         if path not in self.freq_dict.keys():
#             self.pq.put((0, path))
#         else:
#             self.pq.put((self.freq_dict[path], path))
#
#         if self.current <= self.size:
#             return
#         else:
#             while self.current > self.size:
#                 item = self.pq.get()
#                 item_path = item[1]
#                 self.current -= sys.getsizeof(self.cache_dict[item_path])
#                 del self.cache_dict[item_path]
#             return
#
#     def get(self, path):
#         if path in self.cache_dict.keys():
#             return self.cache_dict[path]
#         else:
#             return None
#
#     def init_freq(self):
#         result = dict()
#
#         with open('pageviews.csv', newline='') as pages:
#             lines = csv.reader(pages, delimiter=',')
#             for line in lines:
#                 path = "/" + line[0]
#                 freq = int(line[1])
#                 result[path] = freq
#
#         return result
#
#
# cache = Cache()
#
# l = []
#
# with open('pageviews.csv', newline='') as pages:
#     lines = csv.reader(pages, delimiter=',')
#     for line in lines:
#         p = "/" + line[0]
#         l.append(p)
#
# total = 0
# #
# for i in range(0, 100):
#     content = get_content(8080, l[i])
#     cache.add(l[i], content)
#     # print(content)
#     # print(sys.getsizeof(content))
# #
# # # print(cache.get_size())
# # print(len(cache.cache_dict))
# # print(cache.current)
#
# # for i in range(0, len(cache.cache_dict)):
# #     print(l[i] in cache.cache_dict.keys())
#
# f = open('test6.txt','w')
#
# for key in cache.cache_dict.keys():
#     f.write("wget -O z1 http://p5-http-a.5700.network:40004" + key + '\n')
#     # print(key)
#     # command = "wget -O z1 http://p5-http-a.5700.network:40004{}".format(key)
#     # os.system(command)
#     # break
# f.close()
#
# # t_dict = {1: "a", 2: 'b', 3: 'c'}
# #
# # del t_dict[2]
# #
# # print(t_dict)
#
#
#
#

# import os
#
# os.system('wget http://cs5700cdnorigin.ccs.neu.edu:8080/XXXX')

# import socket
#
# print(socket.gethostbyname("p5-http-h.5700.network"))
import math
print(math.pow(0, 2))