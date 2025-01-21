from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, ObjectProperty, ListProperty
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.logger import Logger
from kivy.graphics import Line, Color, Rectangle
from lib.constants import MenuItems
from lib.event_queue import BmoEvent, add_event
from lib.games import SmartGrid
from lib.kivy_utils import JOY_ACITON_ARROW_UP, JOY_ACTION_ARROW_DOWN, JOY_ACTION_ARROW_LEFT, JOY_ACTION_ARROW_RIGHT, JOY_ACTION_SELECT_BUTTON_DOWN, JoystickHandler
from lib.widgets import BmoMenu
from kivy.vector import Vector


AI_LOOK_AHEAD = 5
CYCLE_WIDTH = 5

class LightCycleHead(Widget):
    color = ListProperty([1, 1, 1, 1])

    def __init__(self, direction: int,  **kwargs):
        super().__init__(**kwargs)
        self.alive = True
        self.speed = 3
        self.orientation = (CYCLE_WIDTH * direction, 0)

    def move(self):
        self.pos = Vector(*self.orientation) + self.pos

    def turn(self, direction):
        if direction == 'up':
            self.orientation = (0, CYCLE_WIDTH)
        elif direction == 'down':
            self.orientation = (0, -CYCLE_WIDTH)
        elif direction == 'left':
            self.orientation = (-CYCLE_WIDTH, 0)
        elif direction == 'right':
            self.orientation = (CYCLE_WIDTH, 0)


class LightCycleTail(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.alive = True

    def move(self, new_pos):
        self.pos = new_pos


class LightCyclesGame(Widget, JoystickHandler):
    player1 = ObjectProperty(None)
    computer = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._clock = None
        self._occupied = None
        self._curr_speed = 45.0

    def start_game(self, payer_vs_computer=True):
        # Initialize grid
        self._occupied = SmartGrid(self.width, self.height)
        # Initialize players
        self.player1 = LightCycleHead(direction=1, pos=(100, self.height/2), color=[0, 1, 1, 1], size=(CYCLE_WIDTH, CYCLE_WIDTH))
        if payer_vs_computer:
            self.computer = LightCycleHead(direction=-1, pos=(self.width-100, self.height/2), color=[1, 0, 0, 1], size=(CYCLE_WIDTH, CYCLE_WIDTH))
        else:
            self.computer = None

        if self.computer:
            self.add_widget(self.computer)

        # Add widgets
        self.add_widget(self.player1)

        # Setup callbacks
        self.bind_joystick(self.on_joystick)

        # Start game loop
        self._clk = Clock.schedule_interval(self.update, 1.0/self._curr_speed)

    def update(self, dt):
        # Move cycles
        prev_player1_pos = self.player1.pos
        self.player1.move()
        if self.computer:
            prev_other_player_pos = self.computer.pos
            self.computer.move()

        # Check for collisions
        if self._occupied[self.player1.pos]:
            self.player1.alive = False
            self._end_game()

        if self.computer:
            if self._occupied[self.computer.pos]:
                self.computer.alive = False
                self._end_game()
            self.computer.add_widget(LightCycleTail(pos=prev_other_player_pos, color=self.computer.color, size=(CYCLE_WIDTH, CYCLE_WIDTH)))
            self._occupied[self.computer.pos] = True
            self._update_computer_ai()

        # Add tail
        self.player1.add_widget(LightCycleTail(pos=prev_player1_pos, color=self.player1.color, size=(CYCLE_WIDTH, CYCLE_WIDTH)))

        # Update occupied grid
        self._occupied[self.player1.pos] = True

    def _update_computer_ai(self):
        # Simple AI: Look ahead and avoid collisions
        possible_moves = [
            (CYCLE_WIDTH, 0, 'right'), (-CYCLE_WIDTH, 0, 'left'), (0, CYCLE_WIDTH, 'up'), (0, -CYCLE_WIDTH, 'down')
        ]

        current_dir = self.computer.orientation
        current_score = 999
        best_move = current_dir
        scores = [
            [999, 'right'],
            [999, 'left'],
            [999, 'up'],
            [999, 'down'],
        ]

        for idx, move in enumerate(possible_moves):
            if move[0] == -current_dir[0] and move[1] == -current_dir[1]:
                scores[idx][0] = -1
                continue  # Don't allow 180-degree turns

            for look_ahead in range(1, AI_LOOK_AHEAD):
                test_x = self.computer.x + move[0] * look_ahead
                test_y = self.computer.y + move[1] * look_ahead
                if self._occupied[test_x, test_y]:
                    scores[idx] = (look_ahead, move[2])
                    if move[0] == current_dir[0] and move[1] == current_dir[1]:
                        current_score = idx
                    break

        best_score = current_score
        best_move = None
        for score in scores:
            if score[0] > best_score:
                best_move = score[1]
                best_score = score[0]
        if best_move:
            self.computer.turn(best_move)

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'up':
            self.player1.velocity_x = 0
            self.player1.velocity_y = 1
        elif keycode[1] == 'down':
            self.player1.velocity_x = 0
            self.player1.velocity_y = -1
        elif keycode[1] == 'left':
            self.player1.velocity_x = -1
            self.player1.velocity_y = 0
        elif keycode[1] == 'right':
            self.player1.velocity_x = 1
            self.player1.velocity_y = 0

    def on_joystick(self, stick_id, action):
        if stick_id == 0:
            player = self.player1
        elif stick_id == 1:
            player = self.player1

        if player:
            if action == JOY_ACITON_ARROW_UP:
                player.turn('up')
            elif action == JOY_ACTION_ARROW_DOWN:
                player.turn('down')
            elif action == JOY_ACTION_ARROW_LEFT:
                player.turn('left')
            elif action == JOY_ACTION_ARROW_RIGHT:
                player.turn('right')
            elif action == JOY_ACTION_SELECT_BUTTON_DOWN:
                self._pause_resume_game()

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None

    def draw_trails(self):
        self.canvas.clear()
        with self.canvas:
            # Draw player trail
            Color(*self.player1.color)
            for rect in self.player1.trail:
                Rectangle(pos=(rect[0], rect[1]), size=(rect[2]-rect[0], rect[3]-rect[1]))

            # Draw computer trail
            if self.computer:
                Color(*self.computer.color)
                for rect in self.computer.trail:
                    Rectangle(pos=(rect[0], rect[1]), size=(rect[2]-rect[0], rect[3]-rect[1]))

    def _end_game(self):
        if not self.player1.alive:
            winner = 'Computer'
        elif not self.computer.alive:
            winner = 'Player 1'
        self._halt_game()
        self.main_menu(winner=winner)

    def _halt_game(self):
        if self._clk:
            self._clk.cancel()
            self._clk = None
        if self.player1:
            self.remove_widget(self.player1)
        if self.computer:
            self.remove_widget(self.computer)
        self.unbind_joystick()

    def _pause_resume_game(self):
        if self._clk:
            self._clk.cancel()
            self._clk = None
            self._pause = True
            self.unbind_joystick()
            self.main_menu(True)
        else:
            self.bind_joystick(self.on_joystick)
            self._clk = Clock.schedule_interval(self.update, 1.0 / self._curr_speed)

    def main_menu(self, pause_resume: bool = False, winner: str = None):
        mnu_items = [MenuItems.PLAYER_VS_COMPUTER, MenuItems.PLAYER_VS_PLAYER, MenuItems.EXIT]
        if pause_resume:
            mnu_items.insert(0, MenuItems.RESUME)

        title = 'Lightcycles'
        if winner:
            title += f' - {winner} wins!'
        mnu =  BmoMenu(
            title=title,
            menu_items=mnu_items,
            callback=self.menu_callback)
        mnu.open()

    def menu_callback(self, cmd: str):
        Logger.info(f'Menu item: {cmd}')

        if cmd == MenuItems.EXIT:
            add_event(BmoEvent('leave_screen', {}))
        elif cmd == MenuItems.PLAYER_VS_COMPUTER:
            self.start_game(True)
        elif cmd == MenuItems.PLAYER_VS_PLAYER:
            self.start_game(False)
        elif cmd == MenuItems.RESUME:
            self._pause_resume_game()


class LightCyclesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._game = LightCyclesGame()
        self.add_widget(self._game)

    def play(self):
        self._game.main_menu()

    def on_enter(self):
        Logger.info('ENTER LightCycles screen')
        self._game.main_menu()


    def on_leave(self):
        Logger.info('LEAVE LightCycles screen')
