# yzu-wlan

扬州大学校园网自动登录工具。

零外部依赖，仅使用 Python 标准库。

## 安装

### 方式一：下载二进制（推荐）

从 [GitHub Releases](https://github.com/ChaoXu1997/yzu-wlan/releases) 下载对应平台的预编译文件，无需安装 Python：

| 平台 | 文件 |
|------|------|
| Linux (x86_64) | `yzu-wlan-*-linux-amd64` |
| macOS (Apple Silicon) | `yzu-wlan-*-macos-arm64` |
| Windows (x86_64) | `yzu-wlan-*-windows-amd64.exe` |

Linux / macOS：

```bash
chmod +x yzu-wlan-*
sudo mv yzu-wlan-* /usr/local/bin/yzu-wlan
```

Windows：直接运行 `.exe` 文件。

### 方式二：从源码安装

需要 Python >= 3.8：

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

无外部依赖。从源码安装需要 Python >= 3.8，下载二进制无需任何运行时。

## 安全说明

- 调用的是 eportal 官方登录接口（`/eportal/InterFace.do?method=login`），与浏览器手动登录完全一致
- 使用用户自己的账号密码，不绕过任何认证机制
- 不涉及漏洞利用、暴力破解、端口扫描等行为
- 每 60 秒仅发送一次轻量级连通性检测（HTTP 204），已联网时不会触发登录请求
- 对校园网服务器和其他用户零影响

## 免责声明

本工具仅为个人便利开发的自动化脚本，所用的方法均为对正常登录流程的模拟，不得用于任何商业用途。

使用者需自行承担使用本工具的风险。因使用本工具导致的账号冻结、网络限制或其他任何损失，作者不承担任何责任。

请确保遵守扬州大学校园网相关管理规定。

## 致谢

登录逻辑参考了 [luoboQAQ/yzu-campusnet-login](https://github.com/luoboQAQ/yzu-campusnet-login)（Go 版本）。
