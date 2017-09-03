# Second Shooter

Scripted camera control.

During the Great American Eclipse, I spent way too much time with my head down,
adjusting camera settings during totality instead of looking around. Afterwards,
I swore that next time, I would automate the shooting process. This is the
result.

Script the camera control with [YAML](http://yaml.org), and run 
second_shooter.py with that file. Second shooter will step through the YAML, 
and execute the commands in order.

## Requirements

* Python 3.5 or greater.
* gphoto2 command line interface.
* gphoto2-compatible camera attached to the computer.

## Commands

Camera commands are written as YAML directives. Directives in YAML are
separated by `---`

### Capture

Take a picture.

    cmd: capture
    
### Set Aperture

Set the camera's aperture.

    cmd: aperture
    value: <aperture value>
    
where `aperture value` value is the f-number to set the aperture to.

### Set ISO

Set the camera's ISO.

    cmd: iso
    value: <iso value>
    
where `iso value` is the ISO value to set the camera to.
    
### Set Shutter Speed

Set the camera's shutter speed.

    cmd: shutter
    value: <speed>
    
where `speed` is the shutter speed as a fraction of a second (1/N).

### Wait

    cmd: wait
    value: <duration>
    
where `duration` is the time to wait after the completion of the previous 
command in seconds.

## Design

* auto detect camera.
* load command set for camera.
* iterate yaml directives.

## Gphoto2 command arguments of interest

--auto-detect
    detect attached camera
    can grep output for camera manufacturer.
--capture-image
    take a picture.
--set-config <entry>=<value>
    entry is the path value of interest from --list-config
    value is the actual value setting, not the index.
--set-config-index <entry>=<value>
    entry is the path value of interest from --list-config
    value is the index of the value wanted.

### Nikon entries of interest

/main/imgsettings/iso
/main/capturesetting/f-number
/main/capturesettings/shutterspeed (as decimal)
/main/capturesettings/shutterspeed2 (as fraction)

## License

Copyright 2017, Andrew Lin.
All rights reserved.

This software is released under the BSD 3-clause license. See
LICENSE.txt or https://opensource.org/licenses/BSD-3-Clause for more
information.
