import serial
import datetime
import csv
import time
import cv2

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

def read_and_record_data(ser, writer):
    line = ser.readline().decode('utf-8').strip()
    heart_value = int(line)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = [timestamp, heart_value]
    writer.writerow(data)
    return heart_value, data

def switch_animation(bpm, cap):
    if bpm >= 100:
        print("心拍数が100bpm以上です。水を飲むアニメーションを再生します。")
        cap.open('drinking.mp4')
    else:
        print("心拍数が100bpm未満です。プレゼンのアニメーションを再生します。")
        cap.open('presentation.mp4')

try:
    cap = cv2.VideoCapture('presentation.mp4')
    if not cap.isOpened():
        print("Error: Cannot open video file.")
        exit()

    with serial.Serial(serial_port, baud_rate) as ser, open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        start_time = time.time()

        while True:
            heart_value, data = read_and_record_data(ser, writer)
            get_count = get_count + 1
            print(get_count, data)

            if (get_count % 200 == 0 and get_count != 0):
                beats_per_minute = beat_count_10seconds * 6
                print(f"10秒毎の平均心拍数: {beats_per_minute} bpm")
                heartbeats.append(beats_per_minute)
                beat_count_10seconds = 0
                switch_animation(beats_per_minute, cap)

            if preValue is None:
                preValue = heart_value
                continue
            elif flag is None:
                flag = heart_value > preValue
                preValue = heart_value
                continue

            if (flag):
                if (preValue > heart_value):
                    beat_count_10seconds = beat_count_10seconds + 1
                    all_beat_count = all_beat_count+1
                    flag = False
                    threshold_count = 1
                preValue = heart_value
            else:
                if ((preValue < heart_value) and (threshold_count > 4)):
                    flag = True
                    threshold_count = 0
                preValue = heart_value
                threshold_count = threshold_count + 1

            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            cv2.imshow('Video', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

except KeyboardInterrupt:
    print("プログラムを終了します")
    print('心拍数: ', all_beat_count)
    print('10秒毎の心拍数: ', heartbeats)
    cap.release()
    cv2.destroyAllWindows()
