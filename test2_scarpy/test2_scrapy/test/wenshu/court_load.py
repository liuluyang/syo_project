import json

court_num = 0
with open('court.json', 'r') as f:
    data = json.load(f)
    for k_t, v_t in data.items():
        print(k_t)
        court_num += 1
        for k_m, v_m in v_t.items():
            print(' '*6, k_m)
            court_num += 1
            for k_b in v_m:
                print(' '*15, k_b)
                court_num += 1
    # p = data['辽宁省']
    # p.pop('辽宁省')
    # print(data['辽宁省'])

# with open('court.json', 'w') as f:
#     json.dump(data, f)
print(court_num)