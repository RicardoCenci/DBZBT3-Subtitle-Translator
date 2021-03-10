import os
def saveFile(outputToSave):
    clear()
    print('Saving...')
    outputFile = open('OUTPUT-'+FileInfo['FileName'], "wb")
    outputFile.write(outputToSave)
    outputFile.close()
    clear()
    print('Done')

def processFile():
    # Processing the file to Save it correctly
    newFileBytes = bytearray(FileInfo['HeaderRaw']) #Still using the old header
    # TODO
    # create a custom header based on the content

    for data in FileInfo['DataIndexes']:
        #Iterate over all the indexes checking if there is a translated text to be added to the new file.
        if 'TranslatedText' in data: 
            newFileBytes += b'\xFF\xFE'+data['TranslatedText']
        else:
            newFileBytes += b'\xFF\xFE'+data['byteText']

    saveFile(newFileBytes) # This actually create and save the contents to a file
    quit()

def SaveTranslatedText(text,position):
    text = TextToBytes(text)
    oldTextLenght = len(FileInfo['DataIndexes'][position]['byteText'])
    newTextLenght = len(text)
    while oldTextLenght > newTextLenght:
        text.append(0)
        newTextLenght = len(text)
    FileInfo['DataIndexes'][position]['TranslatedText'] = text
    return



def BytesToText(bytesStr):
    string = []
    for byte in bytesStr:
        if byte == 0:
            continue

        char = chr(byte)
        string.append(char)
    return ''.join(string)

def TextToBytes(string):
    bytesArr = []
    for char in string:
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


clear = lambda: os.system('cls') #Windows Clear Funcion
File = open('TXT-US-B-00-0.unk' , 'rb')
ByteFileContent = File.read() #Read the File Contents

splittedBytesArray = ByteFileContent.split(b'\xFF\xFE') # FF FE is a order mark byte, to set the boundaries of the string

#this will store all the info that we recovered from the file
FileInfo = {
    'FileName' : File.name,
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
    print(BytesToText(Line['byteText']))
    userInput = input()
    if userInput == 'quit' or userInput == 'exit':
        break
    
    SaveTranslatedText(userInput,i)
    i = i + 1

processFile()