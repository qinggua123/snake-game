#!/usr/bin/env python3
"""
🐍 经典贪吃蛇游戏 - 完整版
功能：皮肤系统、最高分记录、音效支持
作者：小 z
日期：2026-03-30
版本：2.0.0
"""

import pygame
import random
import sys
import json
import os

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

# 音效文件路径
SOUND_DIR = os.path.join(os.path.dirname(__file__), 'sounds')

class SoundManager:
    """🔊 音效管理器"""
    
    def __init__(self):
        self.enabled = True
        self.sounds = {}
        self.load_sounds()
    
    def load_sounds(self):
        """加载音效文件"""
        sound_files = {
            'eat': 'eat.wav',
            'gameover': 'gameover.wav',
            'move': 'move.wav'
        }
        
        for name, filename in sound_files.items():
            path = os.path.join(SOUND_DIR, filename)
            if os.path.exists(path):
                try:
                    self.sounds[name] = pygame.mixer.Sound(path)
                    print(f"✅ 加载音效：{filename}")
                except Exception as e:
                    print(f"⚠️ 音效加载失败 {filename}: {e}")
            else:
                print(f"ℹ️ 音效文件不存在：{filename} (将使用合成音效)")
        
        # 如果没有音效文件，使用合成音效
        if not self.sounds:
            self.create_synthetic_sounds()
    
    def create_synthetic_sounds(self):
        """创建合成音效（无需外部文件）"""
        print("🎵 使用合成音效模式")
        self.synth_mode = True
        self.sounds['eat'] = self._create_beep(440, 0.1)  # 吃食物：高音
        self.sounds['gameover'] = self._create_beep(150, 0.3)  # 游戏结束：低音
        self.sounds['move'] = None  # 移动音效太频繁，跳过
    
    def _create_beep(self, freq, duration):
        """创建简单的蜂鸣音效"""
        sample_rate = 44100
        n_samples = int(sample_rate * duration)
        buf = bytes([int(128 + 64 * ((i * freq / sample_rate) % 1 * 2 - 1)) 
                     for i in range(n_samples)])
        sound = pygame.mixer.Sound(buffer=buf)
        sound.set_volume(0.3)
        return sound
    
    def play(self, name):
        """播放音效"""
        if not self.enabled:
            return
        
        if name in self.sounds and self.sounds[name]:
            try:
                self.sounds[name].play()
            except:
                pass  # 忽略播放错误
    
    def toggle(self):
        """开关音效"""
        self.enabled = not self.enabled
        return self.enabled


class HighScoreManager:
    """🏆 最高分记录管理器"""
    
    def __init__(self, filename='highscores.json'):
        self.filename = os.path.join(os.path.dirname(__file__), filename)
        self.scores = self.load_scores()
    
    def load_scores(self):
        """加载最高分记录"""
        default_scores = {
            'classic': 0,
            'blue': 0,
            'purple': 0,
            'golden': 0,
            'matrix': 0,
            'dark': 0
        }
        
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    scores = json.load(f)
                    # 合并默认值（防止新版本增加主题）
                    for theme in default_scores:
                        if theme not in scores:
                            scores[theme] = 0
                    return scores
            except Exception as e:
                print(f"⚠️ 读取最高分失败：{e}")
        
        return default_scores
    
    def save_scores(self):
        """保存最高分记录"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.scores, f, indent=2, ensure_ascii=False)
            print(f"💾 最高分已保存")
        except Exception as e:
            print(f"❌ 保存最高分失败：{e}")
    
    def update(self, theme, score):
        """更新最高分"""
        if score > self.scores.get(theme, 0):
            self.scores[theme] = score
            self.save_scores()
            return True  # 新纪录！
        return False
    
    def get(self, theme):
        """获取某主题的最高分"""
        return self.scores.get(theme, 0)
    
    def get_all(self):
        """获取所有最高分"""
        return self.scores.copy()


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
    
    def draw(self, surface, theme_colors):
        """绘制蛇"""
        for i, segment in enumerate(self.body):
            color = theme_colors['snake_head'] if i == 0 else theme_colors['snake_body']
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
    
    def draw(self, surface, color):
        """绘制食物"""
        rect = pygame.Rect(self.position[0], self.position[1], CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, WHITE, rect, 1)


class Game:
    """游戏主类"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('🐍 贪吃蛇 - Snake Game v2.0')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # 初始化系统
        self.sound_manager = SoundManager()
        self.highscore_manager = HighScoreManager()
        
        # 当前主题
        self.current_theme = 'classic'
        self.theme_index = 0
        self.theme_list = list(THEMES.keys())
        
        self.reset()
    
    def reset(self):
        """重置游戏"""
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.score = 0
        self.game_over = False
        self.paused = False
    
    def get_theme_colors(self):
        """获取当前主题颜色"""
        return THEMES[self.current_theme]
    
    def next_theme(self):
        """切换到下一个主题"""
        self.theme_index = (self.theme_index + 1) % len(self.theme_list)
        self.current_theme = self.theme_list[self.theme_index]
        print(f"🎨 切换到主题：{THEMES[self.current_theme]['name']}")
    
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
                    elif event.key == pygame.K_t:
                        self.next_theme()
                    elif event.key == pygame.K_m:
                        state = self.sound_manager.toggle()
                        print(f"🔊 音效：{'开启' if state else '关闭'}")
        
        return True
    
    def update(self):
        """更新游戏状态"""
        if self.game_over or self.paused:
            return
        
        self.snake.move()
        
        # 检查吃食物
        if self.snake.body[0] == self.food.position:
            self.snake.grow = True
            self.score += 10
            self.sound_manager.play('eat')
            self.food.randomize(self.snake.body)
        
        # 检查碰撞
        if self.snake.check_collision():
            self.game_over = True
            self.sound_manager.play('gameover')
            
            # 更新最高分
            theme = self.current_theme
            if self.highscore_manager.update(theme, self.score):
                print(f"🏆 新纪录！{THEMES[theme]['name']}: {self.score}")
    
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
        
        # 绘制分数和最高分
        highscore = self.highscore_manager.get(self.current_theme)
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        highscore_text = self.small_font.render(f'Best: {highscore}', True, (200, 200, 200))
        theme_text = self.small_font.render(f'{THEMES[self.current_theme]["name"]}', True, (150, 150, 150))
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(highscore_text, (10, 45))
        self.screen.blit(theme_text, (WINDOW_WIDTH - 150, 10))
        
        # 暂停提示
        if self.paused:
            pause_text = self.font.render('PAUSED', True, WHITE)
            self.screen.blit(pause_text, 
                           (WINDOW_WIDTH // 2 - pause_text.get_width() // 2, 
                            WINDOW_HEIGHT // 2))
        
        # 游戏结束画面
        if self.game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.font.render('GAME OVER', True, theme_colors['food'])
            score_text = self.font.render(f'Final Score: {self.score}', True, WHITE)
            
            is_new_record = self.score >= highscore and self.score > 0
            if is_new_record:
                record_text = self.font.render('🏆 NEW RECORD! 🏆', True, (255, 215, 0))
                self.screen.blit(record_text,
                               (WINDOW_WIDTH // 2 - record_text.get_width() // 2,
                                WINDOW_HEIGHT // 2 - 100))
            
            self.screen.blit(game_over_text, 
                           (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, 
                            WINDOW_HEIGHT // 2 - 60))
            self.screen.blit(score_text,
                           (WINDOW_WIDTH // 2 - score_text.get_width() // 2,
                            WINDOW_HEIGHT // 2 - 20))
            
            restart_text = self.small_font.render('SPACE - Restart | T - Change Theme | ESC - Quit', True, WHITE)
            self.screen.blit(restart_text,
                           (WINDOW_WIDTH // 2 - restart_text.get_width() // 2,
                            WINDOW_HEIGHT // 2 + 30))
        
        # 控制提示
        if not self.game_over and not self.paused:
            hint_text = self.small_font.render('T-Theme M-Sound P-Pause', True, (100, 100, 100))
            self.screen.blit(hint_text, (WINDOW_WIDTH - 200, WINDOW_HEIGHT - 25))
        
        pygame.display.flip()
    
    def run(self):
        """运行游戏主循环"""
        print("🐍 贪吃蛇游戏 v2.0 启动中...")
        print("🎨 功能：皮肤系统 | 最高分记录 | 音效支持")
        print("\n控制方式：")
        print("  方向键 或 WASD - 移动")
        print("  T - 切换主题")
        print("  M - 开关音效")
        print("  P - 暂停")
        print("  ESC - 退出")
        print("  SPACE - 游戏结束后重新开始")
        print()
        
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


# 方向定义
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def main():
    """主函数"""
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
