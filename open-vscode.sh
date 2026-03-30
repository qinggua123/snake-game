#!/bin/bash
# 🦞 龙虾哥的 VSCode 启动脚本
# 用于在 WSL 中打开 VSCode 并运行贪吃蛇游戏

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME="snake-game"
PROJECT_PATH="$SCRIPT_DIR"

echo "🐍 贪吃蛇项目 VSCode 启动器"
echo "=========================="
echo ""

# 检测 VSCode 安装方式
detect_vscode() {
    # 方式 1: WSL 中直接有 code 命令
    if command -v code &> /dev/null; then
        echo "✅ 检测到 VSCode (WSL code 命令)"
        VSCODE_CMD="code"
        return 0
    fi
    
    # 方式 2: Windows VSCode 的 WSL 集成
    if [ -f "/mnt/c/Users/issuser/AppData/Local/Programs/Microsoft VS Code/bin/code" ]; then
        echo "✅ 检测到 VSCode (Windows 路径)"
        VSCODE_CMD="/mnt/c/Users/issuser/AppData/Local/Programs/Microsoft VS Code/bin/code"
        return 0
    fi
    
    # 方式 3: 通过 Windows code.exe
    if [ -f "/mnt/c/Users/issuser/AppData/Local/Programs/Microsoft VS Code/Code.exe" ]; then
        echo "✅ 检测到 VSCode (Windows Code.exe)"
        VSCODE_CMD="/mnt/c/Users/issuser/AppData/Local/Programs/Microsoft VS Code/Code.exe"
        return 0
    fi
    
    echo "❌ 未找到 VSCode 安装"
    return 1
}

# 显示安装指南
show_install_guide() {
    echo ""
    echo "📖 安装指南"
    echo "=========="
    echo ""
    echo "方式 1: 在 Windows VSCode 中安装 WSL 支持（推荐）"
    echo "------------------------------------------------"
    echo "1. 打开 Windows 上的 VSCode"
    echo "2. 按 Ctrl+Shift+X 打开扩展面板"
    echo "3. 搜索 'WSL' 并安装（Microsoft 出品）"
    echo "4. 在 WSL 终端中运行："
    echo "   code /home/openclaw/.openclaw/workspace/snake-game"
    echo ""
    echo "方式 2: 在 VSCode 中安装 'code' 命令"
    echo "-----------------------------------"
    echo "1. 打开 Windows 上的 VSCode"
    echo "2. 按 Ctrl+Shift+P 打开命令面板"
    echo "3. 输入 'shell command'"
    echo "4. 选择 'Install code command in PATH'"
    echo "5. 重启终端后，在 WSL 中运行：code ."
    echo ""
    echo "方式 3: 手动添加别名"
    echo "-------------------"
    echo "在 ~/.bashrc 中添加："
    echo ""
    echo 'code() {'
    echo '    "/mnt/c/Users/issuser/AppData/Local/Programs/Microsoft VS Code/bin/code" "$@"'
    echo '}'
    echo ""
    echo "然后运行：source ~/.bashrc"
    echo ""
}

# 安装 VSCode 扩展
install_extensions() {
    echo ""
    echo "📦 检查 VSCode 扩展..."
    
    if command -v code &> /dev/null; then
        # 检查 Python 扩展
        if ! code --list-extensions 2>/dev/null | grep -q "ms-python.python"; then
            echo "📥 安装 Python 扩展..."
            code --install-extension ms-python.python 2>/dev/null || echo "⚠️ 扩展安装失败，请手动安装"
        fi
        
        # 检查 OpenClaw Chat 扩展
        if ! code --list-extensions 2>/dev/null | grep -q "openclaw-chat"; then
            echo "📥 安装 OpenClaw Chat 扩展..."
            code --install-extension wodeapp.openclaw-chat 2>/dev/null || echo "⚠️ 扩展安装失败，请手动安装"
        fi
        
        echo "✅ 扩展检查完成"
    fi
}

# 打开 VSCode
open_vscode() {
    echo ""
    echo "🚀 打开 VSCode..."
    echo "📂 项目路径：$PROJECT_PATH"
    echo ""
    
    if [ -n "$VSCODE_CMD" ]; then
        "$VSCODE_CMD" "$PROJECT_PATH" &
        echo "✅ VSCode 已启动！"
        echo ""
        echo "💡 提示："
        echo "   - 按 F5 开始调试"
        echo "   - 按 Ctrl+F5 无调试运行"
        echo "   - 按 Ctrl+` 打开终端"
        echo "   - 在终端运行：python snake.py"
    else
        echo "❌ 无法启动 VSCode"
        show_install_guide
        return 1
    fi
}

# 运行贪吃蛇
run_snake() {
    echo ""
    echo "🐍 运行贪吃蛇游戏..."
    echo ""
    
    cd "$PROJECT_PATH"
    
    # 检查 pygame 是否安装
    if ! python3 -c "import pygame" 2>/dev/null; then
        echo "⚠️ pygame 未安装，正在安装..."
        pip3 install pygame --user
    fi
    
    echo "🎮 启动游戏..."
    python3 snake.py
}

# 主菜单
main() {
    echo "请选择操作："
    echo ""
    echo "  1) 打开 VSCode"
    echo "  2) 直接运行贪吃蛇"
    echo "  3) 运行 Debug 版本（带日志）"
    echo "  4) 安装指南"
    echo "  5) 退出"
    echo ""
    
    read -p "请输入选项 (1-5): " choice
    
    case $choice in
        1)
            if detect_vscode; then
                open_vscode
            else
                show_install_guide
            fi
            ;;
        2)
            run_snake
            ;;
        3)
            cd "$PROJECT_PATH"
            python3 snake_debug.py --debug
            ;;
        4)
            show_install_guide
            ;;
        5)
            echo "👋 再见！"
            exit 0
            ;;
        *)
            echo "❌ 无效选项"
            exit 1
            ;;
    esac
}

# 检查参数
if [ "$1" == "--auto" ]; then
    # 自动模式：尝试打开 VSCode，失败则运行游戏
    if detect_vscode; then
        open_vscode
    else
        echo "⚠️ VSCode 不可用，直接运行游戏..."
        run_snake
    fi
elif [ "$1" == "--vscode" ]; then
    if detect_vscode; then
        open_vscode
    else
        show_install_guide
        exit 1
    fi
elif [ "$1" == "--run" ]; then
    run_snake
elif [ "$1" == "--debug" ]; then
    cd "$PROJECT_PATH"
    python3 snake_debug.py --debug
elif [ "$1" == "--help" ] || [ "$1" == "-h" ]; then
    echo "用法：$0 [选项]"
    echo ""
    echo "选项:"
    echo "  --auto    自动模式（优先 VSCode，失败则运行游戏）"
    echo "  --vscode  打开 VSCode"
    echo "  --run     直接运行游戏"
    echo "  --debug   运行 Debug 版本"
    echo "  --help    显示帮助"
    echo ""
    echo "无参数时显示交互式菜单"
else
    main
fi
