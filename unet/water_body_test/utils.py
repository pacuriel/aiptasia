import numpy as np
import cv2
import math

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

#function to obtain a list of tiles given an input image and size
def tileImage(img: np.ndarray, tile_size: int = 572) -> list[np.ndarray]:
    """
    Input: 
    - img: image of shape (height, width, channels)
    - tile_size: size of tiles

    Output:
    - List of tiles (images): 
    """
    tiles = [] #list of tiles

    #image is smaller than given tile size
    if img.shape[0] < tile_size or img.shape[1] < tile_size: 
        print("Image size is smaller than tile size")
        return False

    #getting number of tiles along height/width
    tiles_height = math.floor(img.shape[0] / tile_size)
    if (img.shape[0] % tile_size) != 0: tiles_height += 1 #incrementing if not divisble
    tiles_width = math.floor(img.shape[1] / tile_size)
    if (img.shape[1] % tile_size) != 0: tiles_width += 1 #incrementing if not divisble

    num_tiles = tiles_height * tiles_width #total number of tiles

    print(num_tiles, tiles_height, tiles_width)
    
    for h_tile in range(tiles_height):
        for w_tile in range(tiles_width):
            tile_top = h_tile*tile_size
            tile_bottom = (h_tile + 1)*tile_size
            tile_left = w_tile*tile_size
            tile_right = (w_tile + 1)*tile_size

            #check to avoid tile doesn't surpass image height
            if tile_bottom > img.shape[0]:
                tile_bottom = img.shape[0]
                tile_top = tile_bottom - tile_size
            
            #check to avoid tile doesn't surpass image width
            if tile_right > img.shape[1]: 
                tile_right = img.shape[1]
                tile_left = tile_right - tile_size
            
            tile = img[tile_top:tile_bottom, tile_left:tile_right, :]
            tiles.append(tile)
 
    return tiles