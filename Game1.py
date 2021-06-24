
import arcade
import time

from arcade.sound import load_sound
from pyglet import window

#path = r'F:\python programs\Game'
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SPRITE_SCALING_COIN = 0.08
SPRITE_SCALING_PLAYER = 0.2
SPRITE_SCALING_WALL=0.8
PLAYER_JUMP_SPEED = 25
PLAYER_MOVEMENT_SPEED = 8
GRAVITY = 1.5

LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 250
BOTTOM_VIEWPORT_MARGIN = 100
TOP_VIEWPORT_MARGIN = 100


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height):
        super().__init__(width, height)
        self.player_sprite = None
        self.ground_list = None
        self.physics_engine = None
        self.setup()

    def setup(self):
        arcade.set_background_color(arcade.color.AERO_BLUE)
        self.view_bottom = 0
        self.view_left = 0
        self.coin_sound = arcade.load_sound("sounds\coin_pickup.wav")
        self.game_over = arcade.load_sound("sounds\Game_over.wav")
        self.finish = arcade.load_sound("sounds\Finish.wav")
        my_map=arcade.tilemap.read_tmx("second-map.tmx")

        self.wall_list = arcade.tilemap.process_layer(map_object=my_map,layer_name="Ground",scaling=0.5,
                                                     use_spatial_hash=True)

        self.coin_list = arcade.tilemap.process_layer(map_object=my_map,layer_name="coins",scaling=0.5,
                                                     use_spatial_hash=True)

        self.water_list = arcade.tilemap.process_layer(map_object=my_map,layer_name="Water",scaling=0.5,
                                                     use_spatial_hash=True)

        self.plant_list = arcade.tilemap.process_layer(map_object=my_map,layer_name="plants",scaling=0.5,
                                                     use_spatial_hash=True)  

        self.goal_list = arcade.tilemap.process_layer(map_object=my_map,layer_name="Goal",scaling=0.5,
                                                     use_spatial_hash=True)                                           
        self.player_list = arcade.SpriteList()

        self.player = arcade.AnimatedWalkingSprite()

        self.player.stand_right_textures=[]

        self.player.stand_left_textures=[]

        self.player.stand_right_textures.append(arcade.load_texture("sprites\character\Idle__000.png"))

        self.player.stand_left_textures.append(arcade.load_texture("sprites\character\Idle__000.png",mirrored=True))

        self.player.walk_right_textures=[]

        self.player.walk_left_textures=[]

        self.player.walk_right_textures.append(arcade.load_texture("sprites\character\Run__000.png"))
        self.player.walk_right_textures.append(arcade.load_texture("sprites\character\Run__001.png"))
        self.player.walk_right_textures.append(arcade.load_texture("sprites\character\Run__002.png"))
        self.player.walk_right_textures.append(arcade.load_texture("sprites\character\Run__003.png"))
        self.player.walk_right_textures.append(arcade.load_texture("sprites\character\Run__004.png"))
        self.player.walk_right_textures.append(arcade.load_texture("sprites\character\Run__005.png"))
        self.player.walk_right_textures.append(arcade.load_texture("sprites\character\Run__006.png"))
        self.player.walk_right_textures.append(arcade.load_texture("sprites\character\Run__007.png"))
        self.player.walk_right_textures.append(arcade.load_texture("sprites\character\Run__008.png"))
        self.player.walk_right_textures.append(arcade.load_texture("sprites\character\Run__009.png"))
        
        self.player.walk_left_textures.append(arcade.load_texture("sprites\character\Run__000.png",mirrored=True))
        self.player.walk_left_textures.append(arcade.load_texture("sprites\character\Run__001.png",mirrored=True))
        self.player.walk_left_textures.append(arcade.load_texture("sprites\character\Run__002.png",mirrored=True))
        self.player.walk_left_textures.append(arcade.load_texture("sprites\character\Run__003.png",mirrored=True))
        self.player.walk_left_textures.append(arcade.load_texture("sprites\character\Run__004.png",mirrored=True))
        self.player.walk_left_textures.append(arcade.load_texture("sprites\character\Run__005.png",mirrored=True))
        self.player.walk_left_textures.append(arcade.load_texture("sprites\character\Run__006.png",mirrored=True))
        self.player.walk_left_textures.append(arcade.load_texture("sprites\character\Run__007.png",mirrored=True))
        self.player.walk_left_textures.append(arcade.load_texture("sprites\character\Run__008.png",mirrored=True))
        self.player.walk_left_textures.append(arcade.load_texture("sprites\character\Run__009.png",mirrored=True))

        self.player.walk_up_textures.append(arcade.load_texture("sprites\character\Jump__000.png"))
        self.player.walk_up_textures.append(arcade.load_texture("sprites\character\Jump__001.png"))
        self.player.walk_up_textures.append(arcade.load_texture("sprites\character\Jump__002.png"))
        self.player.walk_up_textures.append(arcade.load_texture("sprites\character\Jump__003.png"))
        self.player.walk_up_textures.append(arcade.load_texture("sprites\character\Jump__004.png"))
        self.player.walk_up_textures.append(arcade.load_texture("sprites\character\Jump__005.png"))
        self.player.walk_up_textures.append(arcade.load_texture("sprites\character\Jump__006.png"))
        self.player.walk_up_textures.append(arcade.load_texture("sprites\character\Jump__007.png"))
        self.player.walk_up_textures.append(arcade.load_texture("sprites\character\Jump__008.png"))
        self.player.walk_up_textures.append(arcade.load_texture("sprites\character\Jump__009.png"))

        self.player.walk_down_textures.append(arcade.load_texture("sprites\character\Slide__000.png"))
        self.player.walk_down_textures.append(arcade.load_texture("sprites\character\Slide__001.png"))
        self.player.walk_down_textures.append(arcade.load_texture("sprites\character\Slide__002.png"))
        self.player.walk_down_textures.append(arcade.load_texture("sprites\character\Slide__003.png"))
        self.player.walk_down_textures.append(arcade.load_texture("sprites\character\Slide__004.png"))
        self.player.walk_down_textures.append(arcade.load_texture("sprites\character\Slide__005.png"))
        self.player.walk_down_textures.append(arcade.load_texture("sprites\character\Slide__006.png"))
        self.player.walk_down_textures.append(arcade.load_texture("sprites\character\Slide__007.png"))
        self.player.walk_down_textures.append(arcade.load_texture("sprites\character\Slide__008.png"))
        self.player.walk_down_textures.append(arcade.load_texture("sprites\character\Slide__009.png"))

        self.score = 0
        self.player.center_x = 128
        self.player.center_y = 128
        self.player.texture = self.player.stand_right_textures[0]
        self.player.scale = 0.15
        self.player_list.append(self.player)
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player,self.wall_list,1.5)

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        self.coin_list.draw()
        self.player_list.draw()
        self.wall_list.draw()
        self.water_list.draw()
        self.plant_list.draw()
        self.goal_list.draw()
        score_text = f"Score: {self.score}"

        # First a black background for a shadow effect
        arcade.draw_text(
            score_text,
            start_x=10 + self.view_left,
            start_y=10 + self.view_bottom,
            color=arcade.csscolor.BLACK,
            font_size=40,
        )
        # Now in white, slightly shifted
        arcade.draw_text(
            score_text,
            start_x=15 + self.view_left,
            start_y=15 + self.view_bottom,
            color=arcade.csscolor.WHITE,
            font_size=40,
        )


    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        self.player.update_animation(delta_time)
        self.physics_engine.update()
        coins_hit_list = arcade.check_for_collision_with_list(self.player, self.coin_list)
        water_hit_list = arcade.check_for_collision_with_list(self.player,self.water_list)
        finish_hit_list = arcade.check_for_collision_with_list(self.player,self.goal_list)
        for goal in finish_hit_list:
            arcade.play_sound(self.finish,4)
            time.sleep(8)
            exit(1)
            
        for water in water_hit_list:
            arcade.play_sound(self.game_over)
            time.sleep(3)
            self.player.center_x = 128
            self.player.center_y = 128
    
            
            
        for coin in coins_hit_list:
            coin.kill()
            self.score += 1
            arcade.play_sound(self.coin_sound)
            
        changed = False

        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left
            changed = True

        
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            changed = True


        if changed:
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                0,
                                SCREEN_HEIGHT)
        
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.UP:
            self.player.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.DOWN:
            self.player.change_y = -PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT:
            self.player.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0     
    
        # Scroll left
    

def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()
    

if __name__ == "__main__":
    main()