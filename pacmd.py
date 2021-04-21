import subprocess

def get_sinks(card: str = None) -> [str]:
    # find all audio sinks
    sinks = []
    stdout = subprocess.check_output("pacmd list-sinks", shell=True).decode()
    
    currentSink = None
    for _, line in enumerate(stdout.splitlines()):
        
        # looking for "name: <SINK>"
        if "name: <" in line and line.endswith(">"):
            currentSink = line[line.index("<") + 1:-1]

        # looking for "card: \d* <CARD>"
        if "card: " in line and line.endswith(">"):
            currentCard = line[line.index("<") + 1:-1]
            sinks.append((currentSink, currentCard))
    
    if card is not None:
        filtered_sinks = [(s, c) for s, c in sinks if c == card]
        assert (len(filtered_sinks) > 0), f"audio card \"{card}\" not found: {sinks}"
        sinks = filtered_sinks


    return sinks


def get_current() -> str:
    sink = None

    stdout = subprocess.check_output("pacmd stat", shell=True).decode()
    for _, line in enumerate(stdout.splitlines()):
        # looking for "Default sink name: SINK"
        if "Default sink name:" in line:            
            sink = line[line.index(":") + 2:]
            card = next(c for s, c in get_sinks() if s == sink)
    
    return (sink, card)


def set_default_sink(sink: str):
    cmd = " ".join(["pacmd", f"set-default-sink {sink}"])
    subprocess.run(cmd, shell=True)