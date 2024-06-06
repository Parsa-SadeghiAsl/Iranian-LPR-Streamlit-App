import cv2
import numpy as np
import math

def count_digits(string):
    count = 0
    for char in string:
        if char.isdigit():
            count += 1
    return count

def PlateReader(PlateReaderModelPath, image, conf=0.65):
    farsi_to_english = {
        'ALIF': 'ا',
        'BE': 'ب',
        'PE': 'پ',
        'TE': 'ت',
        'SE': 'ث',
        'JIM': 'ج',
        'CHE': 'چ',
        'HE': 'ح',
        'KHE': 'خ',
        'DAL': 'د',
        'ZAL': 'ذ',
        'RE': 'ر',
        'ZE': 'ز',
        'ZHE': 'ژ',
        'SIN': 'س',
        'SHIN': 'ش',
        'SAD': 'ص',
        'ZAD': 'ض',
        'TA': 'ط',
        'ZA': 'ظ',
        'AIN': 'ع',
        'GHAIN': 'غ',
        'FE': 'ف',
        'GHAF': 'ق',
        'KAF': 'ک',
        'GAF': 'گ',
        'LAM': 'ل',
        'MIM': 'م',
        'NUN': 'ن',
        'VAV': 'و',
        'HE': 'ه',
        'YE': 'ی',
        'HAMZE': 'ء'
    }
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.merge([image, image, image])
    # Assuming PlateReaderModelPath is available in this module
    CLASS_NAMES_DICT = PlateReaderModelPath.model.names
    results = PlateReaderModelPath(image, verbose=False)
    pelak = []
    for r in results:
        boxes = r.boxes
        for box in boxes:
            ConfOfBox = math.ceil(box.conf[0] * 100) / 100
            x1, y1, x2, y2 = box.xyxy[0]
            cls = int(box.cls[0])
            currentClass = CLASS_NAMES_DICT[cls]
            if ConfOfBox >= conf:
                pelak.append([x1.item(), currentClass])
    pelak.sort(key=lambda x: x[0])
    cop = str()
    for p in pelak:
        cop += f'{p[1]}'

    if count_digits(cop) == 7 and cop[:2].isnumeric() and cop[-5:].isnumeric():
        cop = cop.strip()
        cop = cop.replace(cop[2:-5], farsi_to_english[cop[2:-5]])
        return cop
    else:
        return False
