import cv2
from PIL import Image, ImageDraw, ImageFont

# Load the template license plate image
template_image = cv2.imread('images/plate_template.png')
def PlateGen(PlateNumber):

    # Convert OpenCV image to PIL image
    template_image_pil = Image.fromarray(cv2.cvtColor(template_image, cv2.COLOR_BGR2RGB))
    num1 = PlateNumber[:2]
    alp = PlateNumber[2]
    num2 = PlateNumber[3:-2]
    num5 = PlateNumber[-2:]
    # Load the recognized plate string

    # Initialize PIL drawing context
    draw = ImageDraw.Draw(template_image_pil)

    # Define font and size
    font = ImageFont.truetype("resources/B Traffic_0.ttf", 190)  # You can change the font and size as needed

    # Define text color
    text_color = (0,0,0)  # White color



    # Draw text on the image
    draw.text((90, 40), num1, fill=text_color, font=font)
    draw.text((340, 30), alp, fill=text_color, font=font)
    draw.text((500, 40), num2, fill=text_color, font=font)
    draw.text((815, 60), num5, fill=text_color, font=font)
    return template_image_pil


