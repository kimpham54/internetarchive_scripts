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

def move_file(orig,destfolder):
    """ The dest folder doesn't include the filename, while orig does"""

    shutil.move(orig,destfolder+"/"+orig.split("/")[-1])

def untarball(tarfile, dest):
    """Untar a file
       creates path to dest if it doesn't exist"""
    call(['mkdir','-p',dest])
    call(['tar','-xzf',tarfile,"-C",dest])

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

def split_into_folders(tarfile_name,toc,tempfolder="_tmp"):
    """Untar the tarball file and using the table of contents, split the tarfile into multiple folders
      
      tarfile -> STRING file name and path of the tarfile to be split into sub folders
      toc -> STRING file name and path of the TOC.xml file to use for splitting the tarfile
      tempfolder -> path of a temp folder ?
       
       """

    untarball(tarfile_name,tempfolder) # Untar the image files

    files = glob.glob(tempfolder+"/*.jp2") # Get a list of the image files that have been uncompressed


    
    toc = ET.parse(xmlfile)                             # Open the TOC to  read for splitting
    for page in toc.find('pageData').findall('chapter'): # TODO get the right xml tags to loop over
        if('leafNum' in page.attrib and page.attrib['leafNum'] < count):
            # Up count of some sort? 
            pass # POP image into directory?


if __name__ == "__main__":
    
#    split_by_chapter("eightconceptsofb00gilb/eightconceptsofb00gilb_scandata.xml")
    
# untarball("testarchive/testarchive.tar","newarchive")
#    split_into_folders("testarchive/testarchive.tar","TOC.xml","newarchive")
#    move_file("testarchive/testfile.txt","newarchive")

#    create_dest_folders("bleh",0,11,0)



    pass
