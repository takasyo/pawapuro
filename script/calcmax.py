import pulp

from load_data import load_ability, load_basis

ability = load_ability()
basis = load_basis()
extend = load_basis("extend")

# 問題の定義
prob = pulp.LpProblem(name="パワプロ", sense=pulp.LpMaximize)

# 変数の定義
xs = [pulp.LpVariable('{}'.format(x), cat=pulp.LpBinary) for x in ability["得能"]]
ys = [[pulp.LpVariable('{}{}'.format(name, x), cat=pulp.LpBinary) for x in basis[name][name]] for name in basis.keys()]
zs = [[pulp.LpVariable('{}{}'.format(name, x), cat=pulp.LpBinary) for x in extend[name][name]] for name in extend.keys()]

# 目的関数
xx = pulp.lpDot(ability["査定"], xs)
yy = 7.84*(pulp.lpDot([basis[name]["÷7.84"] for name in basis.keys()], ys)*7/6 + 0.5)
zz = pulp.lpDot([extend[name]["査定"] for name in extend.keys()], zs)
prob += pulp.lpSum(xx + yy + zz)

# 制約条件の定義
for j in ["筋力", "敏捷", "技術", "変化", "精神"]:
    x0 = pulp.lpDot(ability[j], xs)
    y0 = pulp.lpSum([pulp.lpDot(basis[name][j], ys[i]) for i, name in enumerate(basis.keys())])
    z0 = pulp.lpSum([pulp.lpDot(extend[name][j], zs[i]) for i, name in enumerate(extend.keys())])
    prob += pulp.lpSum(x0 + y0 + z0) <= 5000

# 下位得能の対応
flag = 0
for i in range(len(ability["得能"])):
    if ability["得能"][i-1] == ability["下位"][i] and flag == 0:
        low = i - 1
        flag = 1
    if ability["得能"][i-1] != ability["下位"][i] and flag == 1:
        up = i
        flag = 0
        prob += pulp.lpSum([xs[j] for j in range(low, up)]) <= 1

for i in range(len(ys)):
    prob += pulp.lpSum(ys[i]) <= 1

for i in range(len(zs)):
    prob += pulp.lpSum(zs[i]) <= 1

# 互換得能の対応
for i in range(len(ability["得能"])):
    if ability["互換"][i] != "":
        for j in range(i+1, len(ability["得能"])):
            if ability["互換"][i] == ability["得能"][j]:
                prob += pulp.lpSum([xs[i], xs[j]]) <= 1

# print(prob)

# 問題を解く
status = prob.solve()
print(pulp.LpStatus[status])

# 結果表示
print("----結果----")
for x in xs:
    if x.value() != 0:
        print(f"{x}:{x.value()}")
for tmp in ys:
    for y in tmp:
        if y.value() != 0:
            print(f"{y}:{y.value()}")
for tmp in zs:
    for z in tmp:
        if z.value() != 0:
            print(f"{z}:{z.value()}")

print(f"\n査定：{pulp.lpSum(xx + yy + zz).value()}")

for j in ["筋力", "敏捷", "技術", "変化", "精神"]:
    x0 = pulp.lpDot(ability[j], xs)
    y0 = pulp.lpSum([pulp.lpDot(basis[name][j], ys[i]) for i, name in enumerate(basis.keys())])
    z0 = pulp.lpSum([pulp.lpDot(extend[name][j], zs[i]) for i, name in enumerate(extend.keys())])
    print(f"{j}：5000に対し {pulp.lpSum(x0 + y0 + z0).value()}")
