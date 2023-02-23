import cv2
import numpy as np
import random


class sence():
    def __init__(self, imgpath, output, fire_spread_prob = 0.2, 
                wind_speed = 5, wind_direction = np.array([1, 0]).reshape(2, 1),
                fire_sim_steps = 100, loc_fire = "middle", fire_radius = 2,
                smoke_sim_steps = 5):

        self.imgpath = imgpath

        # READ IMAGE FROM FILEPATH
        self.img = cv2.imread(imgpath)
        assert self.img is not None, "Img is invalid or not exist!"

        # Define the probability of the fire spreading to a neighboring cell
        self.fire_spread_prob = fire_spread_prob

        # Define the wind direction and speed
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction

        # Define the number of time steps to simulate spread of fire
        self.fire_sim_steps = fire_sim_steps
        if loc_fire == "middle":
            self.loc_fire = (self.img.shape[1] // 2, self.img.shape[0] // 2)
        elif loc_fire == "random":
            self.loc_fire = (np.random.randint(0, self.img.shape[1]),np.random.randint(0, self.img.shape[0]))
        else:
            raise ValueError("parameters of location of fire is invalid!")
            

        # Define the initial radius of the fire
        self.fire_radius = fire_radius

        # Define the smoke simulation steps
        self.smoke_sim_steps = smoke_sim_steps

        # Simulate spread of fire
        firemap = self.fire_sim(if_show_fire = True) # visualize the simulation when if_show is True

        # Simulate spread of smoke based on fire
        smokemap = self.smoke_sim(if_show_smoke = True) # visualize the simulation when if_show is True

        self.save(output, firemap, smokemap)




    def fire_sim(self, if_show_fire = True):

        # Get the initial fire location
        fire_x, fire_y = self.loc_fire

        # Simulate the fire propagation
        for i in range(self.fire_sim_steps):

            # Calculate the new position of the fire source based on the wind direction
            fire_x += int(round(self.wind_speed * self.wind_direction[0, 0]))
            fire_y += int(round(self.wind_speed * self.wind_direction[1, 0]))

            # Update the wind direction randomly
            angle = random.randint(-45, 45)
            rotation_matrix = cv2.getRotationMatrix2D((0, 0), angle, 1)
            self.wind_direction = np.dot(rotation_matrix[:, :2], self.wind_direction)

            # Generate a binary mask of the neighboring cells
            mask = np.zeros_like(self.img, dtype=np.uint8)
            cv2.circle(mask, (fire_x, fire_y), self.fire_radius, (1, 1, 1), -1)
            mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
            mask = (mask > 0).astype(np.uint8)

            # Spread the fire to neighboring cells with a certain probability
            spread_mask = (np.random.rand(*mask.shape) < self.fire_spread_prob).astype(np.uint8)
            spread_mask = cv2.dilate(spread_mask, np.ones((3, 3), np.uint8))
            mask = cv2.bitwise_and(mask, spread_mask)
            for c in range(3):
                self.img[:, :, c] = self.img[:, :, c] * (1 - mask) + mask * np.array([0, 0, 255], dtype=np.uint8)[c]

            # Increase the radius of the fire
            self.fire_radius += 1

            # Draw a red circle at the position of the fire
            cv2.circle(self.img, (fire_x, fire_y), 3, (0, 0, 255), -1)


            # Visualize the simulation of the spread of fire
            if if_show_fire is True:
                cv2.imshow("Fire propagation", self.img)
                cv2.waitKey(40)  # Adjust the wait time as needed

        return self.img[:,:,2] - self.img[:,:,0]
    
    def smoke_sim(self, if_show_smoke = True):
        
        # size of sence to reduce the computation
        size = 100


        # Extract firemap from image
        firemap = cv2.resize(self.img,[size, size]).astype(np.float64)[:,:,2] - cv2.resize(self.img,[size,size]).astype(np.float64)[:,:,0]
        
        # Initialize smokemap
        smoke = np.zeros_like(firemap)
        smoke[firemap==255] = 1.0 # smoke generates from fires


        # Define diffusion parameters
        diffusion_coeff = 0.4
        dt = 0.1

        # Define wind vector
        wind = np.array([1.0, 0.0])

        for step in range(self.smoke_sim_steps):
            print("Smoke Simulation Step {}/{}".format(step+1, self.smoke_sim_steps))

            # Compute Laplacian of smoke concentration
            laplacian = np.roll(smoke, 1, axis=0) + np.roll(smoke, -1, axis=0) \
                        + np.roll(smoke, 1, axis=1) + np.roll(smoke, -1, axis=1) \
                        - 4 * smoke
            
            # Compute advection term using wind vector
            advect = np.zeros_like(smoke)
            for i in range(size):
                for j in range(size):
                    position = np.array([i, j])
                    diff = position -  (size//2, size//2)
                    dist = np.linalg.norm(diff)
                    if dist > 0:
                        direction = diff / dist
                        projection = np.dot(wind, direction)
                        advect[i, j] = projection * smoke[i, j]
            
            # Update smoke concentration using diffusion-advection equation
            smoke += (diffusion_coeff * laplacian - advect) * dt
            smokemap = cv2.resize(smoke, (self.img.shape[1], self.img.shape[0]), interpolation=cv2.INTER_CUBIC)
            smokemap = (smokemap * 255).astype(np.uint8)

            if if_show_smoke == True:
                rgb_smokemap = np.zeros_like(self.img)
                rgb_smokemap[:,:,0] = smokemap
                cv2.imshow('RGB_SMOKE_MAP',rgb_smokemap)
                cv2.waitKey(1)
                cv2.destroyAllWindows()
            
        return smokemap
    
    def save(self, output, firemap, smokemap):
        roadmap = cv2.imread(self.imgpath)

        roadmap[:,:,0][smokemap != 0 ] = 0
        roadmap[:,:,0][firemap != 0 ] = 0
        roadmap[:,:,1][smokemap != 0 ] = 0
        roadmap[:,:,1][firemap != 0 ] = 0
        roadmap[:,:,2][smokemap != 0 ] = 0
        roadmap[:,:,2][firemap != 0 ] = 0

        roadmap[:,:,0][smokemap != 0 ] = 255
        roadmap[:,:,2][firemap != 0 ] = 255

        filepath = output
        cv2.imwrite(filepath, roadmap)
        print("Result has been saved in {}".format(filepath))



if __name__ == "__main__":
    sence(imgpath='70933_maskW.png',output='fire_smoke_propagation_result.png')