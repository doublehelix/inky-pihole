# inky-pihole
eInk Display for the PiHole

Inspired by: https://github.com/neauoire/inky-hole

Display statistics including the **number of blocked requests, and filtered traffic**, from [Pi-Hole](https://pi-hole.net), on [Pimoroni's Inky pHAT](https://github.com/pimoroni/inky-phat).

Default display / Simple display (using `--simple` option):  
<img src='https://raw.githubusercontent.com/doublehelix/inky-pihole/master/preview.jpg?v=1' width="300"/> 
<img src='https://raw.githubusercontent.com/doublehelix/inky-pihole/master/preview_simple.jpg?v=1' width="300"/>


LCARS display (using `--lcars` option) / LCARS + Simple:  
<img src='https://raw.githubusercontent.com/doublehelix/inky-pihole/master/preview_lcars.jpg?v=1' width="300"/> 
<img src='https://raw.githubusercontent.com/doublehelix/inky-pihole/master/preview_lcars_simple.jpg?v=1' width="300"/>

## Installation

1. Setup **Pi-Hole**, follow the [installation instructions](https://learn.adafruit.com/pi-hole-ad-blocker-with-pi-zero-w/install-pi-hole).
2. Setup **Inky pHAT**, follow the [installation instructions](https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-inky-phat).
3. Clone this repo on your [Raspberry Pi Zero W](https://www.raspberrypi.org/products/).
    ```
    git clone https://github.com/doublehelix/inky-pihole.git
    ```

### Test your setup
Executing the following command will run the script once and update the eInk display:
```
python ./inky-pihole/main.py
```

## Options
All command line optins are optional and the default values when left out are detailed below.
* `-a` , `--apihosts`  
  A comma separated list of your Pi-Hole host names.  
  e.g.: `--apihosts "192.168.1.10, 192.168.1.11"`  
  *(Defaults to `"127.0.0.1"` if omitted)*  
  *NOTE:* If you have more than one pi-hole (i.e. primary and secondary pi-hole DNS servers), the statistics will be consolidated.
  This is because all clients can talk to one or both of the pi-hole servers.
  Therefore, the total number of requests and blocked queries will be the **combined** values from all servers. Whereas the total number of blocked domains and clients will be the **greater** of the unique values from each server.

* `--tz`  
  Set the TimeZone of your pi-hole for date/time display purposes.  
  e.g. `--tz "Australia/Melbourne"` or `--tz "Etc/GMT-10"`  
  *(Defaults to `"UTC"` if omitted)*  

* `-r` , `--rotate`  
  Rotates the display 180 degrees.  
  This allows you to mount your device with cable at the top instead of the bottom.

* `-s` , `--simple`  
  Show a simplified display with three large numeric values:
    * +Number of Queries
    * -Number Blocked
    * Blocked Ratio %

* `-l` , `--lcars`  
  Show a Star Trek inspired LCARS console style display

** *NOTE:* You can combine the `--lcars` and `--simple` options to display the LCARS background with the simple stats display (text will be all white).

### Help options
These functions will NOT update the display, and output help information to the console only.

* `-h` , `--help`  
  Display command line options

* `--timezones`  
  Display all available time zone names


## Automatic / Scheduled update
*NOTE:* The following assumes you're logged in a the `pi` user, and your home directory is `/home/pi`. (which was the folder you cloned the `inky-pihole` repository into)

Edit your `crontab` settings.

```
crontab -e
```

Add the following line:
```
*/30 * * * * python /home/pi/inky-pihole/main.py
```
Or, add some command line options:
```
*/30 * * * * python /home/pi/inky-pihole/main.py --rotate --lcars --simple --apihosts "10.0.0.10,10.0.0.11" --tz "Australia/Melbourne"
```

30 minutes should be a non-obtrusive refresh time for most people. The display can flash quite a lot during updates, so refreshing more regularly is only recommended if you need closer monitoring.

Cheers.


## Roadmap
* CPU Temerature Display - This currently prevents the display from refreshing on python 3.10 / inky 1.6.2.


## See also

Inky-phat:
* Docs: http://docs.pimoroni.com/inkyphat/
* GitHub: https://github.com/pimoroni/inky-phat

Python Image Library (PIL):
* https://pillow.readthedocs.io/en/stable/reference

Signika Font:
* https://fonts.google.com/specimen/Signika

Remote debugging Python from Visual Studio Code:
* https://www.linkedin.com/pulse/python-remote-debugging-visual-studio-code-raspberry-pi-mircea-dogaru
