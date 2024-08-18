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