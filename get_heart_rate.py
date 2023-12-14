'''
注意事項

- flagをFalseとしているので、心拍波形は必ず下がっている状態になる調整する!
- threshold_countについて
    - 心拍波形は人ぞれぞれでたまに山の後に小山が出てくる時がある。そんな時に小山をピークとしないように、ピークとなってから6プロット(0.3秒)以降でないと谷と判断させないためにある
    
'''


import pandas as pd

# CSVファイルのパス
file_path = '/Users/hacchi/Desktop/3年生データ/3年生中間発表（発表のみ）/南谷くん/南谷くん（発表のみ）.csv'

# Pandasを使ってCSVファイルを読み込む（タイムスタンプと心拍波形値）
# `parse_dates` パラメータを使用して日付と時刻を正確に解析
data = pd.read_csv(file_path, header=None, parse_dates=[0])
timestamps = data[0]  # タイムスタンプ列
heartbeats = data[1]  # 心拍波形値列

preValue = 1000
# 総心拍数
mainCount = 0
# 10秒毎の心拍数
count = 0
# 拍動が2つの山になっている場合（False）からいくつまでは谷とカウントしないか（今回は3以下なら谷とカウントしない）
# 注意: 最大点の次の点はまだthreshold_countは0のまま（配列の要素番号的な感じでややこしい）
# 初回は飛ばしたいので4以上の値に設定しておく
threshold_count = 5
# 5秒あたりの心拍数
countArray = []
# 上昇中はTrue 下降中はFalse
flag = False

for element in range(len(heartbeats)):

    print(
        f"{timestamps[element]} : {element+1}番目 心拍波形値: {heartbeats[element]}")
    print(threshold_count)
    if (element % 200 == 0 and element != 0):
        countArray.append(count)
        count = 0

    if (flag):
        if (preValue > heartbeats[element]):
            mainCount = mainCount + 1
            count = count+1
            flag = False
            print('ピーク')
            print('count: ', count)
            threshold_count = 1
        preValue = heartbeats[element]

    else:

        if ((preValue < heartbeats[element]) and (threshold_count > 4)):
            flag = True
            print('ボトム')
            threshold_count = 0
            preValue = heartbeats[element]
            continue
        preValue = heartbeats[element]
        threshold_count = threshold_count + 1


print('総心拍回数： ', mainCount)
print('10秒おきの心拍数: ', countArray, len(countArray))
duration_seconds = len(timestamps)*0.05
print('平均心拍数: ', mainCount/duration_seconds*60, '回/分')
print('計測時間: ', duration_seconds, '秒')
