# appStoreScreenshots
Programatically generates Screenshots for App Stores with texts in different locales.
I rather spent more time developing a script that does it for me than doing it by hand.
Much of it is with chatGPT support.

Have your app screenshots in the same folder and with the same name as in ```text.py```

Add your needed resolutions for the different App Stores as needed:

```
targetSize_ios_fon_6_9 = (1320, 2868) # 6.9 inch resolution for iOS
targetSize_android_fon = (1080, 1920) # default Android resolution
targetSize_ios_pad = (2048, 2732)     # default iPdad resolution

targetSizes = [targetSize_ios_fon_6_9, targetSize_android_fon, targetSize_ios_pad] # make sure the sizes are in the array
```

Currently generates a black background and a scaled screenshot in portrait mode.
Text underneath is in mind with a four line maximum, centered with a 50px padding to the screenshot.

Adjust ```fontsize = int(textFieldSize / (4*1.5))``` accordingly.
Text will line wrap automatically.
