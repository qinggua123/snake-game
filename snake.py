#!/usr/bin/env python3
"""
🐍 经典贪吃蛇游戏
使用 pygame 实现
作者：小z
日期：2026-03-30
"""

import pygame
import random
import sys

# 初始化 pygame
pygame.init()

# 游戏配置
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
CELL_SIZE = 20
FPS = 10

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
RED = (255, 0, 0)
GRAY = (40, 40, 40)

# 方向定义
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    """蛇类"""
    
    def __init__(self):
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
    
    def move(self):
        """移动蛇"""
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x * CELL_SIZE, head_y + dir_y * CELL_SIZE)
        
        self.body.insert(0, new_head)
        
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
    
    def change_direction(self, new_direction):
        """改变方向（不能直接反向）"""
        opposite = (self.direction[0] * -1, self.direction[1] * -1)
        if new_direction != opposite:
            self.direction = new_direction
    
    def check_collision(self):
        """检查碰撞"""
        head = self.body[0]
        
        # 撞墙
        if (head[0] < 0 or head[0] >= WINDOW_WIDTH or
            head[1] < 0 or head[1] >= WINDOW_HEIGHT):
            return True
        
        # 撞自己
        if head in self.body[1:]:
            return True
        
        return False
    
    def draw(self, surface):
        """绘制蛇"""
        for i, segment in enumerate(self.body):
            color = GREEN if i == 0 else DARK_GREEN
            rect = pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, WHITE, rect, 1)


class Food:
    """食物类"""
    
    def __init__(self, snake_body):
        self.position = (0, 0)
        self.randomize(snake_body)
    
    def randomize(self, snake_body):
        """随机生成食物位置"""
        while True:
            x = random.randint(0, (WINDOW_WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
            y = random.randint(0, (WINDOW_HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
            if (x, y) not in snake_body:
                self.position = (x, y)
                break
    
    def draw(self, surface):
        """绘制食物"""
        rect = pygame.Rect(self.position[0], self.position[1], CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, RED, rect)
        pygame.draw.rect(surface, WHITE, rect, 1)


class Game:
    """游戏主类"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('🐍 贪吃蛇 - Snake Game')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset()
    
    def reset(self):
        """重置游戏"""
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.score = 0
        self.game_over = False
    
    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.reset()
                    elif event.key == pygame.K_ESCAPE:
                        return False
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
        
        return True
    
    def update(self):
        """更新游戏状态"""
        if self.game_over:
            return
        
        self.snake.move()
        
        # 检查吃食物
        if self.snake.body[0] == self.food.position:
            self.snake.grow = True
            self.score += 10
            self.food.randomize(self.snake.body)
        
        # 检查碰撞
        if self.snake.check_collision():
            self.game_over = True
    
    def draw(self):
        """绘制游戏画面"""
        self.screen.fill(BLACK)
        
        # 绘制网格
        for x in range(0, WINDOW_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (WINDOW_WIDTH, y))
        
        # 绘制蛇和食物
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        
        # 绘制分数
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # 游戏结束画面
        if self.game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.font.render('GAME OVER', True, RED)
            score_text = self.font.render(f'Final Score: {self.score}', True, WHITE)
            restart_text = self.font.render('Press SPACE to restart', True, WHITE)
            quit_text = self.font.render('Press ESC to quit', True, WHITE)
            
            self.screen.blit(game_over_text, 
                           (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, 
                            WINDOW_HEIGHT // 2 - 60))
            self.screen.blit(score_text,
                           (WINDOW_WIDTH // 2 - score_text.get_width() // 2,
                            WINDOW_HEIGHT // 2 - 20))
            self.screen.blit(restart_text,
                           (WINDOW_WIDTH // 2 - restart_text.get_width() // 2,
                            WINDOW_HEIGHT // 2 + 20))
            self.screen.blit(quit_text,
                           (WINDOW_WIDTH // 2 - quit_text.get_width() // 2,
                            WINDOW_HEIGHT // 2 + 60))
        
        pygame.display.flip()
    
    def run(self):
        """运行游戏主循环"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


def main():
    """主函数"""
    print("🐍 贪吃蛇游戏启动中...")
    print("控制方式：")
    print("  方向键 或 WASD - 移动")
    print("  ESC - 退出")
    print("  SPACE - 游戏结束后重新开始")
    print()
    
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
