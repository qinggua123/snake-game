# 🦞 龙虾哥的贪吃蛇 - VSCode 配置指南

## 🚀 快速启动

### 方式 1: 使用快捷命令（推荐）

```bash
# 加载新配置
source ~/.bashrc

# 直接运行游戏
snake

# 运行 Debug 版本
snake-debug

# 打开 VSCode
vscode-snake
```

### 方式 2: 使用启动脚本

```bash
cd /home/openclaw/.openclaw/workspace/snake-game

# 交互式菜单
./open-vscode.sh

# 自动模式（优先 VSCode）
./open-vscode.sh --auto

# 直接打开 VSCode
./open-vscode.sh --vscode

# 直接运行游戏
./open-vscode.sh --run

# Debug 模式
./open-vscode.sh --debug
```

---

## 📖 在 WSL 中打开 VSCode

### 前提条件

1. **Windows 上已安装 VSCode**
2. **WSL 已安装并配置**

### 方式 1: 安装 WSL 扩展（最佳体验 ⭐）

**在 Windows VSCode 中：**

1. 按 `Ctrl+Shift+X` 打开扩展面板
2. 搜索 **"WSL"** (Microsoft 出品)
3. 点击安装
4. 在 WSL 终端中运行：
   ```bash
   code /home/openclaw/.openclaw/workspace/snake-game
   ```

### 方式 2: 安装 'code' 命令

**在 Windows VSCode 中：**

1. 按 `Ctrl+Shift+P` 打开命令面板
2. 输入 `shell command`
3. 选择 **"Install code command in PATH"**
4. 重启终端
5. 在 WSL 中运行：
   ```bash
   code /home/openclaw/.openclaw/workspace/snake-game
   ```

### 方式 3: 手动配置别名

**在 WSL 终端中：**

```bash
# 编辑 ~/.bashrc
nano ~/.bashrc

# 添加以下内容
code() {
    "/mnt/c/Users/issuser/AppData/Local/Programs/Microsoft VS Code/bin/code" "$@"
}

# 保存后重新加载
source ~/.bashrc

# 测试
code --version
```

---

## 🐛 Debug 配置

### VSCode 中调试

1. **打开项目**
   ```bash
   code /home/openclaw/.openclaw/workspace/snake-game
   ```

2. **配置已自动生成**
   - `.vscode/launch.json` - 调试配置
   - `.vscode/settings.json` - 项目设置

3. **开始调试**
   - 按 `F5` - 启动调试
   - 按 `Ctrl+F5` - 无调试运行
   - 按 `F9` - 切换断点
   - 按 `F10` - 单步执行

4. **选择调试配置**
   - 🐍 Python: 贪吃蛇 - 运行当前文件
   - 🐍 Python: 贪吃蛇 (Debug 模式) - 带详细日志

### 命令行调试

```bash
# 运行 Debug 版本
python3 snake_debug.py --debug

# 查看实时日志
tail -f snake_debug.log

# 以不同 FPS 运行
python3 snake.py --fps 5    # 慢速
python3 snake.py --fps 20   # 快速
```

---

## 📦 依赖安装

### 已自动安装
- ✅ pygame 2.x

### 手动安装（如需要）

```bash
# 系统级安装
sudo apt install python3-pygame

# 或 pip 安装
pip3 install pygame --break-system-packages

# 或在虚拟环境中
python3 -m venv venv
source venv/bin/activate
pip install pygame
```

---

## 🎮 运行游戏

### Python 桌面版

```bash
# 方式 1: 使用快捷命令
snake

# 方式 2: 直接运行
cd /home/openclaw/.openclaw/workspace/snake-game
python3 snake.py

# 方式 3: 带参数运行
python3 snake.py --debug      # Debug 模式
python3 snake.py --fps 15     # 设置 FPS
python3 snake.py --theme blue # 选择主题
```

### HTML5 网页版

```bash
# 启动本地服务器
cd /home/openclaw/.openclaw/workspace/snake-game
python3 -m http.server 8000

# 浏览器访问
# http://localhost:8000
```

---

## 🔧 故障排除

### VSCode 无法打开

**问题：** `code: command not found`

**解决：**
```bash
# 检查 VSCode 是否安装
ls -la "/mnt/c/Users/issuser/AppData/Local/Programs/Microsoft VS Code/bin/code"

# 手动添加别名
echo 'code() { "/mnt/c/Users/issuser/AppData/Local/Programs/Microsoft VS Code/bin/code" "$@"; }' >> ~/.bashrc
source ~/.bashrc
```

### pygame 未安装

**问题：** `ModuleNotFoundError: No module named 'pygame'`

**解决：**
```bash
pip3 install pygame --break-system-packages
```

### 游戏无法启动

**问题：** 黑屏或闪退

**解决：**
```bash
# 检查显示服务器
echo $DISPLAY

# 尝试设置 DISPLAY
export DISPLAY=:0

# 运行 Debug 版本查看详细错误
python3 snake_debug.py --debug
cat snake_debug.log
```

---

## 📁 项目结构

```
snake-game/
├── .vscode/
│   ├── launch.json          # Debug 配置
│   ├── settings.json        # 项目设置
│   └── extensions.json      # 推荐插件
├── snake.py                 # 主程序 (v2.0)
├── snake_debug.py           # Debug 版本
├── index.html               # HTML5 网页版
├── requirements.txt         # Python 依赖
├── open-vscode.sh          # VSCode 启动脚本
├── SETUP.md                # 配置指南（本文件）
└── README.md               # 项目说明
```

---

## 💡 快捷键参考

### VSCode
| 快捷键 | 功能 |
|--------|------|
| `F5` | 启动调试 |
| `Ctrl+F5` | 无调试运行 |
| `F9` | 切换断点 |
| `F10` | 单步执行 |
| `Ctrl+`` ` | 打开终端 |
| `Ctrl+Shift+P` | 命令面板 |

### 游戏
| 按键 | 功能 |
|------|------|
| `↑↓←→` / `WASD` | 移动 |
| `T` | 切换主题 |
| `M` | 开关音效 |
| `P` | 暂停 |
| `D` | 打印状态（Debug 版） |
| `SPACE` | 重新开始 |
| `ESC` | 退出 |

---

## 🦞 快捷命令

已添加到 `~/.bashrc`：

```bash
snake          # 运行贪吃蛇
snake-debug    # 运行 Debug 版本
vscode-snake   # 打开 VSCode
```

**使用方式：**
```bash
source ~/.bashrc  # 首次加载
snake             # 随时运行游戏！
```

---

**祝你玩得开心！🎉**
