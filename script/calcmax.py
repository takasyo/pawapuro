import pulp

from load_data import load_ability, load_basis, load_extend

ability=load_ability()

# 問題の定義
prob = pulp.LpProblem(name="パワプロ", sense=pulp.LpMaximize)

# 変数の定義
xs = [pulp.LpVariable('{}'.format(x), cat='Integer', lowBound=0, upBound=1) for x in ability["得能"]]
# ys = [basis]基礎能力
# zs = [extend]拡張能力

# 目的関数
prob += pulp.lpDot(ability["査定"], xs)
# prob += pulp.lpDot(ability["査定"]+basis["査定"], xs+ys)

# 制約条件の定義
prob += pulp.lpDot(ability["筋力"], xs) <= 500
prob += pulp.lpDot(ability["敏捷"], xs) <= 500
prob += pulp.lpDot(ability["技術"], xs) <= 500
prob += pulp.lpDot(ability["変化"], xs) <= 0
prob += pulp.lpDot(ability["精神"], xs) <= 500

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

print(f"\n査定：{pulp.lpDot(ability['査定'], xs).value()}")
for key in ["筋力", "敏捷", "技術", "変化", "精神"]:
    print(f"{key}：500 に対し {pulp.lpDot(ability[key], xs).value()}")
