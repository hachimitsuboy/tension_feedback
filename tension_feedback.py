import serial
import datetime
import csv
import time

serial_port = '/dev/cu.usbmodem1201'
baud_rate = 38400
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
output_file = 'pulse_data_' + timestamp + '.csv'

preValue = None
threshold_count = 5
get_count = 0
beat_count_10seconds = 0
all_beat_count = 0
heartbeats = []
flag = None  # True: 上昇中, False: 下降中



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

            if (get_count % 200 == 0 and get_count != 0):
                beats_per_minute = beat_count_10seconds * 6  # 10秒間の心拍数 × 6
                print(f"10秒毎の平均心拍数: {beats_per_minute} bpm")
                heartbeats.append(beats_per_minute)
                beat_count_10seconds = 0

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
                    beat_count_10seconds = beat_count_10seconds + 1
                    all_beat_count = all_beat_count+1
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


except KeyboardInterrupt:
    print("プログラムを終了します")
    print('心拍数: ', all_beat_count)
    print('10秒毎の心拍数: ', heartbeats)
