import subprocess

def get_sinks():    
    # find all video outputs
    sinks = []
    stdout = subprocess.check_output("xrandr --current", shell=True).decode()
    
    for _, line in enumerate(stdout.splitlines()):
        # looking for "PORT connected "
        if " connected" in line:
            sinks.append(line[0:line.index(" connected")])

    return sinks

def get_current_sink():  
    # find all video outputs
    
    stdout = subprocess.check_output("xrandr --current", shell=True).decode()
    
    if not "*" in stdout:
        # no active rate found
        return None
    
    current_sink = None
    for _, line in enumerate(stdout.splitlines()):

        if " connected" in line:
            current_sink = line[0:line.index(" connected")]
            
        if "*" in line:
            # possible resolution contains star
            # --> indication for current rate 
            #     and therefore  current display
            return current_sink
    
    # no active rate found, which should be impossible
    return None

def off(sink: str):
    cmd = " ".join(["xrandr", f"--output {sink}", "--off"])
    subprocess.run(cmd, shell=True)


def on(sink: str, mode: str, rate: str):
    cmd = " ".join(["xrandr", f"--output {sink}", f"--mode {mode}", f"--rate {rate}"])
    subprocess.run(cmd, shell=True)



if __name__ == "__main__":
    print(get_current_sink())
