# A quick script that generates some information about my RPi-based server
# to be served on a Web page (uptime/free disk space/temperature etc)
from datetime import timedelta, datetime
import subprocess

def getUptime():
    with open("/proc/uptime", 'r') as f:
        result = str(timedelta(seconds = int(float(f.readline().split()[0]))))

    return result

def getFreeSpace():
    df = subprocess.Popen(["df", "/dev/sda1", "-h"], stdout=subprocess.PIPE)
    output = df.communicate()[0]
    device, size, used, available, percent, mountpoint = \
        output.splitlines()[1].split()
    return (used,available,percent)

def getTemperature():
    temp = subprocess.Popen(["/opt/vc/bin/vcgencmd", "measure_temp"], stdout=subprocess.PIPE)
    output = temp.communicate()[0]
    return output[5:] # Skip "temp="

def generatePage():
    print("<html><head><title>Stats</title></head><body>")
    print("<h1>sup</h1><hr><p>")
    uptimeLine = "<b>Uptime</b>: " + getUptime() + "<br>"
    freeSpace = getFreeSpace()
    freeSpaceLine = "<b>Disk</b>: used " + freeSpace[0].decode("utf-8") + " (" + \
        freeSpace[2].decode("utf-8") + "), free " + \
        freeSpace[1].decode("utf-8") + "<br>"
    temperatureLine = "<b>Temperature</b>: " + getTemperature() + "<br>"

    print(uptimeLine)
    print(freeSpaceLine)
    print(temperatureLine)

    print("</p>")

    print("<small>Page generated on " + str(datetime.now().date()) + \
        " at " + str(datetime.now().time()) + \
        " by a silly static static page generator written in \
        Python.<br>")
    print("Static used twice deliberately.</small>")
    print("</body></html>")

generatePage()
