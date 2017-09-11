# Second Shooter

Scripted camera control.

During the 2017 Great American Eclipse, I spent way too much time with my head 
down, adjusting camera settings during totality instead of looking around. 
Afterwards, I swore that next time, I would automate the shooting process. This 
is the result.

Script the camera control with [YAML](http://yaml.org), and run 
second_shooter.py with that file. 

    $ python second_shooter.py <script.yaml>

Second shooter will step through the YAML, and execute the commands in order.

If autodetect does not work, or you're controlling multiple cameras with one
computer, you can specify the camera name and port on the command line.

    $ python second_shooter.py --camera [camera] --port [port] <script.yaml>
    
Where `[camera]` is the gphoto2 camera name, and `[port]` is the gphoto2 port
name.

## Requirements

* Python 3.5 or greater.
* [gphoto2](http://gphoto.org/) command line interface.
* gphoto2-compatible camera attached to the computer.

## Commands

Camera commands are written as YAML directives. Directives in YAML start with a
`---`

Note that the YAML parser is very persnickety about formatting, so test your 
scripts! Badly formatted YAML will cause the program to quit.

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

## Example

The following is an example YAML script that brackets exposures one stop down,
and one stop up.

    ---
    cmd: iso
    value: 100
    ---
    cmd: aperture
    value: f/8
    ---
    cmd: shutter
    value: 1/60
    ---
    cmd: capture
    ---
    cmd: shutter
    value: 1/30
    ---
    cmd: capture
    ---
    cmd: shutter
    value: 1/125
    ---
    cmd: capture
   

## License

Copyright 2017, Andrew Lin.
All rights reserved.

This software is released under the BSD 3-clause license. See
LICENSE.txt or https://opensource.org/licenses/BSD-3-Clause for more
information.
