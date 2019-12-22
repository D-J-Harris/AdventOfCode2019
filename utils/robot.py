class Robot:
    
    #define a dict of pos changes depending on angle
    angles = ['^', '>', 'v', '<']
    move_dict = {
            '^': -1j,
            'v': 1j,
            '<': -1,
            '>': 1}
    
    def __init__(self, grid, pos, angle_pointer=0):
        self.grid = grid
        self.pos = pos
        self.angle_pointer = angle_pointer
        self.path = []


    # method to return coord of pos above/left/below/right
    def get_coord(self, angle):
        coord = self.pos + self.move_dict[angle]
        x, y = int(coord.real), int(coord.imag)
        return x, y
                     
    @property
    def x(self):
        return int(self.pos.real)
    @property
    def y(self):
        return int(self.pos.imag)
        
    @property
    def angle(self):
        return self.angles[self.angle_pointer % 4]
    
    @property
    def left_angle(self):
        return self.angles[(self.angle_pointer-1) % 4]
    
    @property
    def right_angle(self):
        return self.angles[(self.angle_pointer+1) % 4]