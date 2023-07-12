import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.core.window import Window
from kivy.utils import platform
from kivy.clock import Clock

from plyer import accelerometer
import random

# Fenstergröße
WIDTH = 720
HEIGHT = 1600

# Farben
WHITE = (1, 1, 1, 1)
BLACK = (0, 0, 0, 1)

# Spielergröße und Geschwindigkeit
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_SPEED = 5

# Plattformgröße und Geschwindigkeit
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20
PLATFORM_SPEED = 3

# Sprunggeschwindigkeit
JUMP_SPEED = 2


class Player(Widget):
    acceleration_x = NumericProperty(0)
    vel_y = NumericProperty(0)

    def start_accelerometer(self):
        if platform == 'android':
            accelerometer.enable()
            accelerometer.bind(on_acceleration=self.on_acceleration)

    def on_acceleration(self, _, acceleration):
        self.acceleration_x = acceleration[0]  # Nutze die X-Achse für die Steuerung

    def update(self, dt):
        keys = self._keyboard
        if keys and keys[273]:
            self.y += PLAYER_SPEED
        elif keys and keys[274]:
            self.y -= PLAYER_SPEED

        self.x += self.acceleration_x * 10

        self.vel_y += -9.8  # Schwerkraft
        self.y += self.vel_y

        # Überprüfe Kollision mit Plattformen
        for platform in platforms:
            if self.collide_widget(platform) and self.vel_y < 0:
                self.y = platform.y + platform.height
                self.vel_y = JUMP_SPEED  # Nach oben springen
                platform.remove_widget(platform)
                break

        # Sprunggeschwindigkeit anpassen
        if self.vel_y < 0:
            self.vel_y += 0.5  # Schrittweise Beschleunigung nach oben
            if self.vel_y >= 0:  # Maximale Sprunghöhe erreicht
                self.vel_y = 0  # Sprung abbremsen

        # Überprüfe, ob Spieler den Bildschirm verlässt
        if self.y < 0:
            self.y = 0
        elif self.y > HEIGHT - self.height:
            self.y = HEIGHT - self.height


class Platform(Widget):
    pass


class DoodleJumpGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player = Player()
        self.add_widget(self.player)

        for _ in range(10):
            platform = Platform()
            platform.x = random.randint(0, WIDTH - PLATFORM_WIDTH)
            platform.y = random.randint(0, HEIGHT - PLATFORM_HEIGHT)
            self.add_widget(platform)

        self.player.start_accelerometer()
        self._keyboard = Window.request_keyboard(None, self)
        self._keyboard.bind(on_key_down=self.on_key_down)
        self._keyboard.bind(on_key_up=self.on_key_up)

    def on_key_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'spacebar':
            self.player.vel_y = JUMP_SPEED
        return True

    def on_key_up(self, keyboard, keycode):
        if keycode[1] == 'spacebar':
            self.player.vel_y = 0
        return True

    def update(self, dt):
        self.player.update(dt)


class DoodleJumpApp(App):
    def build(self):
        game = DoodleJumpGame()
        Clock.schedule_interval(game.update, 1/60)  # Aktualisiere das Spiel 60 Mal pro Sekunde
        return game


if __name__ == '__main__':
    DoodleJumpApp().run()
