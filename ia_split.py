import xml.etree.ElementTree as ET      # To read the TOC and other xml files
import glob                             # To get lists of files from folders
from subprocess import call             # To tar and untar files
import shutil

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

def split_into_folders(tarfile_name,toc,dest_folder="_tmp"):
    """Using the table of contents, split the tarfile into multiple folders
      
      tarfile -> STRING file name and path of the tarfile to be split into sub folders
      toc -> STRING file name and path of the TOC.xml file to use for splitting the tarfile
      tempfolder -> path of a temp folder ? not sure if this is staying TODO
       
       """


    files = glob.glob(dest_folder+"/*.jp2") # Get a list of the image files that have been uncompressed

    
    toc = ET.parse(xmlfile)                             # Open the TOC to  read for splitting
    for page in toc.find('pageData').findall('chapter'): # TODO get the right xml tags to loop over
        if('leafNum' in page.attrib and page.attrib['leafNum'] < count):
            # Up count of some sort? 
            pass # POP image into directory?

def create_mods_file(xmltree,folder):
    """ Generates a MODS.xml file in the specified folder from the given xmltree """

    tree = ET.ElementTree()
    if(type(xmltree) != type(tree)):
        tree._setroot(xmltree)
        tree.write(folder+"/MODS.xml")
    else:
        xmltree.write(folder+"/MODS.xml")

def make_folder_into_compound(folder,destination,modspath,scandata,ext=".jp2"):
    """ Turn a folder containing ext type files
        folder -> files
        into
        folder->firstchild->OBJ.jp2,secondchild->OBJ.jp2
        according to the islandor compound batch tool
        """

    files = glob.glob(folder+"/*"+ext) # Get list of files of the specified type in the folder
    padding = len(str(len(files))) # This makes sure that they will be ordered

    identifier_leafNums = scandata_leafnums(scandata)
    leafNums = []
    for a in range(0,identifier_leafNums.keys()):
        leafNums.append(int(identifier_leafNums[identifier_leafNums.keys()[a]]))
    leafNums += [len(files)]
    menuSizes = []
    for a in range(0,len(leafNums)-1):
        menuSize.append(leafNums[a+1]-leafNums[a])
    leafCount = 0
    for a in range(0,identifier_leafNums.keys()):
        leafCount += 1
        identifier = identifier_leafNums.keys()[a]
        folders = create_dest_folders(destination+"/"+identifier+"/compound_",0,menuSize[a],padding) # Create dest folders
        for a in range(0,len(folders)):
            move_file(files[leafCount],folders[a]+"/OBJ.jp2") # Move and rename the files into their respective folder
            modfile = find_mods(modspath,identifier)
            copy_file(modfile,folders[leafCount]+"/MODS.xml")
    # TODO MOD file?

def scandata_leafnums(scandata)
    """ Goes through a scandata file and makes a dict for identifiers and leafnum index"""

    leafnums = {}
    tree = ET.parse(scandata)
    root = tree.getroot()
    for item in root: # TODO update structure
        leafnums[item.find('title').text] = int(item.attrib['leafNum']) # TODO update structure
    return leafnums

def new_folders(parent_path, folder_names):
    """Makes directories with names in folder_names (list), inside of parent_path path"""


    if(parent_path[-2:-1] != "/"):
        parent_path += "/"
    for folder in folder_names:
        call(['mkdir','-p',parent_path + folder]) # Makes the full path if it doesn't exist (yes this includes the parent)

def copy_file(start,finish):
    """ start->(string) start path of file
        finish->(string) finish path of file
        
        Wrapper for shutil copy"""

   shutil.copy(start,finish) 

def get_scan_identifier(scandata,leafnum):
    """ TODO: return the identifier for the given leaf number """

    tree = ET.parse(scandata)
    root = tree.getroot()
    for item in root:
        if(item.find("leafNum")):
            return item.identifier
    # TODO Restructure as needed


def find_mods(mods_dir,identifier):
    """ Look for a mods file in the mods_dir of a given identifier. 
        Returns a path to the MODS files"""

    files = glob.glob(mods_dir+"*.xml") # Get list of files in the directory given
    for f in files: # lets look at the all the files
        tree = ET.parse(f) # Open the file as an xml tree, lets make like a treet and....split :D
        root = tree.getroot()
        for child in root:
            if 'identifier' in child.tag and child.text == identifier: # TODO Test with actual files
                 return f # correct file found, return the path
        

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

    pass
    
