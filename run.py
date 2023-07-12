
import os
import cv2
from heinsight.liquidlevel.liquid_level import LiquidLevel
from heinsight.liquidlevel.track_tolerance_levels import \
    TrackLiquidToleranceLevels, TrackOneLiquidToleranceLevel, TrackTwoLiquidToleranceLevels

# TODO

# Get a better test picture from the side, so the text on the vessel is less visible
# Try out smaller vol labels -> these should sit to the side of where you want to track the distillation

# Add ability to set multiple reference levels -> add as a dictionary, with keys = no. volumes, values = the normal ref value

# Things I could add to improve HeinSight:
# Ability to also look at color and take that into account when deciding on the liquid level
# Ability to read text labels stuck on the vessel (or even like the vol labels that come printed on some vessels) and find ref level from them

tracker = TrackTwoLiquidToleranceLevels()

image = cv2.imread("/Users/Emma/Documents/Documents - MacBook Pro/Liverpool PhD/Code/auto_distillation/media/test3.jpg")
image_for_run = image.copy()

liquid_level = LiquidLevel(
    camera=None,
    track_liquid_tolerance_levels=tracker,
    use_tolerance=False,
    use_reference=True,
    rows_to_count=30,
    number_of_liquid_levels_to_find=1,
    find_meniscus_minimum=0.03,
    no_error=False,
    liquid_level_data_save_folder=os.path.join(os.path.abspath(os.path.curdir),'logs')
    )


liquid_level.start(image=image, select_region_of_interest=True, set_reference=True, 
    no_reference_lines=3, select_tolerance=False)

liquid_level.run(image=image_for_run)



