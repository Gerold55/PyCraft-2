from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

# Define chunk size
CHUNK_SIZE = 16
CHUNK_HEIGHT = 16
VIEW_DISTANCE = 2  # Number of chunks in any direction that are visible

# Load textures
grass_texture = load_texture('textures/grass_top.png')
dirt_texture = load_texture('textures/dirt.png')

class Voxel(Entity):
    def __init__(self, position=(0, 0, 0), texture=grass_texture):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1)),
            scale=1
        )

class Chunk(Entity):
    def __init__(self, position=(0, 0, 0)):
        super().__init__()
        self.position = position
        self.generate_chunk()

    def generate_chunk(self):
        for z in range(CHUNK_SIZE):
            for x in range(CHUNK_SIZE):
                Voxel(position=(self.position[0] + x, 0, self.position[2] + z), texture=grass_texture)
                for y in range(-1, -CHUNK_HEIGHT, -1):
                    Voxel(position=(self.position[0] + x, y, self.position[2] + z), texture=dirt_texture)

player = FirstPersonController()
chunks = {}

def update():
    global chunks
    player_chunk_x = int(player.x // CHUNK_SIZE)
    player_chunk_z = int(player.z // CHUNK_SIZE)

    # Load chunks
    for x in range(player_chunk_x - VIEW_DISTANCE, player_chunk_x + VIEW_DISTANCE + 1):
        for z in range(player_chunk_z - VIEW_DISTANCE, player_chunk_z + VIEW_DISTANCE + 1):
            if (x, z) not in chunks:
                chunks[(x, z)] = Chunk(position=(x * CHUNK_SIZE, 0, z * CHUNK_SIZE))

    # Unload chunks
    for key in list(chunks.keys()):
        if abs(key[0] - player_chunk_x) > VIEW_DISTANCE or abs(key[1] - player_chunk_z) > VIEW_DISTANCE:
            chunks[key].disable()
            del chunks[key]

app.run()
