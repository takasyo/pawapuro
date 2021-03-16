import csv

def load_ability():
    # 特殊能力

    with open("./data/special_ability.csv") as f:
        reader = csv.reader(f)
        l = [row for row in reader]
        l = [list(x) for x in zip(*l)]

    data={l[i][0]:l[i][1:] for i in range(len(l))}

    for i in ["筋力", "敏捷", "技術", "変化", "精神", "査定"]:
        data[i] = list(map(float, data[i]))

    # 下位を合わせた計算
    for i in range(len(data["得能"])):
        if data["下位"][i] != "":
            for j in ["筋力", "敏捷", "技術", "変化", "精神", "査定"]:
                data[j][i] += data[j][i-1]

    return data

def load_basis():
    # 基礎能力
    pass

def load_extend():
    # 拡張能力
    pass
