from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw

FILE_BASE = "60BPM_"
FILE_EXT = "png"

duration = 15 # Duration of animation (in seconds)
fps = 20 # frames per second
frames = fps*duration

BPM = 60
size_multi = 120
velocity = (size_multi*(BPM/60))/fps

point_size = 10
border = 10

direction = [1, 1]

def create_base(meter_a, meter_b):
    """Creates a visual a polyrhythm of meter_a against meter_b.
    """
    image_size = (meter_a*size_multi, meter_b*size_multi)
    
    img = Image.new("RGB", image_size, "#FFFFFF")

    canvas = ImageDraw.Draw(img)
    
    canvas.rectangle([(0,0), image_size],
                 outline="#000000",
                 width=border)

    return img


def create_frame(base_img, pos):
    new = base_img.copy()
    canvas = ImageDraw.Draw(new)
    br = [i+point_size for i in pos]
    canvas.rectangle(pos + br, fill="#000000")
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
        pos[0] += velocity*direction[0]
        pos[1] += velocity*direction[1]
        if pos[0] =< border or pos[0] + point_size >= (img.width - border):
            direction[0] = -direction[0]
        if pos[1] =< border or pos[1] + point_size >= (img.height - border):
            direction[1] = -direction[1]





