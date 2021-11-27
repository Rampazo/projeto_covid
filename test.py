import collections

d = [{'create_at': '2021-11-22', 'health_state': 'NO', 'qty': 1}, {'create_at': '2021-11-22', 'health_state': 'NO', 'qty': 1}, {'create_at': '2021-11-22', 'health_state': 'YES', 'qty': 1}]

e = collections.Counter(e['health_state'] == 'NO' for e in d)


print(e)
