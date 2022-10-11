import datetime

# get date and time to guarantee unique file name:
def file_name():
    currentDT = datetime.datetime.now()
    time_stamp = currentDT.strftime("%Y_%m_%d_%Hh%Mm%Ss")
    return "new_images/IMG" + time_stamp + '.png'
    
# formatted date and time:


# new image name:


# now save image

