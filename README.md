# 流量控制与监测


## 配置
- `utils.config.py` 内配置网卡名称
- `main.py` line61 在 `limit_bandwidth` 函数中控制进出方式
- 基于 `tcconfig` 控制网卡，需要 `pip install tcconfig`
- 在`utils.tools.py` 中， `limit_bandwidth` 函数 和 `clear_bandwidth_limit` 分别执行控制和清楚限制命令

## 运行
- `python main.py` 开始流量控制与监测，监测结果文件在 `log/` 目录下
- `python receiver.py` 启动接收端，默认端口 9999
- `python sender.py` 启动发送端，默认端口 9999

## 测试日志

- 2024-08-21 20:01:01 [Debug] 调试两个控制命令之间，流量控制临时失效的问题：`tcset` 不能用--overwrite 参数，得用 --change 参数
- 2024-08-22 09:21:01 [Update] 添加uplink和downlink.py两个文件，加入RPC调用功能
- 2024-08-22 17:21:01 [Debug]  在控制流量的for循环中，两个机器执行for循环的时间不一样
- 2024-08-23 14:58:01 [Debug] 解决了downlink.py运行的机器会卡死的问题，在主函数运行开始时候情况tc配置
- 2024-08-23 16:58:01 [Update] 通过sleep(1-运行时间)的方式控制一个循环始终在1s，在uplink上循环前加了sleep函数矫正同步
- 2024-08-28 09:21:01 [Update] 添加了压力测试功能,在 payload.py 中
- 2024-09-09 10:45:01 [Update] 根据鲁蒙数据，更新了CPU压力测试功能,在 payload-sim.py 中