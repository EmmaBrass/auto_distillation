from pylabware import Optimax
import time

clr = Optimax(device_name="radleys_clr", port="COMX", connection_mode="serial", address="00", experiment_name="test1")
clr.simulation = False

clr.experiment_name = 'put 54 ml'
#clr._test_exe_path()
clr.is_connected()
#clr.initialize_device()

#clr._create_experiment(f"put 54 ml")
#clr._click_phase_1()
#clr._add_stirring_step(400,20)
#clr._add_dosing_step(54)
#clr._add_end_experiment_step()
clr.start()

# check if the experiment has ended every 30 sec
while True:
    time.sleep(30)
    print("checking if experiment has ended")
    ended = clr.end_of_experiment_check()
    if ended == True:
        print("experiment has ended")
        break