from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw


BPM = 60
duration = 30  # Duration of animation (in seconds)
fps = 20  # frames per second
frames = fps*duration

FILE_BASE = f"{BPM}BPM_"
FILE_EXT = "png"

border = 10
resolution = 20  # Size of ball
multiplier = 4  # How many balls will fit inside one meter

velocity = (resolution*multiplier*(BPM/60))/fps


direction = [1, 1]

def create_base(meter_a, meter_b):
    """Creates a visual of a polyrhythm of meter_a against meter_b.
    """
    image_size = (2*border+resolution*(meter_a*multiplier+1), 
                  2*border+resolution*(meter_b*multiplier+1))
    
    img = Image.new("RGB", image_size, "#FFFFFF")

    canvas = ImageDraw.Draw(img)
    
    canvas.rectangle([(0,0), image_size],
                     outline="#000000",
                     width=border)

    return img


def create_frame(base_img, pos):
    new = base_img.copy()
    canvas = ImageDraw.Draw(new)
    bottom_right = [i+resolution for i in pos]  # Bottom right pos of point rectangle
    canvas.rectangle(pos + bottom_right, fill="#FF0000")
    return new
    

if __name__ == "__main__":
    meter_a = int(input("Meter A: "))
    meter_b = int(input("Meter B: "))

    img = create_base(meter_a, meter_b)

    pos = [border, border]

    for frame in range(frames):
        file_name = f"frames\{FILE_BASE}{frame}.{FILE_EXT}"
        create_frame(img, pos).save(file_name)
        print(f"Created frame {frame} of {frames} ({file_name})")

        for i in range(2):
            pos[i] += velocity*direction[i]

            # Checks if point hits border
            if pos[i] <= border or pos[i] + resolution >= (img.size[i] - border):
                direction[i] = -direction[i]





