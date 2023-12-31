from pylabware import Optimax
import os
import cv2
import time
from heinsight.liquidlevel.liquid_level import LiquidLevel
from heinsight.liquidlevel.track_tolerance_levels import \
    TrackLiquidToleranceLevels, TrackOneLiquidToleranceLevel, TrackTwoLiquidToleranceLevels


# main TODO
# Play with iControl to find a method to detect when an experiment has ended
# Learn about how those main opencv methods work

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

def take_then_put(distill_temp, distill_volumes, add_volume, iterator, threshold=0.01):
    """
    Distill down to a pre-defined number of volumes and then add more solvent.
    Note that liquid level start method should have been called before this method is run.

    :param distill_temp: the temeprature to maintain the jacket at for for distillation.
    :param distill_volumes: the number of volumes to distill down to.
    :param add_volumes: the volume (in ml) of solvent to add in after the distill_volumes value has been reached.
    :param threshold: the theshold % diff value below which the liquid level is said to have reached the ref line.
    """

    #  Create and start an iControl experiment that stirs and heats the reaction mixture
    print("creating experiment")
    clr._create_experiment(f"take {distill_volumes} {iterator}")
    clr._click_phase_1()
    clr._add_stirring_step(400,20)
    clr._add_temperature_step(distill_temp, 5, 'Tj')
    clr._add_waiting_step(35000) # wait for a long time - exp should not end
    print("starting experiment")
    clr.start()

    # Every 50 seconds, pause the experiment, and run liquid_level analysis
    while True:
        time.sleep(50)
        print("pausing stirring")
        clr.set_stirrer_live(80) # slow stirring
        time.sleep(5) # wait a few seconds for liquid level to settle
        cap = cv2.VideoCapture(RTSP_URL) # open video feed
        print("taking picture")
        _, image = cap.read() # take a picture with the camera
        image = resize(image)
        cap.release() # close video feed
        print("resuming stirring")
        clr.set_stirrer_live(400) # resume stirring
        print("running analysis")
        _, percent_diff = liquid_level.run(input_image=image, volume=str(distill_volumes))  # will return % diff from volume ref line specified
        if percent_diff < threshold:
            print("percent diff is less than threshold, moving on to adding solvent")
            clr.stop()
            time.sleep(10)
            break # leave the while loop
        else:
            print("percent diff is above threshold, continuing with heating")

    #  Create and start an iControl experiment that adds solvent
    print("creating experiment to add solvent")
    clr._create_experiment(f"put {add_volume} ml {iterator}")
    clr._click_phase_1()
    clr._add_stirring_step(400,20)
    clr._add_dosing_step(add_volume)
    clr._add_end_experiment_step()
    clr.start()

    # check if the experiment has ended every 30 sec
    while True:
        time.sleep(30)
        print("checking if experiment has ended")
        ended = clr.end_of_experiment_check()
        if ended == True:
            print("experiment has ended")
            break


def take(distill_temp, distill_volumes, iterator, threshold=0.01):
    # TODO update to same as take_then_put
    """
    Distill down to a pre-defined number of volumes and then add more solvent.
    Note that liquid level start method should have been called before this method is run.

    :param distill_temp: the temeprature to maintain the jacket at for for distillation.
    :param distill_volumes: the number of volumes to distill down to.
    :param add_volumes: the volume (in ml) of solvent to add in after the distill_volumes value has been reached.
    :param threshold: the theshold % diff value below which the liquid level is said to have reached the ref line.
    """

    #  Create and start an iControl experiment that stirs and heats the reaction mixture
    print("creating experiment")
    clr._create_experiment(f"take {distill_volumes} {iterator}")
    clr._click_phase_1()
    clr._add_stirring_step(400,20)
    clr._add_temperature_step(distill_temp, 5, 'Tj')
    clr._add_waiting_step(35000) # wait for a long time - exp should not end
    clr.start()

    # Every 50 seconds, pause the experiment, and run liquid_level analysis
    while True:
        time.sleep(50)
        print("pausing stirring")
        clr.set_stirrer_live(80) # slow stirring
        time.sleep(5) # wait a few seconds for liquid level to settle
        cap = cv2.VideoCapture(RTSP_URL) # open video feed
        print("taking picture")
        _, image = cap.read() # take a picture with the camera
        image = resize(image)
        cap.release() # close video feed
        print("resuming stirring")
        clr.set_stirrer_live(400) # resume stirring
        print("running analysis")
        _, percent_diff = liquid_level.run(input_image=image, volume=str(distill_volumes))  # will return % diff from volume ref line specified
        if percent_diff < threshold:
            print("percent diff is less than threshold, stopping experiment")
            clr.stop()
            time.sleep(10)
            break # leave the while loop
        else:
            print("percent diff is above threshold, continuing with heating")


clr = Optimax(device_name="radleys_clr", port="COMX", connection_mode="serial", address="00", experiment_name="test1")
clr.simulation = False

clr._test_exe_path()
clr.initialize_device()

RTSP_URL = "rtsp://admin:Reolink5@10.236.65.56:554/h264Preview_01_main"

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

# image for initial selection of region of interest
cap = cv2.VideoCapture(RTSP_URL) # open video feed
time.sleep(2) # allow camera feed to initialise
_, image = cap.read() # take a picture with the camera
image = resize(image)
cap.release() # close the video feed
liquid_level.start(image=image, select_region_of_interest=True, set_reference=True, 
    volumes_list = ['3.5', '4', '6'], select_tolerance=False)


#take_then_put(95, 3.5, 54, 0)
#take_then_put(115, 4, 54, 1)
take_then_put(120, 4, 54, 2)
#take(115, 6, 3)



