from pylabware import Optimax
import os
import cv2
import time
from heinsight.liquidlevel.liquid_level import LiquidLevel
from heinsight.liquidlevel.track_tolerance_levels import \
    TrackLiquidToleranceLevels, TrackOneLiquidToleranceLevel, TrackTwoLiquidToleranceLevels

# main TODO
# Play with iControl to find a method to detect when an experiment has ended
# learn about how those main opencv methods work


# Things I could add to improve HeinSight:
# Parallax error correction
# Ability to also look at color and take that into account when deciding on the liquid level
# Ability to read text labels stuck on the vessel (or even like the vol labels that come printed on some vessels) and find ref level from them
# Ability to report back absolute volume difference rather than just htis arbitrary % diff...

def resize(input_image):
    h, w = input_image.shape[:2]
    aspect = h/w
    new_width = 600
    new_height = int(new_width*aspect)
    output_image = cv2.resize(input_image, dsize=(new_width,new_height))
    return output_image

def take_then_put(distill_temp, distill_volumes, add_volume, threshold=0.01):
    """
    Distill down to a pre-defined number of volumes and then add more solvent.
    Note that liquid level start method should have been called before this method is run.

    :param distill_temp: the temeprature to maintain the jacket at for for distillation.
    :param distill_volumes: the number of volumes to distill down to.
    :param add_volumes: the volume (in ml) of solvent to add in after the distill_volumes value has been reached.
    :param threshold: the theshold % diff value below which the liquid level is said to have reached the ref line.
    """

    #  Create and start an iControl experiment that stirs and heats the reaction mixture
    clr._create_experiment(f"take {distill_volumes}")
    clr._click_phase_1()
    clr._add_stirring_step(400,20)
    clr._add_temperature_step(distill_temp, 5, 'Tj')
    clr._add_waiting_step(35000) # wait for a long time - exp should not end
    clr.start()

    # Every 30 seconds, pause the experiment, and run liquid_level analysis
    while True:
        time.sleep(45)
        clr.pause() # pause the experiment to pause stirring
        time.sleep(5) # wait a few seconds for liquid level to settle
        _, image = cap.read() # take a picture with the camera
        image = resize(image)
        clr.start() # resume the experiment
        _, percent_diff = liquid_level.run(image=image, volume=distill_volumes)  # will return % diff from volume ref line specified
        if percent_diff < threshold:
            clr.stop()
            break # leave the while loop

    #  Create and start an iControl experiment that adds solvent
    clr._create_experiment(f"put {add_volume} ml")
    clr._click_phase_1()
    clr._add_stirring_step(400,20)
    clr._add_dosing_step(add_volume)
    clr.start()

    # TODO Need a way here to know if the experiment has completed!!!

def take(distill_temp, distill_volumes, threshold=0.01):
    """
    Distill down to a pre-defined number of volumes and then add more solvent.
    Note that liquid level start method should have been called before this method is run.

    :param distill_temp: the temeprature to maintain the jacket at for for distillation.
    :param distill_volumes: the number of volumes to distill down to.
    :param add_volumes: the volume (in ml) of solvent to add in after the distill_volumes value has been reached.
    :param threshold: the theshold % diff value below which the liquid level is said to have reached the ref line.
    """

    #  Create and start an iControl experiment that stirs and heats the reaction mixture
    clr._create_experiment(f"take {distill_volumes}")
    clr._click_phase_1()
    clr._add_stirring_step(400,20)
    clr._add_temperature_step(distill_temp, 5, 'Tj')
    clr._add_waiting_step(35000) # wait for a long time - exp should not end
    clr.start()

    # Every 30 seconds, pause the experiment, and run liquid_level analysis
    while True:
        time.sleep(45)
        clr.pause() # pause the experiment to pause stirring
        time.sleep(5) # wait a few seconds for liquid level to settle
        _, image = cap.read() # take a picture with the camera
        image = resize(image)
        clr.start() # resume the experiment
        _, percent_diff = liquid_level.run(image=image, volume=distill_volumes)  # will return % diff from volume ref line specified
        if percent_diff < threshold:
            clr.stop()
            break # leave the while loop


clr = Optimax(device_name="radleys_clr", port="COMX", connection_mode="serial", address="00", experiment_name="test1")
clr.simulation = False

clr._test_exe_path()
clr.initialize_device()

cap = cv2.VideoCapture("rtsp://admin:Reolink5@10.236.65.56:554/h264Preview_01_main")

tracker = TrackTwoLiquidToleranceLevels()
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

# image for initial selection of region of interest
_, image = cap.read() # take a picture with the camera
image = resize(image)
liquid_level.start(image=image, select_region_of_interest=True, set_reference=True, 
    volumes_list = [3.5, 4, 6], select_tolerance=False)

take_then_put(25, 3.5, 54)
take_then_put(30, 4, 54)
take_then_put(35, 4, 54)
take(35, 6)
# Initial step of user setting the desired volune levels
# Save these as a dict
# User sets order to assess... e.g. first step is wait until at 4 vols


# use experiment pause method to pause, take a pic, analyse, then resume!




# will return % diff from volumes lines at 3.5, 4 and 6 volumes in the order specified in the start method

# run method should only take ONE reference level as input -> whereas start should be allowed to use several.



