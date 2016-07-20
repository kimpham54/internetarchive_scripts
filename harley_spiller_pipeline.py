# Purpose of this file is to link all of the Internet Archive 
# files together into a pipeline to process the Harley-Spiller 
# collection.
#
#

import ia_getitems, ia_split, ia_redmine, ia_settings

# **************************

# **************************

downloaded_path = "harley_spiller_downloaded/"
preprocess_path = "harley_spiller_preprocess/"
processed_path = "harley_spiller_processed/"

# **************************
# CHECK FOR NEW COLLECTIONS
# **************************

collection_id = 'booksgrouptest' # The collection to watch
collections_db = 'harley_spiller_collections.txt' # The text file containing the subcollection (scan boxs, books?) that have already been processed

new_collections = ia_getitems.check_for_new_items(ia_settings.ia_username,ia_settings.ia_password,collection_id,collections_db)

if (len(new_colllections) == 0):
    # No new collections to process!
    return

ia_split.new_folders(downloaded_path,new_collections) # Prep folders for the download data

# **************************
# DOWNLOAD COLLECTION
# **************************

dry_run=False

for col in new_collections:
    ia_getitems.download_collection(ia_settings.ia_username,ia_settings.ia_password,col,download_path,dry_run) # Download new collections

# **************************
# UNTAR the jp2 archive
# **************************

tocfile = "_scandata.xml" # TODO This probably isn't right

ia_split.new_folders(preprocess_path,new_collections) # New folders to uncompress into

for col in new_collections:
    ia_split.untarball(download_path+"/"+col,preprocess_path + col)
    ia_split.move_file(download_path+"/"+col+"/"+col+tocfile,preprocess_path+"/"+col+"/"+col+tocfile)

# **************************
# Split the archive into multiple folders and move the jp2 files
# Also generate the MODS files
# **************************

ia_split.new_folders(processed_path,new_collections) # New folders to uncompress into
for col in new_collections:
    ia_split.make_folder_into_compound(preprocess_path,processed_path) # TODO THERE IS MODS STUFF TO DO HERE

# **************************
# Islandora stuff?
# **************************

# **************************
# Open redmine ticket
# **************************

redmine_url = "https://digitalscholarship.utsc.utoronto.ca/redmine/"
#project_id = "digital-collections-working-group"
project_id = "kim-pham"
issue_subject = "Harley-Spiller Collection new items"
assign_to = "cadenarmstrong"
print(new_collections)
issue_description = "The following items are new and have been processed:\n"
for col in new_collections:
    issue_description += col + "\n"
ia_redmine.create_redmine_issue(ia_settings.redmine_username,ia_settings.redmine_password,redmine_url,project_id,issue_subject,issue_description)

# **************************
# SAVE COLLECTIONS TO DATABASE
# **************************

ia_getitems.add_item_to_db(collections_db,new_collections)


