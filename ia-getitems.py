
# This is how we get items from the Internet Archive
# https://archive.org/details/turkishhistoryfr01knol

from internetarchive import get_item, download, search_items,configure

def download_new_items(username,password,collection,md5_table, destination, dry_run=False):
    """ username->(String) internet archive user login
        password->(String)
        collection->(String) IA collection identifier
        md5_table->(String) filename of file containing downloaded files md5 hashes
        destination->(String) folder location to download collection to

        Checks the collection for new files based off a local file containing md5 hashes.
        Each hash in the md5_table file should be on its own line.
        """
    configure(username,password) # Configure log in for IA
    downloaded_files = [] # Make collection of existing files
    with open(md5_table) as f:
        for line in f:
            downloaded_files.append(line.rstrip("\n")) # remove new line character

    ia_collection = get_item(collection) # Get collection to be watched
    for book in ia_collection.contents(): # Cycle through 'books' (Collections in the collection)
        download_book = False # Does the collection contain new files
        for f in book.files:
            if('md5' in f):
                if not(f['md5'] in downloaded_files): #  Check for hash in existing table
                    download_book = True
                    with open(md5_table, "a") as md5_f: # add new hash to table
                        md5_f.write(f['md5'] + "\n")                
            else: # The files do not contain a hash, so they cant be tracked and must be downloaded each time (?)
                 download_book = True
        if download_book:
            download(book.identifier, destdir=destination, dry_run=dry_run) # Dry run for testing purposes


if __name__ == "__main__":

    collection = 'booksgrouptest'
    username = input("Username(email):")
    password = input("Password:")
    md5_table = "test_md5.txt"
    dest="."

    print("Running dry run of download_new_items on %s"%(collection))
    download_new_items(username,password,collection,md5_table, dest,dry_run=True)

    #book = 'menusfromvarious00unse'

    #item = get_item(book) # Gets book of this name

#print(item.item_metadata.keys())
#
## check type of variable
#print(type(item.files) is list)
##True
#print(type(item.files) is dict)
##False
##
### list all files in an object
#for k in item.files:
#    print(k)
#
## download a collection
#
#dest = "."

#item.download(checksum=True, destdir=dest)

# download an item
# script to scan compare checksum and pull items that are new
