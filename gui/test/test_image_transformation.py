import numpy as np

class ImageTransformations:
    def __init__(self):
        #
        self.affine_matrix = None
    
    # Function to perform panning (translations)
    def translate(self, offset_x, offset_y):
        # Below obtained from section 2.1.1 in Szeliski's "Computer Vision" book
        translation_matrix = np.eye(3) 
        translation_matrix[0, 2] = offset_x
        translation_matrix[1, 2] = offset_y
        
        # Updating affine matrix

    # Resets affine matrix to perform transformations
    def reset_affine_matrix(self):
        self.affine_matrix = np.eye(3)