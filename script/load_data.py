import csv

def load_ability():
    # 特殊能力
    with open("./data/ability.csv") as f:
        reader = csv.reader(f)
        l = [row for row in reader]
        l = [list(x) for x in zip(*l)]

    data={l[i][0]:l[i][1:] for i in range(len(l))}

    for i in ["筋力", "敏捷", "技術", "変化", "精神", "査定"]:
        data[i] = list(map(float, data[i]))

    # 下位を合わせた計算
    for i in range(len(l[0]) - 1):
        if data["下位"][i] != "":
            for j in ["筋力", "敏捷", "技術", "変化", "精神", "査定"]:
                data[j][i] += data[j][i-1] if i-1 >= 0 else data[j][0]

    return data

def load_basis(set="basis"):
    # 基礎能力
    maxlen = 7
    prefix = "b"
    if set == "extend":
        maxlen=2
        prefix="e"

    basis = {}
    for num in range(maxlen):
        with open(f"./data/{prefix}{num}.csv") as f:
            reader = csv.reader(f)
            l = [row for row in reader]
            l = [list(x) for x in zip(*l)]

        data={l[i][0]:l[i][1:] for i in range(len(l))}

        for i in ["筋力", "敏捷", "技術", "変化", "精神", "査定", "÷7.84"]:
            data[i] = list(map(float, data[i]))

        # 下位を合わせた計算
        for i in range(len(l[0]) - 1):
            for j in ["筋力", "敏捷", "技術", "変化", "精神"]:
                data[j][i] += data[j][i-1] if i-1 >= 0 else data[j][0]
        
        basis[l[0][0]] = data

    return basis
