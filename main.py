import subprocess
import argparse
import shutil
import os

def main():
    # win_dir="\\"
    args=parse()
    files = populate_files(args.src)
    folder_dict = assign_folder(files, args.file_type)
    for folder, files in folder_dict.items():
        new_folder="{}\{}".format(args.dst,folder)
        # Create folder
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)
        # Move a file to folder
        elif os.path.exists(new_folder):
            for infile in files:
                shutil.move(infile,new_folder)
            

def parse():
    use="python autorgmate.py --src 'SOURCE_FOLDER' --dst 'DESTINATION_FOLDER' --file 'MP3'"
    parser = argparse.ArgumentParser(prog=__file__, description="Tool to organize data in matter of secs.", usage=use)
    parser.add_argument('--src', help="Source path of disorganized data", action="store", dest="src", type=str)
    parser.add_argument('--dst', help="Destination path of disorganized data", action="store", dest="dst", type=str)
    parser.add_argument('--file', help="File type of data to deal with. Add one at a time", action="store", dest="file_type", type=str)
    return parser.parse_args()

# Populate list with absolute path of files
def populate_files(src):
    files=[]
    for root,dirs,filenames in os.walk(src):
        if not dirs:
            for filename in filenames:
                file='{}\\{}'.format(root,filename)
                files.append(file)
    return files

# Assign folder name to files
def assign_folder(files, file_type):
    exe='exiftool.exe'
    folder_dict = dict()
    for input_file in files:
        
        # Subprocess in bash / cmd
        process=subprocess.Popen([exe,input_file],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=True)
    
        # Extract metadata of a file
        metadata={}
        for output in process.stdout:
            meta=output.strip().split(":")
            metadata[meta[0].strip()]=meta[1].strip()
        
        if file_type.upper() == 'MP3':
            if metadata['File Type'] == file_type.upper():
                # Assign file to a folder
                if metadata['Album'] == '':
                    if metadata['Artist'] not in folder_dict.keys():
                        folder_dict[metadata["Artist"]]=list()
                    folder_dict[metadata["Artist"]].append(input_file)
                else:
                    if metadata['Album'] not in folder_dict.keys():
                        folder_dict[metadata["Album"]]=list()
                    folder_dict[metadata['Album']].append(input_file)
            else:
                continue
    return folder_dict

if __name__ == "__main__":
    main()