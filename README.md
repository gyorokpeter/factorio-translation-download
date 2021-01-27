# factorio-translation-download
Script to download translations from Crowdin

# Why is this necessary?
Factorio gets its translations from Crowdin. However in order to be able to translate strings on Crowdin, the strings must be added to it. According to my observations, the build procedure of Factorio looks like this:

1. Download strings from Crowdin
2. Build the game with the translated strings
3. Push game update to Steam
4. Push any new strings to Crowdin

This process has a glaringly obvious flaw: as long as new strings are being added to the game, it is impossible to achieve a 100% complete translation because translators don't get a chance to translate the new strings before they are added to the live game. The only exception is when a new release doesn't contain any new strings and translators were quick enough to translate everything before that release comes out. But that's once again ruined if a new release comes out with new strings. A very conspicuous example was the 1.0.0 release which introduced lots of spidertron-related strings, causing them to be untranslated in the supposedly finished version of the game that would be the first version seen by people who avoid early access games.
New strings also happen all the time, sometimes for trivial reasons that are specific to English (e.g. using singular vs plural, American vs British spelling, use of punctuation) and shouldn't even have an effect on translations but they do because that's how the system is set up. These are quickly resolved using Crowdin's TM (Translation Memory) feature but still a human must be there to press the button.

Since I wanted to create a video series with all strings fully translated, I came up with this script that downloads every string from Crowdin and puts them into their correct places in the Factorio game directory. It uses the Crowdin API to download every string. (The "download" button on crowdin is not useful for this as it downloads the prior version, without the new strings.)

# Usage
You must have an account on Crowdin and create an API token in it. Create a config.json file with the following content:
```
{"token":"<insert crowdin token here>"}
```
Obviously don't make it world-readable if you want to keep this file there for a long time.
Look into the script and change the Factorio path to match yours.
Also change the language variable at the top to download a language other than Hungarian.
Then invoke the script as ```python download.py```.
I have used it with Python 3.8.5.
Game updates or checking file integrity in Steam will undo the effects of the script.
