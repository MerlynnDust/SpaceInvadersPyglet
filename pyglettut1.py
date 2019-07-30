import pyglet
from pyglet.window import key
from GameObject import GameObjectClass, preload_image

import inspect

print(pyglet.window.Window.on_key_press)

class GameWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_location(400, 100)
        self.frame_rate = 1/60.0

        player_spr = pyglet.sprite.Sprite(preload_image('pixelship.png'))
        self.player = GameObjectClass(500, 100, player_spr)


        self.space_list = []
        self.space_img = preload_image('bluespace-seamless.png')
        for i in range(2):
            self.space_list.append(GameObjectClass(0, i*1060, pyglet.sprite.Sprite(self.space_img)))

        for space in self.space_list:
            space.vely = -200

    def on_key_press(self, symbol, modifiers):
        if symbol == key.RIGHT:
            self.player.velx = 300
        if symbol == key.LEFT:
            self.player.velx = -300

    def on_key_release(self, symbol, modifiers):
        if symbol in (key.RIGHT, key.LEFT):
            self.player.velx = 0

    def on_draw(self):
        self.clear()
        for space in self.space_list:
            space.draw()
        self.player.sprite.draw()

    def update_space(self, dt):
        for space in self.space_list:
            space.update(dt)
            if space.posy <= -1060:
                self.space_list.remove(space)
                self.space_list.append(GameObjectClass(0, (space.posy * -1), pyglet.sprite.Sprite(self.space_img)))
                for spc in self.space_list:
                    spc.vely = -200

    def update(self, dt):
        self.player.update(dt)
        self.update_space(dt)

if __name__ == "__main__":
    window = GameWindow(1200, 900, "Space Invaders", resizable=False)
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()

