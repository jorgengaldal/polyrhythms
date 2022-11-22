"""
TODO: Rewrite with OOP (more dynamic with default values for functions)
"""


from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw

import glob
import cv2 as cv
import os


class PolyRhythmVisual:
    def __init__(self,
                 meter_a,
                 meter_b,
                 border = 10,
                 resolution = 20,
                 multiplier = 1,
                 duration = 15,
                 fps = 30,
                 bpm = 60):
        """
        TODO Fix docstring
        Creates a visual of a polyrhythm of meter_a against meter_b.

        args:
        meter_a: horisontal meter
        meter_b: vertical meter
        resolution: size of ball
        border: border size in pixels
        multiplier: How many balls will fit inside one division (*meter* number of divisions in a beat)
        duration: number of seconds the video will last
        fps: frames per second
        bpm: beats per minute
        frames_directory: directory to save frames to
        img_extension: file extension for frames
        codec - string representation of FourCC video codec
        """

        self.meter_a = meter_a
        self.meter_b = meter_b
        self.border = border
        self.resolution = resolution
        self.multiplier = multiplier
        self.duration = duration
        self.fps = fps
        self.bpm = bpm

        # Initiate variable for video (NOTE Consider removing)
        self.frames_directory = None
        self.destination = None
        self.img_extension = None
        self.codec = None

        # Calculate extra properties
        self.size = self._calculate_size()
        self.velocity = self._calculate_velocity()
        self.pos = [self.border, self.border]
        self.direction = [1, 1]
        self.frames = self.duration * self.fps

        self.base = self._create_base()

    def video(self,
              frames_directory="frames",
              destination="output.avi",
              img_extension="png",
              codec="DIVX"):
        
        self.frames_directory = frames_directory
        self.destination = destination
        self.img_extension = img_extension
        self.codec = codec

        print(f"Creating video and saving to {destination}")
        self._create_video()        
        print(f"Video written to {self.destination}")


    @classmethod
    def one_loop(self):
        # TODO
        # Makes an object with the duration of one loop
        pass

    def _calculate_size(self):
        # TODO Add documentation
        return (2*self.border+self.resolution*(self.meter_a*self.multiplier+1),
                2*self.border+self.resolution*(self.meter_b*self.multiplier+1))

    def _calculate_velocity(self):
        # TODO Add documentation
        reference_beat = min(self.size)
        velocity_per_second = (reference_beat) / (self.bpm / 60)
        velocity = int(velocity_per_second / self.fps)
        return velocity

    def _create_base(self):
        """
        TODO Add docstring
        """

        img = Image.new("RGB", self.size, "#FFFFFF")

        canvas = ImageDraw.Draw(img)

        canvas.rectangle([(0, 0), self.size],
                        outline="#000000",
                        width=self.border)

        return img

    def _create_frame(self):
        """Creates single frame"""

        new = self.base.copy()
        canvas = ImageDraw.Draw(new)

        # Bottom right pos of point rectangle
        bottom_right = [i+self.resolution for i in self.pos]

        canvas.rectangle(self.pos + bottom_right, fill="#FF0000")
        return new

    def _create_frames(self):
        """TODO Complete docstring
        args:
        """

        file_base = f"{self.bpm}BPM_"

        for frame in range(self.frames):
            file_name = f"{self.frames_directory}\{file_base}{frame}.{self.img_extension}"
            self._create_frame().save(file_name)
            print(f"Created frame {frame} of {self.frames} ({file_name})")

            self._move_point()

    def _move_point(self):
        """
        Does in-place modification of pos.
        """

        for i in range(2):
            wanted_move = self.velocity * self.direction[i]

            self.direction[i] *= -1  # Assumes border hit

            # Checks first (left/top) border hit
            if (self.pos[i] + wanted_move) <= self.border:
                # print("First border hit")
                to_border_move = self.pos[i] - self.border
                from_border_move = (-wanted_move) - to_border_move
                final_move = -(to_border_move - from_border_move)
                # print(f"{self.pos=}, {to_border_move=}, {wanted_move=}")

            # Checks last (right/bottom) border hit
            elif (self.pos[i] + wanted_move + self.resolution) >= (self.size[i] - self.border):
                # print("Last border hit")
                to_border_move = (
                    self.size[i] - self.border) - (self.pos[i] + self.resolution)
                from_border_move = wanted_move - to_border_move
                final_move = to_border_move - from_border_move

            # No border hit
            else:
                final_move = wanted_move
                self.direction[i] *= -1  # Reverts border hit assumption

            self.pos[i] += final_move

    def _create_video(self):
        """
        Creates a video with OpenCV and returns path to video
        """
        # TODO Clear frames_directory

        images = []

        fourcc_object = cv.VideoWriter_fourcc(*self.codec)
        for filename in sorted(glob.glob(f"{self.frames_directory}/*"), key=os.path.getmtime):
            img = cv.imread(filename)
            images.append(img)

        output = cv.VideoWriter(self.destination, fourcc_object, self.fps, self.size)

        for im in images:
            output.write(im)

        output.release()

if __name__ == "__main__":
    meter_a = int(input("Meter A: "))
    meter_b = int(input("Meter B: "))

    visual = PolyRhythmVisual(meter_a, meter_b)
    visual.video()
