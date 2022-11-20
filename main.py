"""
TODO: Rewrite with OOP (more dynamic with default values for functions)
TODO: Fix border control
"""


from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw

import glob
import cv2 as cv
import os


def create_base(meter_a, meter_b,
                border=10,
                resolution=20,
                multiplier=4):
    """Creates a visual of a polyrhythm of meter_a against meter_b.
    """
    image_size = (2*border+resolution*(meter_a*multiplier+1),
                  2*border+resolution*(meter_b*multiplier+1))

    img = Image.new("RGB", image_size, "#FFFFFF")

    canvas = ImageDraw.Draw(img)

    canvas.rectangle([(0, 0), image_size],
                     outline="#000000",
                     width=border)

    return img


def create_frame(base_img,
                 pos,
                 resolution=20):
    new = base_img.copy()
    canvas = ImageDraw.Draw(new)
    # Bottom right pos of point rectangle
    bottom_right = [i+resolution for i in pos]
    canvas.rectangle(pos + bottom_right, fill="#FF0000")
    return new


def create_frames(base_img,
                  duration=30,
                  fps=30,
                  bpm=60,
                  resolution=20,
                  border=10,
                  multiplier=4,
                  frame_dir="frames",
                  file_extension="png"):
    """TODO: Add Docstring
    args:
    resolution - size of ball
    multiplier - How many ball will fit inside one meter
    """

    file_base = f"{bpm}BPM_"

    frames = duration * fps

    reference_beat = min(base_img.size)
    velocity_per_second = (reference_beat) / (bpm / 60) 
    velocity = int(velocity_per_second / fps) # TODO: Fix formula
    print(velocity)

    pos = [border, border]
    direction = [1, 1]

    for frame in range(frames):
        file_name = f"{frame_dir}\{file_base}{frame}.{file_extension}"
        create_frame(base_img, pos, resolution).save(file_name)
        print(f"Created frame {frame} of {frames} ({file_name})")

        move_point(base_img, pos, direction, velocity, border, resolution)


def move_point(base_img,
              pos,
              direction,
              velocity,
              border,
              resolution):
    """
    Does in-place modification of pos.
    """
    
    for i in range(2):
        wanted_move = velocity * direction[i]

        direction[i] *= -1  # Assumes border hit

        # Checks first (left/top) border hit
        if (pos[i] + wanted_move) <= border:
            print("First border hit")
            to_border_move = pos[i] - border
            from_border_move = (-wanted_move) - to_border_move
            final_move = -(to_border_move - from_border_move)
            print(f"{pos=}, {to_border_move=}, {wanted_move=}")
        
        # Checks last (right/bottom) border hit
        elif (pos[i] + wanted_move + resolution) >= (base_img.size[i] - border):
            print("Last border hit")
            to_border_move = (base_img.size[i] - border) - (pos[i] + resolution)
            from_border_move = wanted_move - to_border_move
            final_move = to_border_move - from_border_move

        # No border hit
        else:
            final_move = wanted_move
            direction[i] *= -1  # Reverts border hit assumption

        pos[i] += final_move


def create_video(img_dir="frames",
                 destination="output.avi",
                 fps=30,
                 fourcc="DIVX"):
    """ Creates a video with OpenCV and returns path to video
    args:
    img_dir - path to directory of frames
    destination - output file destination
    fps - frames per second
    fourcc - string representation of FourCC video codec
    """

    images = []

    fourcc_object = cv.VideoWriter_fourcc(*fourcc)
    for filename in sorted(glob.glob(f"{img_dir}/*"), key=os.path.getmtime):
        img = cv.imread(filename)
        images.append(img)

    height, width, _ = images[0].shape
    size = (width, height)

    output = cv.VideoWriter(destination, fourcc_object, fps, size)

    for im in images:
        output.write(im)

    output.release()

    print(f"Video written to {destination}")

    return destination


if __name__ == "__main__":
    meter_a = int(input("Meter A: "))
    meter_b = int(input("Meter B: "))

    img = create_base(meter_a, meter_b)

    create_frames(img)

    create_video()
