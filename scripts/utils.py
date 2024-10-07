import pygame, os

BASE_IMG_PATH = 'data/images/'

def load_image(path):
    #convert() is really good to use as it chhanges internal 
    # reperesentation of img in pygame which makes it efficient
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((255, 255, 255))
    return img

def load_images(path):
    images = []
    for img_name in os.listdir(BASE_IMG_PATH + path):
        images.append(load_image(path + '/' + img_name))
    return images