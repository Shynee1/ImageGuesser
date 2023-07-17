from PIL import Image, ImageDraw
import cairo
import numpy as np
import rdp

def processStrokes(strokes):
    
    align_to_corner(strokes)
    scale_image(strokes)
    #strokes = [resample_stroke(stroke) for stroke in strokes]
    for i in range(len(strokes)):
        strokes[i] = rdp.rdp(strokes[i], epsilon=2.0)

    return vector_to_raster([strokes])

def vector_to_raster(vector_images, side=28, line_diameter=16, padding=16, bg_color=(0,0,0), fg_color=(1,1,1)):
  
    original_side = 255.
    
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, side, side)
    ctx = cairo.Context(surface)
    ctx.set_antialias(cairo.ANTIALIAS_BEST)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_line_width(line_diameter)

    total_padding = padding * 2. + line_diameter
    new_scale = float(side) / float(original_side + total_padding)
    ctx.scale(new_scale, new_scale)
    ctx.translate(total_padding / 2., total_padding / 2.)

    raster_images = []
    for vector_image in vector_images:
        # clear background
        ctx.set_source_rgb(*bg_color)
        ctx.paint()
        
        bbox = np.hstack(vector_image).max(axis=1)
        offset = ((original_side, original_side) - bbox) / 2.
        offset = offset.reshape(-1,1)
        centered = [stroke + offset for stroke in vector_image]

        ctx.set_source_rgb(*fg_color)        
        for xv, yv in centered:
            ctx.move_to(xv[0], yv[0])
            for x, y in zip(xv, yv):
                ctx.line_to(x, y)
            ctx.stroke()
        
        data = surface.get_data()
        raster_image = np.copy(np.asarray(data)[::4])
        raster_images.append(raster_image)

        """
        format = surface.get_format()
        size = (surface.get_width(), surface.get_height())
        stride = surface.get_stride()

        image = None

        with surface.get_data() as memory:
            if format == cairo.Format.RGB24:
                image =  Image.frombuffer(
                    "RGB", size, memory.tobytes(),
                    'raw', "BGRX", stride)
            elif format == cairo.Format.ARGB32:
                image = Image.frombuffer(
                    "RGBA", size, memory.tobytes(),
                    'raw', "BGRa", stride)
            else:
                raise NotImplementedError(repr(format))

        image.show()
        """
        
    return raster_image

def align_to_corner(strokes):
    # Find the minimum values of x and y coordinates across all strokes
    min_x = min(min(stroke[0]) for stroke in strokes)
    min_y = min(min(stroke[1]) for stroke in strokes)

    # Subtract the minimum values from all x and y coordinates to align to top-left corner
    for stroke in strokes:
        for i in range(len(stroke[0])):
            stroke[0][i] -= min_x
            stroke[1][i] -= min_y

def scale_image(aligned_strokes):
    # Find the maximum values of x and y coordinates across all strokes
    max_x = 0
    max_y = 0
    for stroke in aligned_strokes:
        max_x = max(max_x, max(stroke[0]))
        max_y = max(max_y, max(stroke[1]))

    # Scale the coordinates to have a maximum value of 255
    for stroke in aligned_strokes:
        for i in range(len(stroke[0])):
            stroke[0][i] = (stroke[0][i] / max_x) * 255
            stroke[1][i] = (stroke[1][i] / max_y) * 255
    
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