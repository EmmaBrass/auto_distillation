from pylabware import Optimax
import os
import cv2
import time
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
clr = Optimax(device_name="radleys_clr", port="COMX", connection_mode="serial", address="00", experiment_name="test1")
clr.simulation = False

clr._test_exe_path()
clr.initialize_device()

clr._add_stirring_step(200,20)
clr._add_dosing_step(54)

def take_then_put(distill_temp, distill_volumes, add_volume, threshold):
    """
    Distill down to a pre-defined number of volumes and then add more solvent.
    Note that liquid level start method should have been called before this method is run.

    :param distill_temp: the temeprature to maintain the jacket at for for distillation.
    :param distill_volumes: the number of volumes to distill down to.
    :param add_volumes: the volume (in ml) of solvent to add in after the distill_volumes value has been reached.
    :param threshold: the theshold % diff value below which the liquid level is said to have reached the ref line.
    """

    #  Create and start an iControl experiment that stirs and heats the reaction mixture
    clr._create_experiment()
    clr._add_stirring_step(400,20)
    clr._add_temperature_step(distill_temp)
    clr._add_waiting_step(600000) # wait for a long time - exp should not end
    clr.start()

    # Every 30 seconds, pause the experiment, and run liquid_level analysis
    while True:
        time.sleep(45)
        _, percent_diff = liquid_level.run(image=image_for_run, volume=distill_volumes)  # will return % diff from volume ref line specified
        if percent_diff < threshold:
            clr.end()

    


# For running the whole process...

# Initial step of user setting the desired volune levels
# Save these as a dict
# User sets order to assess... e.g. first step is wait until at 4 vols



# Turn reactor on, heat to specified temp 
# Stop stirring every 30 sec, take a picture, then resume stirring
# Analyse pic and return distance from liquid level to ref level for current step
# If at ref level, stop, otherwise continue
# If at ref level, pump in x ml of next solvent
# 

# use experiment pause method to pause, take a pic, analyse, then resume!

tracker = TrackTwoLiquidToleranceLevels()

image = cv2.imread("/Users/Emma/Documents/Documents - MacBook Pro/Liverpool PhD/Code/auto_distillation/media/test3.jpg")
image_for_run = image.copy()

liquid_level = LiquidLevel(
    camera=None,
    track_liquid_tolerance_levels=tracker,
    use_tolerance=False,
    use_reference=True,
    rows_to_count=25,
    number_of_liquid_levels_to_find=1,
    find_meniscus_minimum=0.03,
    no_error=False,
    liquid_level_data_save_folder=os.path.join(os.path.abspath(os.path.curdir),'logs')
    )


liquid_level.start(image=image, select_region_of_interest=True, set_reference=True, 
    volumes_list = [3.5, 4, 6], select_tolerance=False)

take_then_put(95, 3.5, 54)

 # will return % diff from volumes lines at 3.5, 4 and 6 volumes in the order specified in the start method

# run method should only take ONE reference level as input -> whereas start should be allowed to use several.



