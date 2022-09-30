"""
TODO: Rewrite with OOP (more dynamic with default values for functions)
"""



from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw

import glob
import cv2 as cv


def create_base(meter_a, meter_b,
                border = 10, 
                resolution = 20, 
                multiplier = 4):
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
                 resolution = 20):
    new = base_img.copy()
    canvas = ImageDraw.Draw(new)
    # Bottom right pos of point rectangle
    bottom_right = [i+resolution for i in pos]
    canvas.rectangle(pos + bottom_right, fill="#FF0000")
    return new


def create_frames(base_img,
                  duration = 30,
                  fps = 30,
                  bpm = 60,
                  resolution = 20,
                  border = 10,
                  multiplier = 4,
                  frame_dir = "frames",
                  file_extension = "png"):
    """TODO: Add Docstring
    args:
    resolution - size of ball
    multiplier - How many ball will fit inside one meter
    """
    
    file_base = f"{bpm}BPM_"

    frames = duration * fps

    velocity = (resolution*multiplier*(bpm/60))/fps  # TODO: Fix formula

    pos = [border, border]
    direction = [1, 1]

    for frame in range(frames):
        file_name = f"{frame_dir}\{file_base}{frame}.{file_extension}"
        create_frame(base_img, pos).save(file_name)
        print(f"Created frame {frame} of {frames} ({file_name})")

        for i in range(2):
            pos[i] += velocity*direction[i]

            # Checks if point hits border
            if pos[i] <= border or pos[i] + resolution >= (base_img.size[i] - border):
                direction[i] = -direction[i]


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
    for filename in glob.iglob(f"{img_dir}/*"):
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
    # meter_a = int(input("Meter A: "))
    # meter_b = int(input("Meter B: "))

    # img = create_base(meter_a, meter_b)

    # create_frames(img)


    create_video()
