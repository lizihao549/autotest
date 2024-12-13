import serial
import logging
from datetime import datetime

# 获取当前时间并格式化为字符串
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file_name = f'command_log_{current_time}.txt'

# 设置日志配置
logging.basicConfig(filename=log_file_name, level=logging.INFO, format='%(asctime)s - %(message)s')

# 串口配置
SERIAL_PORT = 'COM3'  # 根据你的实际串口号修改
BAUD_RATE = 9600  # 波特率，根据设备要求修改
TIMEOUT = 1  # 超时时间

# 指令列表
command_list = [
    'command1',
    'command2',
    'command3',
    # 添加更多指令
]


def send_command(ser, command):
    ser.write((command + '\n').encode('utf-8'))  # 发送指令
    logging.info(f'Sent: {command}')  # 记录日志
    print(f'Sent: {command}')  # 打印到控制台


def read_response(ser):
    response = ''
    while True:
        if ser.in_waiting > 0:
            data = ser.read(ser.in_waiting).decode('utf-8')
            response += data
            logging.info(data)  # 记录日志
            print(data, end='')  # 打印响应到控制台，不换行

            # 检查是否包含结束标志
            if 'HTP>' in response or '<huawei>' in response:
                break
    return response


def main():
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT) as ser:
            for command in command_list:
                send_command(ser, command)  # 发送指令
                read_response(ser)  # 读取并处理每次的响应
                # 在这里不需要 sleep，因为我们会在下一次循环中发送下一条指令

    except serial.SerialException as e:
        logging.error(f'Serial error: {e}')
        print(f'Serial error: {e}')
    except KeyboardInterrupt:
        logging.info('Program interrupted by user.')
        print('Program interrupted by user.')
    except Exception as e:
        logging.error(f'An error occurred: {e}')
        print(f'An error occurred: {e}')


if __name__ == '__main__':
    main()