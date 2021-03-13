# DBZBT3-Subtitle-Translator
The main purpose of this project is to create a tool to modify subtitles from the game Dragon Ball Z: Budokai Tenkaichi 3.
Feel free to change the code for better, in case of any issues with the code please open a [issue](https://github.com/RicardoCenci/DBZBT3-Subtitle-Translator/issues/new) on the repository page

Keep the originals in case of anything happen
## How to use:
* Download the latest build from the release tab
* Get the .unk file from the game .AFS files usually they are named like TXT-xx-x-xx-x.unk
* Drag and drop on the .exe executable
* The program will open a CMD window and a text will appear on the screen
* Translate the text and hit enter to see the next line
* Type 'exit' or 'quit' to exit and save the file
* The new file will appear on the folder 'TranslatedContent' in the same folder as the .exe executable
* Put the newly generated file inside the .ASF file
* Launch the game and test if its all right

## How to build from the source code
* Ensure that you have python3 installed
* Double-Click on the build.bat on the root folder
* Enjoy

## If you want to develop
If you want to further develop the code, here is an explanation of what i found when reverse engeneering the file, if you recognize any the binaries
and you are confident that they belong to a known extension, feel free to contact me.

The 'magic bytes' or the signature of the file is ```2C 01 00 00```


The file is composed of a header and a body, the header holds an array of all offsets where you can find the actual text
The body is an array containing texts in each index, the first byte of every text is an order mark byte ```FF FE```, and the offset where all
the order mark bytes are stored in the header.
What this code does is, read the header and find all the indexes, read the body and create an array of texts, the boundries of the texts
is set by the offset given from the header, then display the text to the user, take the input and saves it in the array.
When saving, the code will iterate over all bytes of the newly created body and find all occurences of the order mark byte ```FF FE``` and saves the
index where those bytes are, store in an array and in the end take the lenght of this array and apply as an offset on all elements of itself then saves it.

I know this code can be optimized and i forgot a lot of error handling things, so if you are willing to take your time to fix it, i will appreciate it.
