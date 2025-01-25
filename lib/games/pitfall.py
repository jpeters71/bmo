"""DOES NOT CURRENTLY WORK!!!"""

from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, ObjectProperty, ListProperty, BooleanProperty
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.logger import Logger
from kivy.vector import Vector
from lib.event_queue import BmoEvent, add_event
from lib.widgets import BmoMenu
import random

GRAVITY = 0.8
JUMP_SPEED = 15
PLAYER_SPEED = 5
SCROLL_SPEED = 3


class Player(Widget):
    velocity_y = NumericProperty(0)
    velocity_x = NumericProperty(0)
    is_jumping = BooleanProperty(False)

    def move(self):
        self.velocity_y -= GRAVITY
        self.pos = Vector(self.velocity_x, self.velocity_y) + self.pos

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = JUMP_SPEED
            self.is_jumping = True


class Obstacle(Widget):
    obstacle_type = NumericProperty(0)  # 0: pit, 1: log, 2: rope

    def move(self):
        self.x -= SCROLL_SPEED


class PitfallGame(Widget):
    player = ObjectProperty(None)
    score = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._clock = None
        self.obstacles = []
        self.game_over = False

    def start_game(self):
        self.player = Player(pos=(100, 100))
        self.score = 0
        self.game_over = False
        self.obstacles = []
        self.add_widget(self.player)
        self._generate_initial_obstacles()
        self._clock = Clock.schedule_interval(self.update, 1.0 / 60.0)

    def _generate_initial_obstacles(self):
        # Generate initial set of obstacles
        for i in range(5):
            obstacle = Obstacle(pos=(800 + i * 300, 60), obstacle_type=random.randint(0, 2))
            self.obstacles.append(obstacle)
            self.add_widget(obstacle)

    def update(self, dt):
        if self.game_over:
            return

        self.player.move()

        # Update obstacles
        for obstacle in self.obstacles[:]:
            obstacle.move()
            if obstacle.x < -100:
                self.remove_widget(obstacle)
                self.obstacles.remove(obstacle)
                self._add_new_obstacle()

            # Collision detection
            if self._check_collision(self.player, obstacle):
                self._end_game()
                return

        # Ground collision
        if self.player.y < 60:
            self.player.y = 60
            self.player.velocity_y = 0
            self.player.is_jumping = False

        # Update score
        self.score += 1

    def _add_new_obstacle(self):
        obstacle = Obstacle(pos=(self.width + 100, 60), obstacle_type=random.randint(0, 2))
        self.obstacles.append(obstacle)
        self.add_widget(obstacle)

    def _check_collision(self, player, obstacle):
        if obstacle.obstacle_type == 0:  # pit
            return player.collide_widget(obstacle) and player.y < obstacle.top
        else:
            return player.collide_widget(obstacle)

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'up':
            self.player.jump()
        elif keycode[1] == 'left':
            self.player.velocity_x = -PLAYER_SPEED
        elif keycode[1] == 'right':
            self.player.velocity_x = PLAYER_SPEED

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None

    def _end_game(self):
        self.game_over = True
        if self._clock:
            self._clock.cancel()

        mnu = BmoMenu(title=f'Game Over! Score: {self.score}', menu_items=['Play Again', 'Exit'], callback=self.menu_callback)
        mnu.open()

    def menu_callback(self, cmd: str):
        if cmd == 'Exit':
            add_event(BmoEvent('leave_screen', {}))
        elif cmd == 'Play Again':
            self.start_game()


class PitfallScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._game = PitfallGame()
        self.add_widget(self._game)

    def on_enter(self):
        Logger.info('ENTER Pitfall screen')
        self._game.start_game()

    def on_leave(self):
        Logger.info('LEAVE Pitfall screen')
        if self._game._clock:
            self._game._clock.cancel()
