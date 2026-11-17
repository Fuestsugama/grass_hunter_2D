from os import walk
import pygame

def frame_number(file_name):
    # '10.png' -> 10, so frames play in order 0,1,2...10 and not 0,1,10,2...
    stem = file_name.split('.')[0]
    return (int(stem) if stem.isdigit() else float('inf'), file_name)

def import_folder(path):
    surface_list = []
    for _,__,img_files in walk(path):
        for image in sorted(img_files, key = frame_number):
            if not image.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                continue    # skips stray files such as Thumbs.db or desktop.ini
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list