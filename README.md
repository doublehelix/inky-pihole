# inky-pihole
eInk Display for the PiHole

Inspired by: https://github.com/neauoire/inky-hole

Display the **number of blocked requests, and filtered traffic**, from [Pi-Hole](https://pi-hole.net), on [Pimoroni's Inky pHAT](https://github.com/pimoroni/inky-phat).

<img src='https://raw.githubusercontent.com/doublehelix/inky-pihole/master/preview.jpg?v=1' width="400"/>

- Setup **Pi-Hole**, follow the [installation instructions](https://learn.adafruit.com/pi-hole-ad-blocker-with-pi-zero-w/install-pi-hole).
- Setup **Inky pHAT**, follow the [installation instructions](https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-inky-phat).
- Clone this repo on your [Raspberry Pi Zero W](https://www.raspberrypi.org/products/).

### Display Rotation

*NB:* If you need to Rotate the image displayed on your eInk display, uncomment line 88
```
img = img.rotate(180)
```
This allows you to mount your device with cable at the top instead of the bottom.

## Roadmap
* CPU Temerature Display
  * This currently prevents the display from refreshing on python 3.10 / inky 1.6.2


## Reload automatically every NN minutes

Edit your `crontab` settings.

```
crontab -e
```

Add the following line:

```
*/30 * * * * python /home/pi/inky-pihole/main.py
```
where:
*  `*/30`: is every 30 minutes.
* `.../pi/inky-pihole/...`: **/pi/** is the username, and **/inky-pihole/** is the folder you cloned the repo into.

30 minutes should be a non-obtrusive refresh time for most people. The display can flash quite a lot during updates, so refreshing more regularly is only recommended if you need closer monitoring.

Cheers.

## See also
Remote debugging Python from Visual Studio Code:
* https://www.linkedin.com/pulse/python-remote-debugging-visual-studio-code-raspberry-pi-mircea-dogaru/
