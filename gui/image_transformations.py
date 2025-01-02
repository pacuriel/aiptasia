import numpy as np

# Class to perform image transformations triggered by user actions
class ImageTransformations:
    def __init__(self):
        super().__init__()

    # Pan
    def translate(self, offset_x, offset_y):
        mat = np.eye(3)
        mat[0, 2] = float(offset_x)
        mat[1, 2] = float(offset_y)
        self.mat_affine = np.dot(mat, self.mat_affine)
    
    # Zoom base function
    def scale(self, scale:float):
        mat = np.eye(3)
        mat[0, 0] = scale
        mat[1, 1] = scale
        self.mat_affine = np.dot(mat, self.mat_affine)
    
    # Function to zoom at cursor location
    def scale_at(self, scale:float, cx:float, cy:float):
        self.translate(-cx, -cy)
        self.scale(scale)
        self.translate(cx, cy)
    
    def reset_transform(self):
        self.mat_affine = np.eye(3)