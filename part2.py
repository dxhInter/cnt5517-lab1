import socket_manager
import threading
import time

# 线程控制变量
thread_running = False
humidity_threshold = None

def monitor_humidity():
    global thread_running
    while thread_running:
        # 发送获取湿度的服务调用
        result = socket_manager.send_service_call('Humidity', 'DHT11', ())
        if result[0]:
            humidity = result[1]["Service Result"]
            try:
                # 尝试将湿度转换为浮点数
                humidity_value = float(humidity)
                print(f"Current humidity: {humidity_value}%")
                if humidity_value > humidity_threshold:
                    # 湿度高于阈值，点亮LED
                    result = socket_manager.send_service_call('TurnOnLED', 'LED', ())
                    if result is not None:
                        print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                        if result[0]:
                            print('Result was: {}.'.format(result[1]["Service Result"]))
                        else:
                            print('\nService {} execution failed due to a TCP error.'.format(choice))
                        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
                else:
                    # 湿度不高于阈值，熄灭LED
                    result = socket_manager.send_service_call('TurnOffLED', 'LED', ())
                    if result is not None:
                        print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                        if result[0]:
                            print('Result was: {}.'.format(result[1]["Service Result"]))
                        else:
                            print('\nService {} execution failed due to a TCP error.'.format(choice))
                        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
            except ValueError:
                # 如果转换失败，打印错误信息
                print("Error: Unable to convert humidity to float.")
            else:
                print('\nFailed to get humidity due to a TCP error.\n')
            time.sleep(10)

# 主程序
def main():
    global thread_running, humidity_threshold

    while True:
        print("======================================")
        print("\tg6 ATLAS SERVICES")
        print("======================================")
        print("(1) Turn On LED")
        print("(2) Turn Off LED")
        print("(3) Start Monitoring Humidity")
        print("(6) Exit")
        print("\nEnter your choice:")
        choice = int(input())
        result = None

        if choice == 1:
            result = socket_manager.send_service_call('TurnOnLED', 'LED', ())
        elif choice == 2:
            result = socket_manager.send_service_call('TurnOffLED', 'LED', ())
        elif choice == 3:
            if not thread_running:
                print("Enter humidity threshold:")
                humidity_threshold = float(input())
                thread_running = True
                threading.Thread(target=monitor_humidity, daemon=True).start()
                print("Started monitoring humidity...")
            else:
                print("Humidity monitoring is already running.")
        elif choice == 4:
            # Send call to Turn Off LED
            result = socket_manager.send_service_call('Temperature', 'DHT11', ())
        elif choice == 5:
            # Send call to Turn Off LED
            result = socket_manager.send_service_call('Humidity', 'DHT11', ())
        elif choice == 6:
            print("Bye!")
            thread_running = False
            break
        else:
            print("\nUnsupported choice!\n")

        if result is not None:
            print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            if result[0]:
                print('EXECUTED Choice {}. Result was: {}.'.format(
                    choice, result[1]["Service Result"]))
            else:
                print('\nService {} execution failed due to a TCP error.'.format(choice))
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")

if __name__ == "__main__":
    main()