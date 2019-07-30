import pyglet
from pyglet.window import key, FPSDisplay
from pyglet.sprite import Sprite
from GameObject import GameObjectClass, preload_image

import inspect

print(pyglet.window.Window.on_key_press)

class GameWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_location(400, 100)
        self.frame_rate = 1/60.0
        self.fps_display = FPSDisplay(self)
        self.fps_display.label.font_size = 10

        self.right = False
        self.left = False
        self.player_speed = 300

        player_spr = Sprite(preload_image('pixelship.png'))
        self.player = GameObjectClass(500, 100, player_spr)


        self.space_list = []
        self.space_img = preload_image('bluespace-seamless.png')
        for i in range(2):
            self.space_list.append(GameObjectClass(0, i*1060, Sprite(self.space_img)))

        for space in self.space_list:
            space.vely = -200

    def on_key_press(self, symbol, modifiers):
        if symbol == key.RIGHT:
            self.right = True
        if symbol == key.LEFT:
            self.left = True
        if symbol == key.ESCAPE:
            pyglet.app.exit()

    def on_key_release(self, symbol, modifiers):
        if symbol == key.RIGHT:
            self.right = False
        if symbol == key.LEFT:
            self.left = False

    def on_draw(self):
        self.clear()
        for space in self.space_list:
            space.draw()
        self.player.sprite.draw()
        self.fps_display.draw()

    def update_player(self, dt):
        self.player.update(dt)
        if self.right and self.player.posx < 1000 - self.player.width:
            self.player.posx += self.player_speed * dt
        if self.left and self.player.posx > 100:
            self.player.posx -= self.player_speed * dt



    def update_space(self, dt):
        for space in self.space_list:
            space.update(dt)
            if space.posy <= -1050:
                self.space_list.append(GameObjectClass(0, abs(space.posy), Sprite(self.space_img)))
                self.space_list.remove(space)
            space.vely = -200

    def update(self, dt):
        self.update_player(dt)
        self.update_space(dt)

if __name__ == "__main__":
    window = GameWindow(1200, 900, "Space Invaders", resizable=False)
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()

