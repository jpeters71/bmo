from dataclasses import dataclass
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout
from lib.event_queue import BmoEvent, add_event
from lib.kivy_utils import JoystickHandler
import requests
from kivy.clock import Clock


# These values are for Seattle
NWS_STATION = 'SEW'
NWS_GRID_X_Y = '126,70'


@dataclass
class Forecast:
    day: str
    temperature: float
    temperature_unit: str
    icon: str
    short_forecast: str


class WeatherScreen(Screen, JoystickHandler):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._layout = MDBoxLayout(
            orientation='vertical',
            spacing=10,
            padding=20,
            md_bg_color=[0.4745, 0.7843, 0.6, 1],
        )
        self.add_widget(self._layout)

        # Header
        self._header = Label(
            text='Seattle Weather Forecast',
            font_size=40,
            size_hint_y=0.2,
            color=[0, 0, 0, 1],
        )
        self._layout.add_widget(self._header)

        # Weather content layout
        self._weather_content = MDBoxLayout(orientation='vertical')
        self._layout.add_widget(self._weather_content)

        self.bind_joystick(self.on_joystick)

    def on_enter(self):
        self.update_weather()

    def on_leave(self):
        self.unbind_joystick()

    def on_joystick(self, stick_id, action):
        add_event(BmoEvent('leave_screen', {}))
        self.unbind_joystick()
        return True

    def update_weather(self):
        # Clear previous weather data
        self._weather_content.clear_widgets()
        weather_data = self._get_weather() or []

        for day in weather_data:
            day_layout = BoxLayout(orientation='horizontal', size_hint_y=0.2)

            # Day label
            day_label = Label(
                text=day.day,
                font_size=30,
                size_hint_x=0.40,
                color=[0, 0, 0, 1],
            )
            day_layout.add_widget(day_label)

            # Weather icon
            icon = Image(source=day.icon, size_hint_x=0.15, size_hint_y=1.2)
            day_layout.add_widget(icon)

            # Temperature
            temp_label = Label(
                text=f'{day.temperature}°{day.temperature_unit}',
                font_size=30,
                size_hint_x=0.15,
                color=[0, 0, 0, 1],
            )
            day_layout.add_widget(temp_label)

            temp_desc = Label(
                text=f'{day.short_forecast}',
                font_size=20,
                size_hint_x=0.5,
                color=[0, 0, 0, 1],
            )
            day_layout.add_widget(temp_desc)

            self._weather_content.add_widget(day_layout)

        self._clock = Clock.schedule_once(self.exit, 10.0)

    def exit(self, dt):
        add_event(BmoEvent('leave_screen', {}))
        self._clock.cancel()
        self._clock = None

    def _get_weather(self) -> list[Forecast]:
        # Make request to NWS
        url = f'https://api.weather.gov/gridpoints/{NWS_STATION}/{NWS_GRID_X_Y}/forecast'

        resp = requests.get(url)

        if resp.ok:
            data = resp.json()
            periods = (data.get('properties') or {}).get('periods') or []

            forecasts = []
            for idx, period in enumerate(periods):
                is_daytime = period.get('isDaytime')
                if idx > 0 and not is_daytime:
                    continue

                # Figure out what icon to use
                short_forecast_lwr = period.get('shortForecast', '').lower()
                if 'snow' in short_forecast_lwr:
                    icon = 'snow'
                if 'rain' in short_forecast_lwr:
                    icon = 'rain'
                elif 'cloudy' in short_forecast_lwr:
                    icon = 'cloudy'
                elif 'partly' in short_forecast_lwr:
                    icon = 'partly-cloudy'
                else:
                    icon = 'sunny'

                icon_path = f'./media/weather/{icon}.png'
                forecast = Forecast(
                    day=period.get('name'),
                    temperature=period.get('temperature'),
                    temperature_unit=period.get('temperatureUnit'),
                    icon=icon_path,
                    short_forecast=period.get('shortForecast'),
                )
                forecasts.append(forecast)

            return forecasts
