from PIL import Image, ImageDraw
import numpy as np
import rdp

def processStrokes(strokes):
    strokes = align_to_corner(strokes)
    strokes = scale_image(strokes)
    #strokes = [resample_stroke(stroke) for stroke in strokes]
    strokes = rdp.rdp(strokes, epsilon=2.0)

    return vector_to_raster(strokes)

def vector_to_raster(strokes):
    
    original_side = 255

    image = Image.new("L", (original_side, original_side), color=(0))
    image_draw = ImageDraw.Draw(image)

    for stroke in strokes:
        positions = []
        for i in range(0, len(stroke[0])):
            positions.append((stroke[0][i], stroke[1][i]))
        image_draw.line(positions, fill=(255), width=3)

    return image.resize(size=(28, 28))

def align_to_corner(strokes):
    # Find the minimum values of x and y coordinates across all strokes
    min_x = min(min(stroke[0]) for stroke in strokes)
    min_y = min(min(stroke[1]) for stroke in strokes)

    # Subtract the minimum values from all x and y coordinates to align to top-left corner
    for stroke in strokes:
        for i in range(len(stroke[0])):
            stroke[0][i] -= min_x
            stroke[1][i] -= min_y

    return strokes

def scale_image(aligned_strokes):
    # Find the maximum values of x and y coordinates across all strokes
    max_x = max(max(stroke[0]) for stroke in aligned_strokes)
    max_y = max(max(stroke[1]) for stroke in aligned_strokes)

    # Scale the coordinates to have a maximum value of 255
    for stroke in aligned_strokes:
        for i in range(len(stroke[0])):
            stroke[0][i] = stroke[0][i] * (255 / max_x)
            stroke[1][i] = stroke[1][i] * (255 / max_y)
    
    return aligned_strokes

def resample_stroke(stroke):
    resampled_x = []
    resampled_y = []
    length = len(stroke[0])
    stroke_length = 0.0
    
    # Calculate the total length of the stroke
    for i in range(1, length):
        dx = stroke[0][i] - stroke[0][i - 1]
        dy = stroke[1][i] - stroke[1][i - 1]
        stroke_length += (dx ** 2 + dy ** 2) ** 0.5
    
    # Calculate the spacing between points
    spacing = stroke_length / (length - 1)
    resampled_x.append(stroke[0][0])
    resampled_y.append(stroke[1][0])
    accum_length = 0.0
    i = 1
    
    # Resample the stroke with 1 pixel spacing
    while i < length:
        dx = stroke[0][i] - stroke[0][i - 1]
        dy = stroke[1][i] - stroke[1][i - 1]
        segment_length = (dx ** 2 + dy ** 2) ** 0.5
        if accum_length + segment_length >= spacing:
            # Add a new point with 1 pixel spacing
            fraction = (spacing - accum_length) / segment_length
            nx = stroke[0][i - 1] + fraction * dx
            ny = stroke[1][i - 1] + fraction * dy
            resampled_x.append(nx)
            resampled_y.append(ny)
            stroke[0].insert(i, nx)
            stroke[1].insert(i, ny)
            accum_length = 0.0
        else:
            accum_length += segment_length
            i += 1
    
    return [resampled_x, resampled_y]