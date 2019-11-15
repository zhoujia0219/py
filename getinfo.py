import wmi, time


# myWmi = wmi.WMI()
def get_cpu(ip, user=None, password=None):
    myWmi = wmi.WMI(ip, user=user, password=password)
    cpuArr = myWmi.Win32_Processor()
    for cpu in cpuArr:
        print('cpu:', "操作系统位数", cpu.AddressWidth, "计算机名", cpu.SystemName, "处理器位数", cpu.DataWidth, "处理器负载力",
              cpu.loadPercentage, "处理器核心数", cpu.numberOfCores, "处理器最大速度(MHz)", cpu.maxClockSpeed / 1000, "处理器名",
              cpu.name)


if __name__ == '__main__':
    while True:
        # get_cpu("172.16.77.90", r"weilz", "w2")
        # get_cpu("172.16.77.90", r".\administrator", "www.taobao.com")
        get_cpu("172.16.9.36", r"administrator", "KG8fkC1A")
        # get_cpu("127.0.0.1", r"zhoujia", "142536")
        # get_cpu("127.0.0.1", r".\administrator", "www.taobao.com")
        # get_cpu("127.0.0.1")