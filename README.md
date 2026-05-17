# yzu-wlan

扬州大学校园网自动登录工具。

零外部依赖，仅使用 Python 标准库。

## 安装

```bash
pip install --user git+https://github.com/ChaoXu1997/yzu-wlan.git
```

## 使用

### 首次配置

```bash
yzu-wlan --setup
```

按提示输入用户名、密码，选择网络服务商。

### 单次检测

```bash
yzu-wlan
```

检测网络状态，未联网则自动登录，完成后退出。

### 持续运行（可选）

```bash
yzu-wlan --daemon
```

以守护进程模式持续运行，断网自动重连。

## 配置为系统服务（推荐）

使用 systemd timer 定时检测，不占用常驻内存：

```bash
mkdir -p ~/.config/systemd/user/
cp contrib/yzu-wlan.service ~/.config/systemd/user/
cp contrib/yzu-wlan.timer ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now yzu-wlan.timer
```

查看日志：

```bash
journalctl --user -u yzu-wlan.service -f
```

## 配置文件

位置：`~/.config/yzu-wlan/config.json`

```json
{
    "username": "学号",
    "password": "密码",
    "service": "电信互联网服务",
    "check_interval": 60,
    "start_delay": 5
}
```

可选服务商：`电信互联网服务`、`移动互联网服务`、`联通互联网服务`、`学校互联网服务`、`校内免费服务`

## 依赖

无。需要 Python >= 3.8。

## 致谢

登录逻辑参考了 [luoboQAQ/yzu-campusnet-login](https://github.com/luoboQAQ/yzu-campusnet-login)（Go 版本）。
