# This script reads a .unk file that contains subtitles, translates it and save, creating the headers and everything to be as close to the original
# file as possible. This is meant to be used to translate Dragon Ball Z: Budokai Tenkaichi 3, the game stores the subtitles in .unk files, there is a possibility that this .unk is a know 
# extension type for subtitles, but in my reseach i didnt find any clue of what type of ext this file is.
# So i created this script to read and help to translate the .unk files
# In my reverse engineering reseach on the file i found out some things:
# Aparently the text content is saved between bytes FF FE (order mark bytes) and the header stores the offset or index in which the FF FE bytes are
# so what this script does is, read the header, look into the content based on the header, edits it and create a new header with the offsets of the new
# content and saves it.
# Created by: Ricardo Cenci Fabris
# Last update 11/03/2021
import os
import sys
import codecs

def saveFile(outputToSave):
    clear()
    print('Saving...')
    currentPath = sys.path[0]
    if not os.path.isdir(currentPath+'/TranslatedContent'):
        try:
            os.mkdir(currentPath+'/TranslatedContent')
        except OSError:
            print ("Creation of the directory %s failed" % currentPath)
            pause()
    try:
        outputFile = open(currentPath+'/TranslatedContent/'+FileInfo['FileName'], "wb+")       
        outputFile.write(outputToSave)
        outputFile.close()
    except Exception:
        print('Failed to save content')
    clear()
    print('Saved on:'+currentPath+'TranslatedContent/'+FileInfo['FileName'])
    print('Done')
    pause()

def processFile():
    # Process the file into
    newFileBytes = bytearray()
    for data in FileInfo['DataIndexes']:
        #Iterate over all the indexes checking if there is a translated text to be added to the new file.
        if 'TranslatedText' in data: 
            newFileBytes += b'\xFF\xFE'+data['TranslatedText']
        else:
            if len(data['byteText']) % 2 != 0:
                data['byteText'] += b'\x00'
            newFileBytes += b'\xFF\xFE'+data['byteText']
    newHeader = createHeader(newFileBytes)
    newFile = newHeader + newFileBytes
    saveFile(newFile) # This actually create and save the contents to a file
    quit()

def SaveTranslatedText(text,position):
    text = TextToBytes(text)
    print(text)
    oldTextLenght = len(FileInfo['DataIndexes'][position]['byteText'])
    newTextLenght = len(text)
    while oldTextLenght >= newTextLenght:
        #Just to minimize the chances of breaking the file, this ensures that the new text is the same lenght as the untranslated one
        text.append(0)
        newTextLenght = len(text)
    
    if len(text) % 2 != 0:
        #this is to prevent the text lenght to be an odd value and breaking the header creation process
        text.append(0)
    FileInfo['DataIndexes'][position]['TranslatedText'] = text
    return


##Utility Functions
def BytesToText(bytesStr):
    string = []
    for byte in bytesStr:
        if byte == 0:
            continue

        char = chr(byte)
        if char == 96:
            char = 10
        string.append(char)
    return ''.join(string)

def TextToBytes(string):
    bytesArr = []
    for char in string:
        if char == '\\':
            char = '\n'
        bytesArr.append(ord(char))
        bytesArr.append(0)
    return bytearray(bytesArr)

def HeaderReader(Header):
    headerInfo = [] #Temp buffer to store the indexes
    # Reads a 4 bytes chunk of the file and transforms them into intNumber
    i = 4
    for a in Header: 
        byteSequence = Header[i:i+4] #Gets the 4 bytes chunk
        intNumber = int.from_bytes(byteSequence, byteorder='little', signed=False) #Transform it as a number
        if intNumber == 0:
            #Since we are expecting an index from this number, is safe to say that the number cant be 0
            break
        i = i + 4
        headerInfo.append(intNumber)

    i = 0
    for index in headerInfo:
        #Get the corresponding Text value from ByteFileContent based on the previous array of indexes that we recovered
        DataIndexInfo = {
            'start' : index + 2,
            'byteText':  None
        }

        #This probably is a bad way to do this
        #To get full string from ByteFileContent, this takes all bytes counting on the start of this index to the end of the next index
        #So, if this hits the last index, it cant recover any more text, becouse the next index is out of range
        #So i simply do this and if i get a out of range exeption i get all bytes from the start of the index to the finish of the list
        try:
            DataIndexInfo['byteText'] = ByteFileContent[DataIndexInfo['start'] : headerInfo[i+1] -1]
        except IndexError:
            DataIndexInfo['byteText'] = ByteFileContent[DataIndexInfo['start'] : len(ByteFileContent) - 1]

        FileInfo['DataIndexes'].append(DataIndexInfo)
        i = i + 1

def createHeader(content):
    #Creates the header based on the content
    IterableArrOfBytes = [content[i:i+1] for i in range(len(content))] #Transforms the content into a iteratable array of bytes
    newIndex = []
    i = 0
    for byte1, byte2 in zip(*[iter(IterableArrOfBytes)]*2):
        if byte1 == b'\xff' and byte2 == b'\xfe':
            newIndex.append(i) #stores the Index of the individual texts based on de FF FE byte (order mark byte)
        i = i + 2
    
    offset = (len(newIndex) + 3) * 4 #Here im calculating the offset, accounting with the lenght of the header, +3 because there is 3 more indexes that serve as padding on the file.
    newIndexWithOffset = []
    for i in range(len(newIndex)):
        offsetedNumber = newIndex[i] + offset
        byteNumber = (offsetedNumber).to_bytes(4, byteorder='little')
        newIndexWithOffset.append(byteNumber)

    newIndexWithOffset += [b'\x00\x00\x00\x00'] * 2
    newIndexWithOffset.insert(0, FileInfo['FirstBytes'])
    return b''.join(newIndexWithOffset)

pause = lambda: os.system('pause') #Windows Console Pause Command
clear = lambda: os.system('cls') #Windows Console Clear Command

try:
    FilePath = sys.argv[1]
    # FilePath = 'TXT-US-B-01-0.unk' #test
except IndexError:
    print('No File Especified') 
    pause()
    quit()

try:
    File = open(FilePath , 'rb')
    ByteFileContent = File.read() #Read the File Contents
except IOError:
    print("File not accessible or invalid path")
    pause()
    quit()

splittedBytesArray = ByteFileContent.split(b'\xFF\xFE') # FF FE is a order mark byte, to set the boundaries of the string

#this will store all the info that we recovered from the file
FileInfo = {
    'FileName' : os.path.basename(File.name),
    'FirstBytes' : splittedBytesArray[0][0:4],
    'HeaderRaw' : splittedBytesArray[0], #Since the header have the index information of the file, we store it to read it later
    'DataIndexes' : []
}
File.close()
HeaderReader(FileInfo['HeaderRaw'])

#Above here is all the logic to actually get the user input and save in this structure
KeepRunning = True
i = 0
for Line in FileInfo['DataIndexes']:
    clear()
    Text = BytesToText(Line['byteText'])
    if Text == '':
        break
    print(Text)
    userInput = input()
    if userInput == 'quit' or userInput == 'exit':
        break
    
    SaveTranslatedText(userInput,i)
    i = i + 1

processFile()