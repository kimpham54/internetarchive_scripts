import xml.etree.ElementTree as ET      # To read the TOC and other xml files
import glob                             # To get lists of files from folders
from subprocess import call             # To tar and untar files
import shutil

def split_by_chapter(xmlfile):
    """ Split the xml file by an identifier into multiple xml files
        """

    chapters = []                                                       # Final Split data
    tree = ET.parse(xmlfile)                                            # Open XML Tree to be Parsed
    tmp_book = []                                                       # Temp book to hold for splitting
    for page in tree.find('pageData').findall('page'):                  # Find all the page elements TODO fix structuring?
        if int(page.attrib['leafNum'])%5==0 and len(tmp_book) != 0:     # TODO For testing, this just splits into 5 page books
            chapters.append(create_new_book_xml(tmp_book))              # Write into a new book and save to the chapters list
            tmp_book = []                                               # Clear temp book 
        tmp_book.append(page)                                           # Save page
    return chapters                                                     # Return list of split chapters (still as xml elements)

def create_new_book_xml(subtrees):
    """ElemenTree -> array of subtree to append under the root of book
       returns the root element of the new tree

       """
        # TODO
        # Check the structure that is supposed to be used for the xml files
        # Do we want to save directly to a file or just return the tree?


    root = ET.Element('book')       # Create new book xml tree
    for ob in subtrees:             # Iterate over list
        root.append(ob)             # Add page

    return root                     # Return new book

def move_file(orig,dest):
    """ The dest folder does include the filename, as does orig"""

    shutil.move(orig,dest)

def rename_file(old,new):
    """ Rename a file"""

    shutil.move(old,new)

def untarball(tarfile, dest):
    """Untar a file
       creates path to dest if it doesn't exist"""
    call(['mkdir','-p',dest])
    call(['tar','-xzf',tarfile,"-C",dest])

def get_tarname(path):
    """ Gets the name of the tarfile in the directory"""

    return glob.glob(path+"/*.tar")[0]

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

def make_folder_into_compound(folder,destination,ext=".jp2"):
    """ Turn a folder containing ext type files
        folder -> files
        into
        folder->firstchild->OBJ.jp2,secondchild->OBJ.jp2
        according to the islandor compound batch tool
        """

    files = glob.glob(folder+"/*"+ext) # Get list of files of the specified type in the folder
    padding = len(str(len(files))) # This makes sure that they will be ordered
    folders = create_dest_folders(destination+"/compound_",0,len(files),padding) # Create dest folders
    for a in range(0,len(files)):
        move_file(files[a],folders[a]+"/OBJ.jp2") # Move and rename the files into their respective folder
        # GET META DATA
        # TODO Create MOD file here
    # Create the overall MOD file?

def new_folders(parent_path, folder_names):
    """Makes directories with names in folder_names (list), inside of parent_path path"""


    if(parent_path[-2:-1] != "/"):
        parent_path += "/"
    for folder in folder_names:
        call(['mkdir','-p',parent_path + folder]) # Makes the full path if it doesn't exist (yes this includes the parent)

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
    pass
    
