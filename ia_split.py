import xml.etree.ElementTree as ET

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

if __name__ == "__main__":
    
    split_by_chapter("eightconceptsofb00gilb/eightconceptsofb00gilb_scandata.xml")



