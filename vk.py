# -*- coding: UTF-8 -*-
import urllib.request, json, sys
token = 'ihtCD3ens9qxz4cYozK2' #Ваш токен
 
def vk(meth, param):
    url  = "https://api.vk.com/method/%s" %meth
    method = {
        'friends.get'    : 'user_id=%s',
        'users.get'      : 'user_ids=%s' ,
        'groups.get'     : 'user_id=%s&access_token=' + token,
        'groups.getById' : 'group_ids=%s&fields=contacts,description,members_count',
		'groups.getMembers' : 'group_id=%s&fields=city'
    }[meth] %param
 
    binary_data = method.encode('utf8')
    res  = urllib.request.urlopen(url, binary_data).read()
    data = json.loads( res )
   
    if 'error' in data:
        print(data)
        return list()
    return data[u'response']

print(vk('groups.getMembers','narratorika'))