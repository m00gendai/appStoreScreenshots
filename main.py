import os
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from text import texts


def draw_text_with_wrap(draw, text, textFieldSize, max_width, padding, start_y, color=(255, 255, 255)):
    """
        Draw text with word wrap and horizontal centering within a padded area.

        Parameters:
        - draw: ImageDraw object
        - text: The text to draw
        - font: The font to use
        - max_width: The maximum width for each line
        - padding: Padding to add to left and right
        - start_y: The y-coordinate to start drawing text
        - color: Text color
        """
    # Split the text into words
    lines = []
    words = text.split(' ')
    current_line = []

    for word in words:
        # Check if adding the next word would exceed the max_width
        current_line.append(word)
        fontsize = int(textFieldSize / (4*1.5))
        font = ImageFont.truetype("arialbd.ttf", fontsize)
        line_width, _ = draw.textsize(' '.join(current_line), font=font)

        if line_width > max_width:
            # If the current line width exceeds the max_width, remove the last word and start a new line
            current_line.pop()
            lines.append(' '.join(current_line))
            current_line = [word]

    # Append the last line
    lines.append(' '.join(current_line))

    # Draw each line
    y = start_y
    for line in lines:
        # Get the width of the line for horizontal centering within the padded area
        line_width, line_height = draw.textsize(line, font=font)
        x = padding + (max_width - line_width) // 2  # Center within the padded width
        draw.text((x, y), line, font=font, fill=color)
        y += line_height  # Move to the next line


def resize_and_fill(image_path, output, target_size, text):
    img = Image.open(image_path)

    # Get the original image size
    original_size = img.size

    # Calculate the new size, maintaining the aspect ratio
    ratio = min(target_size[0] / original_size[0], target_size[1] / original_size[1])
    new_size = (int((original_size[0] // 1.25) * ratio), int((original_size[1] // 1.25) * ratio))

    # Resize the image
    resized_img = img.resize(new_size, Image.ANTIALIAS)

    # Create a new black background image with the target size
    new_img = Image.new("RGB", target_size, (0, 0, 0))

    # Paste the resized image onto the black background, centering it
    offset = ((target_size[0] - new_size[0]) // 2, 50)
    new_img.paste(resized_img, offset)

    draw = ImageDraw.Draw(new_img)
    textFieldSize = target_size[1] - (new_size[1]+50)

    padding = 50
    max_width = target_size[0] - (2 * padding)  # Subtract 50 pixels total for padding
    start_y = new_size[1]+75
    draw_text_with_wrap(draw, text, textFieldSize, max_width, padding, start_y)
    new_img.save(output)


imageExtensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff')
targetSize_ios_fon_6_9 = (1320, 2868)
targetSize_android_fon = (1080, 1920)
# targetSize_ios_fon_6_7 = (1284, 2778)
# targetSize_ios_fon_6_3 = (1206, 2622)
# targetSize_ios_fon_6_5 = (1170, 2532)
targetSize_ios_pad = (2048, 2732)

targetSizes = [targetSize_ios_fon_6_9, targetSize_android_fon, targetSize_ios_pad]

for targetSize in targetSizes:
    for filename in os.listdir('.'):
        if filename.lower().endswith(imageExtensions):
            if not os.path.exists(f'{targetSize[0]}x{targetSize[1]}'):
                os.makedirs(f'{targetSize[0]}x{targetSize[1]}')
            inputPath = os.path.join('.', filename)

            for entry in texts:
                if inputPath.split("\\")[1].split(".")[0] in entry:
                    img_data = entry[inputPath.split("\\")[1].split(".")[0]]
                    for lang in img_data:
                        outputPath = os.path.join(f'{targetSize[0]}x{targetSize[1]}',
                                                  f'{targetSize[0]}x{targetSize[1]}_{lang}_{filename}')
                        resize_and_fill(inputPath, outputPath, targetSize, img_data[lang])
                        print(f'Processed {filename} and saved to {outputPath}')

