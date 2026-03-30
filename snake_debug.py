#!/usr/bin/env python3
"""
🐍 贪吃蛇游戏 - Debug 版本
用于调试和测试
"""

import pygame
import random
import sys
import json
import os
import traceback

# 初始化 pygame
pygame.init()
pygame.mixer.init()

# 游戏配置
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
CELL_SIZE = 20
FPS = 10

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (40, 40, 40)
RED = (255, 0, 0)

# 🎨 皮肤/主题配置
THEMES = {
    'classic': {
        'name': '经典绿',
        'snake_head': (0, 255, 0),
        'snake_body': (0, 200, 0),
        'food': (255, 0, 0),
        'bg': BLACK
    },
    'blue': {
        'name': '蓝色风暴',
        'snake_head': (0, 150, 255),
        'snake_body': (0, 100, 200),
        'food': (255, 100, 0),
        'bg': (10, 10, 30)
    },
    'purple': {
        'name': '紫色幻影',
        'snake_head': (180, 50, 255),
        'snake_body': (120, 30, 200),
        'food': (255, 50, 150),
        'bg': (20, 5, 30)
    },
    'golden': {
        'name': '黄金传说',
        'snake_head': (255, 220, 0),
        'snake_body': (200, 170, 0),
        'food': (255, 50, 50),
        'bg': (30, 20, 5)
    },
    'matrix': {
        'name': '黑客帝国',
        'snake_head': (0, 255, 100),
        'snake_body': (0, 180, 50),
        'food': (255, 255, 255),
        'bg': (0, 10, 0)
    },
    'dark': {
        'name': '暗黑模式',
        'snake_head': (150, 150, 150),
        'snake_body': (100, 100, 100),
        'food': (255, 80, 80),
        'bg': (15, 15, 15)
    }
}

# 方向定义
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class DebugLogger:
    """调试日志器"""
    
    def __init__(self, filename='snake_debug.log'):
        self.filename = filename
        self.log_file = open(filename, 'w', encoding='utf-8')
        self.log("=== 贪吃蛇 Debug 会话开始 ===")
    
    def log(self, message):
        """记录日志"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        log_line = f"[{timestamp}] {message}"
        print(log_line)
        self.log_file.write(log_line + "\n")
        self.log_file.flush()
    
    def log_state(self, snake, food, score, theme):
        """记录游戏状态"""
        self.log(f"🐍 蛇头位置：{snake.body[0]}, 长度：{len(snake.body)}, 分数：{score}, 主题：{theme}")
    
    def log_event(self, event_type, details=""):
        """记录事件"""
        self.log(f"📌 事件：{event_type} - {details}")
    
    def log_error(self, error):
        """记录错误"""
        self.log(f"❌ 错误：{error}")
        traceback.print_exc(file=self.log_file)
    
    def close(self):
        """关闭日志文件"""
        self.log("=== Debug 会话结束 ===")
        self.log_file.close()


class Snake:
    """蛇类"""
    
    def __init__(self, logger=None):
        self.logger = logger
        self.reset()
    
    def reset(self):
        """重置蛇的状态"""
        start_x = WINDOW_WIDTH // 2
        start_y = WINDOW_HEIGHT // 2
        self.body = [
            (start_x, start_y),
            (start_x - CELL_SIZE, start_y),
            (start_x - 2 * CELL_SIZE, start_y)
        ]
        self.direction = RIGHT
        self.grow = False
        if self.logger:
            self.logger.log("🐍 蛇已重置")
    
    def move(self):
        """移动蛇"""
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x * CELL_SIZE, head_y + dir_y * CELL_SIZE)
        
        if self.logger:
            self.logger.log(f"➡️ 移动：方向 {self.direction}, 新头部 {new_head}")
        
        self.body.insert(0, new_head)
        
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
    
    def change_direction(self, new_direction):
        """改变方向（不能直接反向）"""
        opposite = (self.direction[0] * -1, self.direction[1] * -1)
        if new_direction != opposite:
            old_dir = self.direction
            self.direction = new_direction
            if self.logger:
                self.logger.log(f"🔄 方向改变：{old_dir} → {new_direction}")
        elif self.logger:
            self.logger.log(f"⚠️ 无效方向：试图反向 {new_direction}")
    
    def check_collision(self):
        """检查碰撞"""
        head = self.body[0]
        
        # 撞墙
        if (head[0] < 0 or head[0] >= WINDOW_WIDTH or
            head[1] < 0 or head[1] >= WINDOW_HEIGHT):
            if self.logger:
                self.logger.log(f"💥 撞墙：{head}")
            return True
        
        # 撞自己
        if head in self.body[1:]:
            if self.logger:
                self.logger.log(f"💥 撞自己：{head}")
            return True
        
        return False
    
    def draw(self, surface, theme_colors):
        """绘制蛇"""
        for i, segment in enumerate(self.body):
            color = theme_colors['snake_head'] if i == 0 else theme_colors['snake_body']
            rect = pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, WHITE, rect, 1)


class Food:
    """食物类"""
    
    def __init__(self, snake_body, logger=None):
        self.logger = logger
        self.position = (0, 0)
        self.randomize(snake_body)
    
    def randomize(self, snake_body):
        """随机生成食物位置"""
        attempts = 0
        while True:
            x = random.randint(0, (WINDOW_WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
            y = random.randint(0, (WINDOW_HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
            if (x, y) not in snake_body:
                self.position = (x, y)
                if self.logger:
                    self.logger.log(f"🍎 食物位置：{self.position}")
                break
            
            attempts += 1
            if attempts > 1000:
                if self.logger:
                    self.logger.log("⚠️ 警告：无法找到食物位置")
                break
    
    def draw(self, surface, color):
        """绘制食物"""
        rect = pygame.Rect(self.position[0], self.position[1], CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, WHITE, rect, 1)


class Game:
    """游戏主类 - Debug 版本"""
    
    def __init__(self, debug_mode=True):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('🐍 贪吃蛇 - Debug Mode')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Debug 模式
        self.debug_mode = debug_mode
        self.logger = DebugLogger() if debug_mode else None
        
        # 当前主题
        self.current_theme = 'classic'
        self.theme_index = 0
        self.theme_list = list(THEMES.keys())
        
        self.reset()
    
    def reset(self):
        """重置游戏"""
        self.snake = Snake(self.logger)
        self.food = Food(self.snake.body, self.logger)
        self.score = 0
        self.game_over = False
        self.paused = False
        self.frame_count = 0
        
        if self.logger:
            self.logger.log("🎮 游戏重置")
    
    def get_theme_colors(self):
        """获取当前主题颜色"""
        return THEMES[self.current_theme]
    
    def next_theme(self):
        """切换到下一个主题"""
        self.theme_index = (self.theme_index + 1) % len(self.theme_list)
        self.current_theme = self.theme_list[self.theme_index]
        if self.logger:
            self.logger.log(f"🎨 切换到主题：{THEMES[self.current_theme]['name']}")
    
    def handle_events(self):
        """处理事件 - Debug 增强版"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.logger:
                    self.logger.log("🚪 退出事件")
                return False
            
            if event.type == pygame.KEYDOWN:
                if self.logger:
                    self.logger.log_event("KEYDOWN", f"key={pygame.key.name(event.key)}")
                
                if self.game_over:
                    if event.key == pygame.K_SPACE:
                        if self.logger:
                            self.logger.log("🔄 重新开始")
                        self.reset()
                    elif event.key == pygame.K_ESCAPE:
                        return False
                    elif event.key == pygame.K_t:
                        self.next_theme()
                else:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.snake.change_direction(UP)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.snake.change_direction(DOWN)
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        self.snake.change_direction(LEFT)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        self.snake.change_direction(RIGHT)
                    elif event.key == pygame.K_ESCAPE:
                        return False
                    elif event.key == pygame.K_p:
                        self.paused = not self.paused
                        if self.logger:
                            self.logger.log(f"⏸️ 暂停：{self.paused}")
                    elif event.key == pygame.K_t:
                        self.next_theme()
                    elif event.key == pygame.K_d:
                        # D 键：打印详细状态
                        if self.logger:
                            self.logger.log_state(self.snake, self.food, self.score, self.current_theme)
                            self.logger.log(f"📊 帧数：{self.frame_count}")
        
        return True
    
    def update(self):
        """更新游戏状态"""
        if self.game_over or self.paused:
            return
        
        self.frame_count += 1
        self.snake.move()
        
        # 检查吃食物
        if self.snake.body[0] == self.food.position:
            self.snake.grow = True
            self.score += 10
            self.food.randomize(self.snake.body)
            if self.logger:
                self.logger.log(f"✅ 吃到食物！分数：{self.score}")
        
        # 检查碰撞
        if self.snake.check_collision():
            self.game_over = True
            if self.logger:
                self.logger.log(f"💥 游戏结束！最终分数：{self.score}")
                self.logger.log_state(self.snake, self.food, self.score, self.current_theme)
    
    def draw(self):
        """绘制游戏画面"""
        theme_colors = self.get_theme_colors()
        self.screen.fill(theme_colors['bg'])
        
        # 绘制网格
        for x in range(0, WINDOW_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (WINDOW_WIDTH, y))
        
        # 绘制蛇和食物
        self.snake.draw(self.screen, theme_colors)
        self.food.draw(self.screen, theme_colors['food'])
        
        # 绘制分数
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        theme_text = self.small_font.render(f'{THEMES[self.current_theme]["name"]}', True, (150, 150, 150))
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(theme_text, (WINDOW_WIDTH - 150, 10))
        
        # Debug 信息
        if self.debug_mode:
            debug_text = self.small_font.render(f'FPS: {int(self.clock.get_fps())} | Frame: {self.frame_count}', True, (0, 255, 0))
            self.screen.blit(debug_text, (10, WINDOW_HEIGHT - 25))
        
        # 游戏结束画面
        if self.game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.font.render('GAME OVER', True, RED)
            score_text = self.font.render(f'Final Score: {self.score}', True, WHITE)
            
            self.screen.blit(game_over_text, 
                           (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, 
                            WINDOW_HEIGHT // 2 - 60))
            self.screen.blit(score_text,
                           (WINDOW_WIDTH // 2 - score_text.get_width() // 2,
                            WINDOW_HEIGHT // 2 - 20))
            
            restart_text = self.small_font.render('SPACE - Restart | ESC - Quit', True, WHITE)
            self.screen.blit(restart_text,
                           (WINDOW_WIDTH // 2 - restart_text.get_width() // 2,
                            WINDOW_HEIGHT // 2 + 30))
        
        pygame.display.flip()
    
    def run(self):
        """运行游戏主循环"""
        print("🐍 贪吃蛇 Debug 版本启动中...")
        print("🔍 Debug 模式：已启用")
        print("📝 日志文件：snake_debug.log")
        print("\n控制方式：")
        print("  方向键 或 WASD - 移动")
        print("  T - 切换主题")
        print("  P - 暂停")
        print("  D - 打印详细状态（Debug）")
        print("  ESC - 退出")
        print("  SPACE - 游戏结束后重新开始")
        print()
        
        try:
            running = True
            while running:
                running = self.handle_events()
                self.update()
                self.draw()
                self.clock.tick(FPS)
        except Exception as e:
            if self.logger:
                self.logger.log_error(e)
            else:
                traceback.print_exc()
        finally:
            if self.logger:
                self.logger.close()
            pygame.quit()
            sys.exit()


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='🐍 贪吃蛇游戏')
    parser.add_argument('--debug', action='store_true', help='启用 Debug 模式')
    parser.add_argument('--theme', type=str, default='classic', choices=list(THEMES.keys()), help='选择主题')
    parser.add_argument('--fps', type=int, default=10, help='设置 FPS')
    args = parser.parse_args()
    
    global FPS
    FPS = args.fps
    
    game = Game(debug_mode=args.debug)
    
    if args.theme != 'classic':
        game.current_theme = args.theme
        game.theme_index = list(THEMES.keys()).index(args.theme)
    
    game.run()


if __name__ == '__main__':
    main()
