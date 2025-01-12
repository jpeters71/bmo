from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, ObjectProperty, ListProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.logger import Logger
from kivy.graphics import Line, Color
from lib.event_queue import BmoEvent, add_event
from lib.widgets import BmoMenu
import random

CYCLE_SPEED = 3
AI_LOOK_AHEAD = 50

class LightCycle(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.trail = []
        self.alive = True

    def move(self):
        if not self.alive:
            return

        new_x = self.x + self.velocity_x * CYCLE_SPEED
        new_y = self.y + self.velocity_y * CYCLE_SPEED

        # Add current position to trail
        self.trail.append((self.x, self.y))

        # Update position
        self.pos = (new_x, new_y)

class LightCyclesGame(Widget):
    player = ObjectProperty(None)
    computer = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._clock = None
        # self.register_event_type('on_game_over')

    def start_game(self):
        # Initialize players
        self.player = LightCycle(pos=(100, self.height/2), color=[0, 1, 1, 1])
        self.computer = LightCycle(pos=(self.width-100, self.height/2), color=[1, 0, 0, 1])

        # Set initial directions
        self.player.velocity_x = 1
        self.player.velocity_y = 0
        self.computer.velocity_x = -1
        self.computer.velocity_y = 0

        # Clear trails
        self.player.trail = []
        self.computer.trail = []

        # Add widgets
        self.add_widget(self.player)
        self.add_widget(self.computer)

        # Start game loop
        self._clock = Clock.schedule_interval(self.update, 1.0/60.0)

    def update(self, dt):
        # Move cycles
        self.player.move()
        self.computer.move()

        # Update computer AI
        self._update_computer_ai()

        # Check collisions
        if self._check_collision():
            self._end_game()

        # Draw trails
        self.draw_trails()

    def _check_collision(self):
        # Check wall collisions
        if (self.player.x < 0 or self.player.x > self.width or
            self.player.y < 0 or self.player.y > self.height):
            self.player.alive = False
            return True

        if (self.computer.x < 0 or self.computer.x > self.width or
            self.computer.y < 0 or self.computer.y > self.height):
            self.computer.alive = False
            return True

        # Check trail collisions
        p_pos = (self.player.x, self.player.y)
        c_pos = (self.computer.x, self.computer.y)

        if p_pos in self.player.trail[:-1] or p_pos in self.computer.trail:
            self.player.alive = False
            return True

        if c_pos in self.computer.trail[:-1] or c_pos in self.player.trail:
            self.computer.alive = False
            return True

        return False

    def _update_computer_ai(self):
        # Simple AI: Look ahead and avoid collisions
        possible_moves = [
            (1, 0), (-1, 0), (0, 1), (0, -1)
        ]

        current_dir = (self.computer.velocity_x, self.computer.velocity_y)
        best_move = current_dir

        for move in possible_moves:
            if move[0] == -current_dir[0] and move[1] == -current_dir[1]:
                continue  # Don't allow 180-degree turns

            test_x = self.computer.x + move[0] * AI_LOOK_AHEAD
            test_y = self.computer.y + move[1] * AI_LOOK_AHEAD

            if (test_x > 0 and test_x < self.width and
                test_y > 0 and test_y < self.height):
                best_move = move
                break

        self.computer.velocity_x = best_move[0]
        self.computer.velocity_y = best_move[1]

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'up':
            self.player.velocity_x = 0
            self.player.velocity_y = 1
        elif keycode[1] == 'down':
            self.player.velocity_x = 0
            self.player.velocity_y = -1
        elif keycode[1] == 'left':
            self.player.velocity_x = -1
            self.player.velocity_y = 0
        elif keycode[1] == 'right':
            self.player.velocity_x = 1
            self.player.velocity_y = 0

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None

    def draw_trails(self):
        self.canvas.clear()
        with self.canvas:
            # Draw player trail
            Color(*self.player.color)
            for i in range(len(self.player.trail)-1):
                Line(points=[self.player.trail[i][0], self.player.trail[i][1],
                           self.player.trail[i+1][0], self.player.trail[i+1][1]])

            # Draw computer trail
            Color(*self.computer.color)
            for i in range(len(self.computer.trail)-1):
                Line(points=[self.computer.trail[i][0], self.computer.trail[i][1],
                           self.computer.trail[i+1][0], self.computer.trail[i+1][1]])

    def _end_game(self):
        if self._clock:
            self._clock.cancel()

        winner = "Computer" if not self.player.alive else "Player"
        mnu = BmoMenu(
            title=f'Game Over - {winner} wins!',
            menu_items=['Play Again', 'Exit'],
            callback=self.menu_callback)
        mnu.open()

    def menu_callback(self, cmd: str):
        if cmd == 'Exit':
            add_event(BmoEvent('leave_screen', {}))
        elif cmd == 'Play Again':
            self.start_game()

class LightCyclesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._game = LightCyclesGame()
        self.add_widget(self._game)

    def on_enter(self):
        Logger.info('ENTER LightCycles screen')
        self._game.start_game()

    def on_leave(self):
        Logger.info('LEAVE LightCycles screen')
        self._game._clk.cancel()