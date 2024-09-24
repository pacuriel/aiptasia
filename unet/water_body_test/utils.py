import numpy as np
import cv2

#function to resize (the longest side of) an image given: an image, the desired size
def resizeImage(img: np.ndarray, size: int) -> np.ndarray:
    max_dim_idx = np.argmax(img.shape[0:2]) #shape index corresponding to longest side
    other_idx = 0 if max_dim_idx == 1 else 1 #shape index corresponding to min dimension (excluding channels) 
    new_shape = [0]*2 #initialzing list of zeros to store new shape
    new_shape[max_dim_idx] = size #setting longest side of image to desired size
    new_shape[other_idx] = int(img.shape[other_idx] * (size / img.shape[max_dim_idx])) #setting smallest side of image to maintain asepct ratio
    new_shape = tuple(reversed(new_shape)) #reversing tuple bc cv2 shape dims are weird
    return cv2.resize(img, new_shape) #returning resized img

#function to make an image square using padding
def makeImageSquare(img: np.ndarray, size: int, padding_type=cv2.BORDER_REFLECT) -> np.ndarray:
    if img.shape[0] == img.shape[1]: #check if img is already square
        return img
    
    square = np.zeros(shape=(size,size,img.shape[2])) #initalizing image-shaped square of zeross

    max_dim_idx = np.argmax(img.shape) #assumes img.shape[max_dim_idx] == size
    # other_idx = 0 if max_dim_idx == 1 else 1

    height, width = img.shape[0], img.shape[1] #height, width of image

    if max_dim_idx == 0: #height == size -> resize width
        padding = (size - width) // 2 #size of padding to use on width
        #adding padding to width
        square = cv2.copyMakeBorder(src=img, top=0, bottom=0, left=padding, right=padding, borderType=padding_type)        
        
    elif max_dim_idx == 1: #width == size -> resize height
        padding = (size - height) // 2 #size of padding to use on height
        #adding padding to height
        square = cv2.copyMakeBorder(src=img, top=padding, bottom=padding, left=0, right=0, borderType=padding_type)        

    #confirming image is square (sometimes off by one)
    if square.shape[0] != square.shape[1]:
        square = cv2.resize(square, (size, size)) #resizing to square if not already

    return square
