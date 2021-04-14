import csv

def load_file(sense, filename):
    # ファイル読み込み
    with open(filename) as f:
        reader = csv.reader(f)
        l = [row for row in reader]
        l = [list(x) for x in zip(*l)]

    data={l[i][0]:l[i][1:] for i in range(len(l))}

    for i in ["筋力", "敏捷", "技術", "変化", "精神", "査定"]:
        data[i] = list(map(float, data[i]))

    # センス〇
    if sense:
        for i in ["筋力", "敏捷", "技術", "変化", "精神"]:
            data[i] = list(map(lambda x: int(x*0.9), data[i]))

    return data

def load_ability(sense):
    # 特殊能力
    data = load_file(sense, "./data/ability.csv")

    # 下位を合わせた計算
    for i in range(len(data["査定"])):
        if data["下位"][i] != "":
            for j in ["筋力", "敏捷", "技術", "変化", "精神", "査定"]:
                data[j][i] += data[j][i-1]

    # 四捨五入
    data["査定"] = list(map(lambda x: round(x, 2), data["査定"]))

    return data

def load_basis(sense, set="basis"):
    # 基礎能力
    maxlen = 7
    prefix = "b"
    if set == "extend":
        maxlen=2
        prefix="e"

    basis = {}
    for num in range(maxlen):
        data = load_file(sense, f"./data/{prefix}{num}.csv")

        data["÷7.84"] = list(map(float, data["÷7.84"]))

        # 下位を合わせた計算
        for i in range(len(data["査定"])):
            for j in ["筋力", "敏捷", "技術", "変化", "精神"]:
                data[j][i] += data[j][i-1] if i-1 >= 0 else 0

        basis[list(data.keys())[0]] = data

    return basis
