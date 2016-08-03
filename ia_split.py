import xml.etree.ElementTree as ET      # To read the TOC and other xml files
import glob                             # To get lists of files from folders
from subprocess import call             # To tar and untar files
import shutil
import csv_to_mods

def move_file(orig,dest):
    """ orgi->(string) path of the file to move
        dest->(string) destination path (including filename)

        Wrapper for shutil move. Probably unnecessary"""

    shutil.move(orig,dest)

def rename_file(old,new):
    """old->(String) path to file (including filename duh)
       new->(String) path to new file (including new filename)
       
       This is just using the move command to rename the file."""

    shutil.move(old,new)

def untarball(tarfile, dest):
    """tarfile->(String) path to tarfile to be uncompressed
       dest->(String) folder path to uncompress tar into

       Uncompresses a tarfile of the .tar variety using the -xzf flag.
       The dest path will be created if it does not exist."""

    call(['mkdir','-p',dest])
    call(['tar','-xzf',tarfile,"-C",dest])

def get_tarname(path):
    """ Gets the name of the tarfile in the directory"""

    return glob.glob(path+"/*.tar")[0]

def get_scandata(path):
    """ Gets the name of the tarfile in the directory"""

    return glob.glob(path+"/*scandata.xml")[0]

def create_dest_folders(name,range_start,range_end,padding):
    """ Range_start inclusive, range_end exclusive
        padding is zero padding on the number
        ex. 001 is 3, 0001 is 4...etc

        returns the list of folders created
    """

    number_format = "%0"+str(padding)+"d"
    folders = []
    for a in range(range_start,range_end):
        call(['mkdir','-p',name+number_format%(a)])
        folders.append(name+number_format%(a))
    return folders

def create_mods_file(xmltree,folder):
    """ Generates a MODS.xml file in the specified folder from the given xmltree """

    tree = ET.ElementTree()
    if(type(xmltree) != type(tree)):
        tree._setroot(xmltree)
        tree.write(folder+"/MODS.xml")
    else:
        xmltree.write(folder+"/MODS.xml")

def make_folder_into_compound(folder,destination,modspath,scandata,toc,ext=".jp2"):
    """ Turn a folder containing ext type files
        folder -> files
        into
        folder->firstchild->OBJ.jp2,secondchild->OBJ.jp2
        according to the islandor compound batch tool
        """

    files = glob.glob(folder+"/*"+ext) # Get list of files of the specified type in the folder
    padding = len(str(len(files))) # This makes sure that they will be ordered

    leafNums = scandata_leafnums(scandata)
    
    identifiers = []
    with open(toc) as f:
        for line in f:
            identifiers.append(line.rstrip("\n"))

    for a in range(0,len(leafNums)):
        identifier = identifiers[a]
        folders = create_dest_folders(destination+"/"+identifier+"/",0,len(leafNums[a]),padding) # Create dest folders

        for b in range(0,len(folders)):
            move_file(files[leafNums[a][b]],folders[b]+"/OBJ.jp2") # Move and rename the files into their respective folder
            modfile = generate_mods(metapath,identifier,folders[b]+"/MODS.xml")
        copy_file(folders[0]+"/MODS.xml",destionation+"/"+identifier+"/MODS.xml")

def scandata_leafnums(scandata):
    """ Goes through a scandata file and make a nested list of leaf nums """

    leafnums = []
    tree = ET.parse(scandata)
    root = tree.getroot()
    tmp = []
    for item in root.iter('page'): 
        if(item.find("pageType").text == "Chapter"):
            if(len(tmp) != 0):
                leafnums.append(tmp)
            tmp = []
        if(item.find("pageType").text == "Chapter" or item.find("pageType").text == "Normal"):
            tmp.append(int(item.attrib['leafNum']))
    if(len(tmp) != 0):
        leafnums.append(tmp)
    return leafnums

def copy_file(start,finish):
    """ start->(string) start path of file
        finish->(string) finish path of file
        
        Wrapper for shutil copy"""

    shutil.copy(start,finish) 

def generate_mods(metapath,identifier,dest):

    files = glob.glob(metapath+"*.xml") # Get list of files in the directory given
    for f in files: # lets look at the all the files
        key = []
        reader = csv.reader(codecs.open(f,encoding="utf-8"))
        for row in reader:
            if len(key) == 0:
                key = row
            else:
                if(identifier in row):
                    csv_to_mods.csv_row_to_mods(row,key,dest)

def get_toc(path,boxid):
    
    toc = []
    with open(path+"/"+boxid+".txt") as f:
        for line in f:
            toc.append(line.rstrip("\n"))
    return toc


if __name__ == "__main__":
    
#    split_by_chapter("eightconceptsofb00gilb/eightconceptsofb00gilb_scandata.xml")
    
# untarball("testarchive/testarchive.tar","newarchive")
#    split_into_folders("testarchive/testarchive.tar","TOC.xml","newarchive")
#    move_file("testarchive/testfile.txt","newarchive")

#    create_dest_folders("/Users/armst179/workspace/internetarchive_scripts/bleh",0,11,0)

# make_folder_into_compound("newarchive")

#    new_folders("blergfolder/",['glergfolder'])

#    root = ET.Element("blerg")
#    create_mods_file(root,"newarchive")

#print(find_mods("MODS/",""))

    print scandata_leafnums("spiller_006-1-4-3-21_scandata.xml")

    pass
    
