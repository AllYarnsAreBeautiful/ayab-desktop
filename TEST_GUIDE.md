# AYAB Testing Guide

## Find a build

The full list of builds is on the [releases](https://github.com/AllYarnsAreBeautiful/ayab-desktop/releases) page. If you're looking for a specific build, you should be able to find it there.

If you're just interested in poking around, choose the most recent build.

When you click on a build you should see a list of files under the **Assets** section. Click on the correct file for your operating system. If you're on a mac, you want the **.dmg**, if you're on windows you want the **.exe**, if you're on Linux you'll have to build from source.

Open the file you downloaded and install it the way you normally would.

### Extra Mac setup

If your Mac shows an error that ```“AYAB” cannot be opened because the developer cannot be verified.``` you need to update security settings to allow this app.

Open the Apple menu (the apple on the top left corner of your screen), and click **System Settings**.

Click **Privacy & Security**.

Scroll down to the Security section and where you see ```"AYAB" was blocked from use because it is not from an identified developer.``` click on the **Open Anyway** button. It will ask for your password.

Try opening the app again.

## Open the app

Launch the app the way you normally would. It's going to give you a popup that there's a new version of the firmware available, you can ignore that.

Click **Ok** to dismiss the dialog.

## Install the firmware

These releases have the corresponding firmware bundled in. You no longer need to specify which machine  you have for the firmware.

Connect your AYAB hardware to your computer.

Go to **Tools** then **Load AYAB Firmware**. 

Under the **Controller** section, select **uno**.

Under the **Firmware Version** section select the only option there and click **Flash**

## Select machine type

In this version of the desktop software, you need to tell it which machine you're working with.

Go to **Preferences** in the top bar, then select **SetPreferences** and set your machine type and any other defaults you want.

## Test

If you're checking on an existing bug, the issue should have some information about how to recreate the issue.

If you're just poking around, use the AYAB software the way you normally would; knit some swatches. 

## File bugs

If, during your testing, you find something that doesn't seem right, let us know! 

You will need a github account for this so if you don't have one, [go create one](https://github.com/signup).

First, look through the [existing issues](https://github.com/AllYarnsAreBeautiful/ayab-desktop/issues) and see if someone else has already reported the problem. If your bug hasn't been reported then you should [create a new issue](https://github.com/AllYarnsAreBeautiful/ayab-desktop/issues/new?assignees=&labels=&projects=&template=bug_report.md&title=%5BBUG%5D).

We have a report template that should be fairly straightforward. Try to make the title descriptive and give us as much information as possible so that we can figure out what's going on. The development team will be notified when you create a new issue and we may be in touch to ask for more information.

## Get help

If you get stuck in this process or you have questions, come say hi in the #testing channel of our [Discord](https://discord.gg/svgGGTfc)!
