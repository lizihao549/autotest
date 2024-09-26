import telnetlib
import time
import threading

# 后台系统的连接信息
backend_ip = ''
backend_port = 22
backend_username = 'root'
backend_password = 'root'

# 前台ip
switch_ip = '127.0.0.1'
switch_port = 999

# 测试指令列表
test_command_lists = {
    '1': ['测试指令 1', '测试指令 2'],
    '2': ['测试指令 1', '测试指令 2'],
    '3': ['测试指令 1', '测试指令 2'],
}

# 日志文件
log_file = 'test_log.txt'


# 连接到后台系统
def connect_to_backend():
    tn = telnetlib.Telnet(backend_ip, backend_port)
    tn.read_until(b"login: ")
    tn.write(backend_username.encode('ascii') + b"\n")
    tn.read_until(b"Password: ")
    tn.write(backend_password.encode('ascii') + b"\n")
    return tn


# 等待输出中包含 "pass"
def wait_for_pass(tn):
    while True:
        output = tn.read_until(b"pass", timeout=10)  # 等待直到输出中有 "pass"
        log_to_file(output.decode('ascii'))
        if b"pass" in output:
            break


# 连接到交换机并发送指令
def send_commands(tn, commands, stop_event):
    tn.write(f"telnet {switch_ip} {switch_port}\n".encode('ascii'))
    time.sleep(2)

    while not stop_event.is_set():
        for command in commands:
            if stop_event.is_set():
                break
            print(f'执行命令: {command}')
            tn.write(command.encode('ascii') + b"\n")
            wait_for_pass(tn)  # 检查是否打印 "pass"


def log_to_file(message):
    with open(log_file, 'a') as f:
        f.write(message + '\n')


if __name__ == '__main__':
    tn_backend = connect_to_backend()
    stop_event = threading.Event()

    while True:
        #选择测试指令
        print("\n请选择测试指令列表：")
        for key, commands in test_command_lists.items():
            print(f"{key}: {', '.join(commands)}")
        print("q: 退出")

        choice = input("输入选择的指令列表编号（1, 2, 3）：")

        if choice in test_command_lists:
            if choice == '3':
                print("开始循环执行指令列表3，按下 Enter 键取消...")
                thread = threading.Thread(target=send_commands,
                                          args=(tn_backend, test_command_lists[choice], stop_event))
                thread.start()
                input("按 Enter 键停止循环...")
                stop_event.set()  # 设置停止事件
                thread.join()  # 等待线程结束
                print("循环执行已停止。")
            else:
                send_commands(tn_backend, test_command_lists[choice], stop_event)
                print("所有测试指令已执行完毕。")
        elif choice.lower() == 'q':
            print("退出连接。")
            break
        else:
            print("无效的选择！")

    tn_backend.close()
