import os
import re
import zipfile
import shutil

def createMETS(pathZip):
    # # Create temporary directory
    tempDir = pathZip.split(".zip")[0]
    if not os.path.exists(tempDir):
        os.mkdir(tempDir)

    # Unpack zip into the temp dir
    with zipfile.ZipFile(pathZip, mode="r") as archive:
        files = archive.namelist()
    
    print(files)

    # Create list of dicts images and xmls pairs
    fileList = []
    imageList =[]
    xmlList = []
    
    for name in files:
        print(name)
        if re.search(r"\.xml", name):
            xmlList.append(name.split(".xml")[0])
        if re.search(r"\.png", name):
            imageList.append(name.split(".png")[0])
    for xml in xmlList:
        print(xml)
        if xml not in imageList:
            print("Image not found for:" + xml)
            print("Do you wish to continue? y or n")
            ans = input()
            if ans == "n":
                exit()
        else:            
            fileList.append({"xml": xml + ".xml", "image": xml +".png"})
            
    
    # Loop through the dictionary and built the METS XML
    fileSeqListImage = ['<mets:fileGrp USE="binarized">']
    fileSeqListXml = ['<mets:fileGrp>']
    fileStrucList = ['<mets:structMap TYPE="physical">', '<mets:div TYPE="book">']

    for idx, file in enumerate(fileList):
        imageId = "binarized" + str(idx)
        xmlId = "transcript" + str(idx)
        
        seqImage = '<mets:file ID="{}"><mets:FLocat xlink:href="{}"/></mets:file>'.format(imageId, file["image"])
        fileSeqListImage.append(seqImage)
        
        seqXml = '<mets:file ID="{}"><mets:FLocat xlink:href="{}"/></mets:file>'.format(xmlId, file["xml"])
        fileSeqListXml.append(seqXml)

        strucItems = ['<mets:div TYPE="page">', '<mets:fptr FILEID="{}"/>'.format(imageId), '<mets:fptr FILEID="{}"/>'.format(xmlId), '</mets:div>']
        fileStrucList.extend(strucItems)
    
    fileSeqListImage.append('</mets:fileGrp>')
    fileSeqListXml.append('</mets:fileGrp>')
    fileSeq = ['<mets:fileSec>'] + fileSeqListImage + fileSeqListXml + ['</mets:fileSec>']

    fileStrucList.extend(['</mets:div>', '</mets:structMap>'])

    finalXml = ['<mets:mets xmlns:mets="http://www.loc.gov/METS/" xmlns:xlink="http://www.w3.org/1999/xlink">'] + fileSeq + fileStrucList + ['</mets:mets>']
    finalXml = "\n".join(finalXml)

    # Write out the final xml to existing zip
    metsOut = os.path.join(tempDir, "mets_manifest.xml")
    with open(metsOut, "w") as f:
        f.write(finalXml)
    os.chdir(tempDir)
    with zipfile.ZipFile(pathZip, mode="a") as archive:
        archive.write("mets_manifest.xml")
        # with archive.open("mets_manifest.xml", "w") as f:
        #     f.write(finalXml)

    # Clean up temp
    os.chdir("../..")
    shutil.rmtree(tempDir)

pathToZip = "C:/Users/mathe/Documents/Github-repos/ocr-utilities/simple_archive_prefixed.zip"
createMETS(pathToZip)