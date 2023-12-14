import serial
import datetime
import csv
import time

serial_port = '/dev/cu.usbmodem11101'
baud_rate = 38400
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
output_file = 'pulse_data_' + timestamp + '.csv'

preValue = None
threshold_count = 5
get_count = 0
beat_count = 0
heartbeats = []
flag = None  # True: 上昇中, False: 下降中


def calculate_heart_rate(heartbeats, time_window=10):
    beats_per_minute = len(heartbeats) * 6  # 10秒間の心拍数 × 6
    return beats_per_minute


try:
    with serial.Serial(serial_port, baud_rate) as ser, open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        start_time = time.time()

        while True:
            line = ser.readline().decode('utf-8').strip()
            current_time = time.time()
            heart_value = int(line)

            # タイムスタンプはCSV内のデータ用
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data = [timestamp, heart_value]
            writer.writerow(data)
            get_count = get_count + 1
            print(get_count, data)

            # 初期状態の判断
            if preValue is None:
                print('初期値なし')
                preValue = heart_value
                continue
            elif flag is None:
                print('初期値あるけど、波形の向きが決まってない')
                flag = heart_value > preValue
                preValue = heart_value
                continue

            # preValue（初期値）が設定されかつ、心拍波形の向きが決まったら以下が実行される
            if (flag):
                # 上昇中
                if (preValue > heart_value):
                    # 上昇中でピークとなった時
                    beat_count = beat_count + 1
                    flag = False
                    threshold_count = 1
                    print('ピーク -♡-',)

                preValue = heart_value

            else:
                # 下降中
                if ((preValue < heart_value) and (threshold_count > 4)):
                    flag = True
                    print('ボトム')
                    threshold_count = 0
                    preValue = heart_value
                    continue

                preValue = heart_value
                threshold_count = threshold_count + 1

            # 心拍数の計算
            # if heart_value < preValue and flag and threshold_count > 4:
            #     # 波形がピーク（上昇から下降への変化）を示す場合
            #     count += 1
            #     heartbeats.append(heart_value)
            #     threshold_count = 0
            #     flag = False  # 下降フラグに切り替え
            # else:
            #     # ピークが検出されない場合
            #     if heart_value > preValue:
            #         flag = True  # 上昇フラグに切り替え
            #     threshold_count += 1  # 閾値カウンターをインクリメント

            # preValue = heart_value  # 現在の値を保存

            # # 10秒ごとに平均心拍数を計算
            # if current_time - start_time >= time_window:
            #     bpm = calculate_heart_rate(heartbeats)
            #     print(f"10秒毎の平均心拍数: {bpm} bpm")
            #     heartbeats = []
            #     start_time = current_time

except KeyboardInterrupt:
    print("プログラムを終了します")
    print('心拍数: ', beat_count)
