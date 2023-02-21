import cv2
import numpy as np


class Scenes():
    def __init__(self,img_path,p,n):
        self.scenes = cv2.imread(img_path,cv2.IMREAD_GRAYSCALE) # scene with 2-D array
        assert self.scenes is not None, "image is invalid or does not exist!"
        self.h, self.w = self.scenes.shape
        self.p = p # probability of adjacent trees can burn
        self.scenes[self.scenes == 0] = 1  # FOREST
        self.scenes[self.scenes == 255] = 0 # ROAD
        self.lut = {0: ROAD, 1: FOREST, 2: FIRE, 3: BURNT}
        self.johnny(n)
        # self.show()

    def johnny(self, num_fires):
        "Start fire"
        for _fire in range(num_fires):
            xrand = np.random.randint(0, self.h)
            yrand = np.random.randint(0, self.w)
            self.burn(xrand, yrand, 1)


    # Display RGB image with 2-D array scenes as input
    def show(self):
        r_channel = np.zeros_like(self.scenes)
        g_channel = np.zeros_like(self.scenes)
        b_channel = np.zeros_like(self.scenes)

        for value, rgb in self.lut.items():
            r_channel[self.scenes == value] = rgb[0]
            g_channel[self.scenes == value] = rgb[1]
            b_channel[self.scenes == value] = rgb[2]

        # merge the color channels to create the RGB image
        rgb_img = cv2.merge((b_channel, g_channel, r_channel))

        cv2.imshow('scenes',rgb_img)
        cv2.waitKey(1)

    def burn(self, x, y, p):
        if np.random.random() < p:
            self.scenes[x, y] = 2

    def step(self):
        grid = np.copy(self.scenes)
        for x in range(self.h):
            for y in range(self.w):
                if grid[x, y] == 2:
                    # neightbours = [(x-1, y), (x, y-1),
                    #                (x+1, y), (x, y+1)]
                    neighbors = [(x-1, y), (x, y-1),
                                 (x+1, y), (x, y+1), (x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1)]
                    for xn, yn in neighbors:
                        if (self.is_valid(xn, yn) and grid[xn, yn] == 0) or (self.is_valid(xn, yn) and grid[xn, yn] == 1):
                            self.burn(xn, yn, self.p)
                            # pass

                    self.scenes[x, y] = 3
        self.show()

    def is_valid(self, x, y):
        if x < 0 or x >= self.h or y < 0 or y >= self.w:
            return False
        else:
            return True

    def get_nb_tree(self):
        nb_tree = 0
        for x in range(self.h):
            for y in range(self.w):
                if self.scenes[x, y] == 1:
                    nb_tree += 1
        return nb_tree

    def is_over(self):
        for x in range(self.h):
            for y in range(self.w):
                if self.scenes[x, y] == 2:
                    return False
        return True

    def update(self):
        self.step()

    def save(self, filepath):
        r_channel = np.zeros_like(self.scenes)
        g_channel = np.zeros_like(self.scenes)
        b_channel = np.zeros_like(self.scenes)

        for value, rgb in self.lut.items():
            r_channel[self.scenes == value] = rgb[0]
            g_channel[self.scenes == value] = rgb[1]
            b_channel[self.scenes == value] = rgb[2]

        # merge the color channels to create the RGB image
        rgb_img = cv2.merge((b_channel, g_channel, r_channel))

        cv2.imwrite(filepath,rgb_img)
    def play(self, num_steps=None):
        if num_steps is None:
            while not scenes.is_over():
                scenes.step()
        elif isinstance(num_steps, int):
            for i in range(num_steps):
                if not scenes.is_over():
                    scenes.step()
        else:
            print("number of steps should be posivite integer or None")
            

if __name__ == '__main__':
    # Define display (R, G, B)
    ROAD = (255, 255, 255) # 0
    FOREST = (128, 128, 128)   # 1
    FIRE = (255, 0, 0)     # 2
    # SMOKE = (128, 128, 128)
    BURNT = (0, 0, 0)      # 3
    
    scenes = Scenes('./example.png', p=0.4, n=10) # Binary Mask from Road Extraction
    scenes.play(num_steps= 100)
    
    scenes.save(filepath = 'sim_res.jpg')