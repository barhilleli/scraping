from __future__ import print_function

import cPickle

data_path = 'data1.pkl'

data = cPickle.load(open(data_path, 'rb'))
print(len(data['saved_urls']))
print(*data['saved_urls'],sep='\n')
print('')

print(len(data['visited_urls']))
print(*data['visited_urls'],sep='\n')
print('')

print(len(data['visited_missing_urls']))
print(*data['visited_missing_urls'],sep='\n')
