import subprocess
import time

import pacmd
import xrandr
import config


# get sink name from command line
import sys
if len(sys.argv) == 1:
    print("no sink specified")
    exit(1)

sink_name = sys.argv[1]

import os
pwd = os.path.dirname(os.path.abspath(__file__))
config_path = f"{pwd}/sinks.json"

success, conf = config.load(config_path, sink_name)

if not success:
    print("sink not configured")
    exit(1)


# ---- launch configured apps
for launch_task in conf.launch:
    subprocess.Popen(launch_task)



# ---- change video
if not conf.xrandr_name == xrandr.get_current_sink():
    if conf.xrandr_name not in xrandr.get_sinks():
        print(f"video sink not found: {conf.xrandr_name}")
    else:
        # turn off all sinks
        #   --> single monitor setup
        for vs in xrandr.get_sinks():
            xrandr.off(vs)
        
        # turn on specified display
        xrandr.on(conf.xrandr_name, conf.resolution, conf.rate)


time.sleep(2)


# ---- change audio
#   card > sink
#   if card matches, but sink does not, but card has only one sink,
#   switch to card, even if sink does not match
currentSink, currentCard = pacmd.get_current()

# assume that current setup is already correct, 
# when the correct card is selected -> ignore current sink
if conf.pacmd_card != currentCard:
    
    sinks = pacmd.get_sinks(conf.pacmd_card)
    if len(sinks) > 0:
        # find preferred sink for this card
        new_sink, new_card = next(((s, c) for (s, c) in sinks if s == conf.pacmd_sink), (None, None))

        if new_sink is None:
            new_sink, new_card =  sinks[0]

        if currentSink != new_sink:
            pacmd.set_default_sink(new_sink)


exit(0)