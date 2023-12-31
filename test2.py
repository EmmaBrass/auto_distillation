from pylabware import Optimax
import os
import cv2
import time
from heinsight.liquidlevel.liquid_level import LiquidLevel
from heinsight.liquidlevel.track_tolerance_levels import \
    TrackLiquidToleranceLevels, TrackOneLiquidToleranceLevel, TrackTwoLiquidToleranceLevels

def resize(input_image):
    h, w = input_image.shape[:2]
    aspect = h/w
    new_width = 600
    new_height = int(new_width*aspect)
    output_image = cv2.resize(input_image, dsize=(new_width,new_height))
    return output_image

tracker = TrackTwoLiquidToleranceLevels()
liquid_level = LiquidLevel(
    camera=None,
    track_liquid_tolerance_levels=tracker,
    use_tolerance=False,
    use_reference=True,
    rows_to_count=10,
    number_of_liquid_levels_to_find=1,
    find_meniscus_minimum=0.04,
    no_error=False,
    liquid_level_data_save_folder=os.path.join(os.path.abspath(os.path.curdir),'logs')
    )  

start_image = cv2.imread("path/to/image.jpg")
distill_volumes = 4
threshold = 0.01

liquid_level.start(image=start_image, select_region_of_interest=True, set_reference=True, 
    volumes_list = ['3.5', '4', '6'], select_tolerance=False)

run_image = cv2.imread("path/to/image2.jpg")

_, percent_diff = liquid_level.run(input_image=run_image, volume=str(distill_volumes))  # will return % diff from volume ref line specified

if percent_diff < threshold:
    print("above threshold, would keep heating")
else:
    print("below theshold, would move on to next step")