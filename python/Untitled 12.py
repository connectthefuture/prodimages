
from collections import defaultdict
from operator import itemgetter
import pprint

l1 = [{"colorstyle":"323901201", "brand":"Gucci", "file_path":"/Retouch_Still/3839/383901201_2.jpg", "alt": "2", "po_type": "asset"}, {"product_type": "slacks", "colorstyle": "334009907", "file_path": "/Retouch_Still/3340/334009907_1.jpg", "alt": "1"}, {"colorstyle": "323991101", "brand": "Fendi", "file_path": "/Retouch_Still/3839/383991101_1.jpg", "alt": "1"}, {"colorstyle": "323901201", "po_number": "123212", "file_path":"/Retouch_Still/3839/383901201_3.jpg", "alt": "3"}, {"file_path":"/Retouch_Still/3340/334009901_1.jpg", "colorstyle":"334009901", "product_type":"dresses", "alt": "1"}]
l2 = [{"colorstyle":"317801301", "file_path":"/Retouch_Fashion/317801301_1.jpg", "alt": "1"}, {"colorstyle": "333991209", "po_type": "consignment-dropship", "brand": "10 Strawberry Street", "file_path": "/Retouch_Fashion/333991209_2.jpg", "alt": "2"}, {"colorstyle": "334009102", "file_path": "/Retouch_Still/3340/334009102_4.jpg", "alt": "4"}, {"file_path": "/Retouch_Still/3340/334009102_2.jpg", "colorstyle":"334009102", "product_type":"dresses", "alt": "2", "po_number":"123212"} ]

d = defaultdict(dict)
i = defaultdict(list)
altpathtuple = defaultdict(list)
keydict = {}
for l in (l1, l2):
    collectpaths = {}
    for field in l:
        altpathtuple[(field['colorstyle'])].append((field['file_path'], field['alt'],))
        try:
            field.pop('file_path')
            field.pop('alt')
        except:
            pass
        d[field['colorstyle']].update(field)
        i[field['colorstyle']].append(altpathtuple)#d['IMAGES'].update(i)
        altpathtuple['data'] = d

print 'dxxxxxxxxxxxx'
test2 = d.items()[2] #keydict
print d, '\n\n\n', '\n'altpathtuple#test2[0]

l3 = d.values()
#l3 = sorted(d.values(), key=itemgetter("colorstyle"))
#l3 is now:
#pprint#l3
#[{'b': 2, 'c': 4, 'index': 1},
# {'b': 3, 'c': 5, 'index': 2},
# {'green': 'eggs', 'index': 3}]
varlist = l3



 
#[ str("{0} is of type {1}".format(k,type(k))) for k in varlist ]


kvpairs = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
dl = defaultdict(list)
for k, v in kvpairs:
    dl[k].append(v)

dl.items()
