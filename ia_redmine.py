from redmine import Redmine

def create_redmine_issue(username,password,redmine_url,project_id,issue_subject,issue_description,assign_to):
    """Create and save a new issue on redmine
        username ->(String) authentication info for redmine
        password ->(String) authentication info for redmine
        project_id ->(String) name of project
        issue_subject ->(String) issue subject
        issue_description ->(String) description of issue
        assign_to ->(String) id of the person the task is assigned to"""

    redmine = Redmine(redmine_url,username=username,password=password)
    redmine.issue.create(project_id=project_id,subject=issue_subject,description=issue_subject,assigned_to_id=assign_to)


if __name__ == "__main__":

# Password and username input is for testing, I didn't want to leave my password up on github
# Ideally when this is deployed, an external library will be imported with the settings.

    username = input("username:") # Redmine user info
    password = input("password:")
    redmine_url = "https://digitalscholarship.utsc.utoronto.ca/redmine" # Location of redmine 

    redmine = Redmine(redmine_url,username=username,password=password) # connect to redmine
    redmine.auth()
    test_proj = redmine.project.get('test-project-kim3')

#    print(test_proj)

    create_redmine_issue(username,password,redmine_url,'test-project-kim2',"TEST SUBJECT", "TEST DESCRIPTION")

    projects = redmine.project.all()
    for proj in projects:
        print(proj.name)
        print(proj.identifier)

