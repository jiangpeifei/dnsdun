# coding=utf-8
import os
import threading
from queue import Queue
from dnsdunapi import api


uid = '56104',
api_key = 'DdahszuZQfmXYGTz',
handle = api.Handle(uid, api_key)
# domain_add = handle.domain_add('test.com')
# record_add = handle.record_add(domain='test.com', sub_domain='*', value='1.1.1.1')
# domain_del = handle.domain_del('test.com')

domain_file = input('\n默认域名文件当前目录下domains.txt,直接按回车即可\n自定义文件路径请输入完整域名文件路径(例:/usr/bin/domains.txt)\n:')
if domain_file == '':
    domain_file = 'domains.txt'
with open('domains.txt', 'r', encoding='utf-8') as f:
    domains = [line.rstrip() for line in f.readlines()]

handle_type = input('\n请选择操作类型:\n1:\t添加域名\n2:\t添加解析\n3:\t删除域名\n输入1，2，3进行选择\n:')

print('\n域名数量 %d 个' % len(domains))


class ThreadDomain(threading.Thread, api.Handle):
    def __init__(self, queue, method):
        threading.Thread.__init__(self)
        api.Handle.__init__(self, uid, api_key)
        self.queue = queue
        self.method = method

    def run(self):
        while True:
            # 加锁按顺序输出
            # if mutex.acquire():
            #     item = self.queue.get()
            #     self.domain_add(item)
            #     mutex.release()
            # self.queue.task_done()
            item = self.queue.get()
            if self.method == '1':
                self.domain_add(item)
            if self.method == '3':
                self.domain_del(item)
            if self.method == '2':
                self.record_add(domain=item[0], sub_domain=item[1], value=item[2])
            self.queue.task_done()


de_queue = Queue()

for domain in domains:
    de_queue.put(domain)

# 加锁按顺序输出
# mutex = threading.Lock()

if handle_type == '1':
    print('\n---------开始添加域名---------\n')

    for i in range(10):
        t = ThreadDomain(de_queue, handle_type)
        t.setDaemon(True)
        t.start()

if handle_type == '3':
    print('\n---------开始删除域名---------')

    for i in range(10):
        t = ThreadDomain(de_queue, handle_type)
        t.setDaemon(True)
        t.start()

if handle_type == '2':
    # 获取ips文件并动态生成与服务器对应ip列表
    ips_files = os.listdir('./ips/')
    ips_lists = locals()
    for i in range(len(ips_files)):
        ips_lists['v%d-ips' % i] = [ip.rstrip() for ip in open('./ips/v%d-ips' % i, 'r', encoding='utf-8').readlines()]

    server_number = input('\n请选择需要解析到的服务器:\n1代表v1，以此类推\n输入1，2，3...进行选择\n:')

    # 根据域名数量生成对应服务器ip数量
    len_domains = len(domains)
    ip_list = ips_lists['v%s-ips' % server_number]
    ip_number = len_domains//len(ip_list) + 1
    ips = ip_list * ip_number

    domain_ip = zip(domains, ips)

    sub_domains = input('\n默认解析 @,* ,直接按回车即可:\n自定义主机类型请自行输入并以","隔开(例: www,wap )）\n:')
    default_sub_domains = ['@', '*']
    if sub_domains is not '':
        default_sub_domains.extend(sub_domains.split(','))
    print('\n---------域名需要添加的解析为 %s---------' % ', '.join(default_sub_domains))

    print('\n---------开始添加解析---------\n')

    de_queue = Queue()  # 重置de_queue

    for domain, ip in domain_ip:
        for sub_domain in default_sub_domains:
            de_queue.put((domain, sub_domain, ip))

        for i in range(10):
            t = ThreadDomain(de_queue, handle_type)
            t.setDaemon(True)
            t.start()


de_queue.join()

print('\n---------操作完成,错误域名位于error_domain.txt中---------')
