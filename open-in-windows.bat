@echo off
REM 🦞 龙虾哥的贪吃蛇 - Windows 启动脚本
REM 用于在 Windows 上打开 VSCode 并运行贪吃蛇游戏

echo 🐍 贪吃蛇项目 - Windows 启动器
echo ==========================
echo.

REM 设置 WSL 项目路径
set WSL_PROJECT_PATH=\\wsl$\Ubuntu\home\openclaw\.openclaw\workspace\snake-game

REM 检查 VSCode 是否安装
where code >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ 检测到 VSCode
    echo.
    echo 🚀 正在打开 VSCode...
    code "%WSL_PROJECT_PATH%"
    echo ✅ VSCode 已启动！
    echo.
    echo 💡 提示：
    echo    - 按 F5 开始调试
    echo    - 按 Ctrl+` 打开终端
    echo    - 在终端运行：python3 snake.py
) else (
    echo ⚠️ 未找到 VSCode code 命令
    echo.
    echo 📖 安装指南：
    echo.
    echo 方式 1: 在 VSCode 中安装 code 命令
    echo --------------------------------
    echo 1. 打开 VSCode
    echo 2. 按 Ctrl+Shift+P 打开命令面板
    echo 3. 输入 "shell command"
    echo 4. 选择 "Install code command in PATH"
    echo 5. 重新运行此脚本
    echo.
    echo 方式 2: 手动打开项目
    echo -------------------
    echo 1. 打开 VSCode
    echo 2. 文件 → 打开文件夹
    echo 3. 输入：%WSL_PROJECT_PATH%
    echo.
    echo 方式 3: 使用资源管理器
    echo ---------------------
    echo 1. 按 Win+R
    echo 2. 输入：%WSL_PROJECT_PATH%
    echo 3. 右键文件夹 → "通过 Code 打开"
    echo.
)

echo.
pause
