# coding = utf-8

"""
API地址:
http://doc.dnsdun.com/index.html
https://api.dnsdun.com/?c=domain&a=add 添加域名
https://api.dnsdun.com/?c=domain&a=del 删除域名
curl -X POST 'https://api.dnsdun.com/?c=domain&a=del' -d 'format=json&domain=dnsdun.com&api_key=test&uid=1000'
https://api.dnsdun.com/?c=record&a=add 添加记录
https://api.dnsdun.com/?c=record&a=list 记录列表
https://api.dnsdun.com/?c=record&a=modify 修改记录
https://api.dnsdun.com/?c=record&a=del 删除记录
https://api.dnsdun.com/?c=record&a=remark 设置记录备注
https://api.dnsdun.com/?c=record&a=info 获取记录信息
https://api.dnsdun.com/?c=record&a=status 设置记录状态
curl转python requests https://curl.trillworks.com/
"""
import json
import requests


class Handle:
    def __init__(self, uid, api_key):

        self.base_url = 'https://api.dnsdun.com/'

        self.data = {
            'uid': uid,
            'api_key': api_key,
            'format': "json",
        }

    def req(self, api_type, method):
        params = {
            'c': api_type,  # domain/record
            'a': method,  # add/del
        }
        try:
            response = requests.post(self.base_url, params=params, data=self.data, timeout=5)
            response_data = response.content
            ret = json.loads(response_data)
            status_code = int(ret["status"]["code"])
            if status_code == 1:
                print(self.data['domain'], ret["status"]["message"])
                return ret
            else:
                print(self.data['domain'], ret["status"]["message"])
                self.handle_error(ret)
                return
        except Exception as e:
            response_data = '请求错误，请登陆dnsdun检查。错误 ： %s' % e
            print(self.data['domain'], response_data)
            self.handle_error(response_data)
            return

    def domain_add(self, domain):
        self.data['domain'] = domain
        return self.req('domain', 'add')

    def domain_del(self, domain):
        self.data['domain'] = domain
        return self.req('domain', 'del')

    def record_add(self, **kw):
        self.data['record_type'] = 'A',
        self.data['record_line'] = '默认',
        self.data['ttl'] = '600',
        self.data.update(kw)
        return self.req('record', 'add')

    def record_list(self, domain):
        self.data['domain'] = domain
        ret = self.req('record', 'list')
        id_names = dict()
        if ret is not None:
            records = ret["records"]
            for record in records:
                if record['type'] == 'A':
                    id_names[record['name']] = record['id']
        return id_names

    def record_del(self, domain, record_names):
        self.data['domain'] = domain
        domain_records = self.record_list(domain)
        if len(domain_records) >0:
            if record_names is not None:
                # self.data['record_id'] = domain_records[record_name]
                # return self.req('record', 'del')
                for record_name in record_names:
                    self.data['record_id'] = domain_records[record_name]
                    self.req('record', 'del')
            else:
                domain_records = self.record_list(domain)
                for record_name in domain_records.keys():
                    self.data['record_id'] = domain_records[record_name]
                    self.req('record', 'del')

    def handle_error(self, error_message):
        f = open('./error_domain.txt', 'a+')
        error_string = '%s\t%s' % (self.data['domain'], error_message)
        print(error_string, file=f)
