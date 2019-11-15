import wmi, time


# myWmi = wmi.WMI()
def get_cpu(ip, user=None, password=None):
    myWmi = wmi.WMI(ip, user=user, password=password)
    cpuArr = myWmi.Win32_Processor()
    for cpu in cpuArr:
        list = ['cpu:', "操作系统位数", cpu.AddressWidth, "计算机名", cpu.SystemName, "处理器位数", cpu.DataWidth, "处理器负载力",
                cpu.loadPercentage, "处理器核心数", cpu.numberOfCores, "处理器最大速度(MHz)", cpu.maxClockSpeed / 1000, "处理器名",
                cpu.name]
        print(list)

