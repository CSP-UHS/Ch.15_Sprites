import random
import arcade

# --- Constants ---
BB8_scale = 0.3
trooper_scale = 0.1
trooper_count = 40
t_speed = 2
bullet_scale = 1
bullet_speed = 10
SW = 800
SH = 600
SP = 4


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/bb8.png", BB8_scale)
        self.laser_sound = arcade.load_sound("sounds/laser.mp3")

    def update(self):
        self.center_x += self.change_x
        if self.right < 0:
            self.left = SW
        elif self.left > SW:
            self.right = 0


class Trooper(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/stormtrooper.png", trooper_scale)
        self.w = int(self.width)
        self.h = int(self.height)

    def update(self):
        self.center_y -= t_speed
        if self.top < 0:
            self.center_x = random.randrange(self.w, SW - self.w)
            self.center_y = random.randrange(SH + self.h, SH * 2)


class Bullet(arcade.Sprite):
    def __init__(self):
        super().__init__("Images/bullet.png", bullet_scale)
        self.explosion = arcade.load_sound('sounds/explosion.mp3')

    def update(self):
        self.center_y += bullet_speed
        if self.bottom < 0:
            self.kill()


# ------MyGame Class--------------
class MyGame(arcade.Window):

    def __init__(self, SW, SH, title):
        super().__init__(SW, SH, title)
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.set_mouse_visible(False)

    def reset(self):
        self.player_list = arcade.SpriteList()
        self.trooper_list = arcade.SpriteList()
        self.bullets = arcade.SpriteList()

        # VARIABLES
        self.score = 0
        self.Gameover = False

        # Create our Player
        self.BB8 = Player()
        self.BB8.center_x = SW / 2
        self.BB8.bottom = 2
        self.player_list.append(self.BB8)

        # Create a lot of troopers
        for i in range(trooper_count):
            trooper = Trooper()
            trooper.center_x = random.randrange(trooper.w // 2, SW - trooper.w // 2)
            trooper.center_y = random.randrange(SH // 2, SH * 2)
            self.trooper_list.append(trooper)

    def on_draw(self):
        arcade.start_render()
        self.player_list.draw()
        self.trooper_list.draw()
        self.bullets.draw()

        # print the score
        the_score = f"Score: {self.score:}"
        arcade.draw_text(the_score, SW - 80, SH - 20, arcade.color.BLACK, 14)

        # Draw Game Over Screen
        if self.Gameover == True:
            arcade.draw_rectangle_filled(SW // 2, SH // 2, SW, SH, arcade.color.BLACK)
            arcade.draw_text("Game Over: Press P to Play Again!", SW / 2 - 50, SH / 2 - 20, (0, 255, 0), 14)

    def on_update(self, dt):
        self.player_list.update()
        self.trooper_list.update()
        self.bullets.update()

        if len(self.trooper_list) == 0:
            self.Gameover = True

        # Detect BB8 colliding with trooper
        BB8_hit = arcade.check_for_collision_with_list(self.BB8, self.trooper_list)
        if len(BB8_hit) > 0:
            self.BB8.kill()
            self.Gameover = True

        for bullet in self.bullets:
            bullet_hit_list = arcade.check_for_collision_with_list(bullet, self.trooper_list)
            if len(bullet_hit_list) > 0:
                arcade.play_sound(bullet.explosion)
                bullet.kill()




        for trooper in trooper_hit_list:
            trooper.kill()  # order 67
            arcade.play_sound(self.BB8.laser_sound)
            self.score += 1

        if len(self.trooper_list) == 0:
            self.reset()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.BB8.change_x = -SP
        elif key == arcade.key.RIGHT:
            self.BB8.change_x = SP
        elif key == arcade.key.UP:
            self.BB8.change_y = SP
        elif key == arcade.key.DOWN:
            self.BB8.change_y = -SP

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.BB8.change_x = 0
        elif key == arcade.key.UP or key == arcade.key.DOWN:
            self.BB8.change_y = 0


# -----Main Function--------
def main():
    window = MyGame(SW, SH, "BB8 Attack")
    window.reset()
    arcade.run()


# ------Run Main Function-----
if __name__ == "__main__":
    main()