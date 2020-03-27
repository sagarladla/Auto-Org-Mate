import subprocess
import shutil
import os

# Populate list with absolute path of files
files=[]
for root,dirs,filenames in os.walk('C:/Users/sagar/Music'):
    if not dirs:
        for filename in filenames:
            file='{}/{}'.format(root,filename)
            files.append(file)

exe='exiftool.exe'

for input_file in files:

    # Subprocess in bash / cmd
    process=subprocess.Popen([exe,input_file],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=True)
    
    # Extract metadata of a file
    metadata={}
    for output in process.stdout:
        meta=output.strip().split(":")
        metadata[meta[0].strip()]=meta[1].strip()

    foldername=None
    if metadata['File Type'] == 'MP3':
        # Assign file to a folder
        if metadata['Album'] == '':
            foldername=metadata["Artist"]
        else:
            foldername=metadata['Album']
        # Create folder
        if not os.path.exists(foldername):
            os.makedirs(foldername)
        # Move a file to folder
        if os.path.exists(foldername):
            shutil.move(input_file,foldername)