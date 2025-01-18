SINGLE = 1
DOUBLE = 2

WIDTH,HEIGHT = 1200,650
ORIGIN_POINT = [WIDTH/2, HEIGHT/3]

GAME_FRAME_SPEED = 60         # 60 updates frames per second
GAME_PHYSICS_SPEED =20       # update physics every 20 milliseconds

GRAVITY = 0.3#9.81          # 9.81 m per second^2
SPEED_LIMIT = 0.5

BORDER_THICKNESS = 5

simulationState = "asdf"
    # "STARTMENU"   "ABOUTMENU"   "SIMULATION"  "QUIT"

def changeState(newState):
    global simulationState
    simulationState = newState


pen_array = []
pen_edit_array = []

