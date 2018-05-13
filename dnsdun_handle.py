# coding=utf-8
import threading
from queue import Queue
from dnsdunapi import api


uid = '56104',
api_key = 'DdahszuZQfmXYGTz',
handle = api.Handle(uid, api_key)
# domain_add = handle.domain_add('test.com')
# record_add = handle.record_add(domain='test.com', sub_domain='*', value='1.1.1.1')
# domain_del = handle.domain_del('test.com')

domain_file = input('请输入域名文件路径(默认文件当前目录下domains.txt，按回车即可):')
if domain_file == '':
    domain_file = 'domains.txt'
with open('domains.txt', 'r', encoding='utf-8') as f:
    domains = [line.rstrip() for line in f.readlines()]

handle_type = input('请选择操作类型:\n1:\t添加域名\n2:\t添加解析\n3:\t删除域名\n按1，2，3进行选择\n')


class Theeaddomain(threading.Thread):
    def __init__(self, queue, func):
        threading.Thread.__init__(self)
        self.queue = queue
        self.func = func

    def run(self):
        while True:
            # if mutex.acquire():
            #     item = self.queue.get()
            #     handle.domain_add(item)
            #     mutex.release()
            # self.queue.task_done()
            item = self.queue.get()
            self.func(item)
            self.queue.task_done()


if handle_type == '1':
    print('域名数量 %d 个' % len(domains))
    print('---------开始添加域名---------')

    mutex = threading.Lock()

    dequeue = Queue()

    for i in range(10):
        t = Theeaddomain(dequeue, handle.domain_add)
        t.setDaemon(True)
        t.start()

    for domain in domains:
        dequeue.put(domain)

    dequeue.join()


if handle_type == '2':
    pass

if handle_type == '3':
    server_number = input('请选择需要解析到的服务器:\n1\t:v1\n2\t:v2\n3\t:v3\n'
                          '4\t:v4\n5\t:v5\n6\t:v6\n7\t:v7\n8\t:v8\n按1，2，3...进行选择\n')
