import os
import sys
import cv2
import zipfile
from shutil import rmtree

def get_files(zipname: str, extraction_folder=".") -> str:
    assert zipname.endswith(".zip")
    with zipfile.ZipFile(zipname, "r") as zip:
        foldername = f"{zipname[:-4]}"
        print(f"name for {zipname}: {foldername}")
        zip.extractall(os.path.join(extraction_folder, foldername))
    return foldername

def get_bootanimation_path(foldername) -> str|None:
    for root, dirs, files in os.walk(foldername):
        for f in files:
            if f == "bootanimation.zip":
                return os.path.abspath(os.path.join(root, f))
            
def get_bootanimation_frames(bootanimation_folder):
    frames = []
    for file in os.listdir(bootanimation_folder):
        file = os.path.join(bootanimation_folder, file)
        if os.path.isdir(file):
            for img in os.listdir(file):
                arrayimg = cv2.imread(os.path.join(bootanimation_folder, file, img))
                #height, width, channels = arrayimg.shape
                arrayimg = cv2.resize(arrayimg, (225, 400))
                frames.append(arrayimg)
    return frames

def main(zip_file=None) -> None:
    if zip_file is None:
        zip_files = [ x for x in os.listdir() if x.endswith(".zip") ]
        print("Choose zip file:")
        for index, zip_file in enumerate(zip_files):
            print(f"{index}. {zip_file}")
        choice = int(input(">> "))
        foldername = get_files(zip_files[choice])
    else:
        foldername = get_files(zip_file)

    bootanimation_path = get_bootanimation_path(foldername)
    if bootanimation_path:
        print(f"Bootanimation path: {bootanimation_path}")
        bootanimation_folder_path = get_files(bootanimation_path)

        print(f"Bootanimation folder path: {bootanimation_folder_path}")
        frames = get_bootanimation_frames(bootanimation_folder_path)
        for frame in frames:
            cv2.imshow("Bootanimation", frame)
            cv2.setWindowProperty("Bootanimation", cv2.WND_PROP_TOPMOST, 1)
            cv2.waitKey(10)
    print("Removing tmp files")
    rmtree(foldername)
    print("Done")
  
if __name__ == "__main__":
    if len(sys.argv) == 2:
        zip_name = sys.argv[1]
    else:
        zip_name = None
    main(zip_name)
