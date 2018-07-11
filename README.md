# directory
A pythonic remake of the infamous directory.bethel.edu

## Planning Notes:

#### Search Types:
 - #### First/Last name
  - Normal first and last name search for students
 - #### Username
 - #### E-Mail
 - #### Department
  - Staff and faculty within a department
 - #### ID
  - Used primarily by admin as students cannot see other students IDs
 - #### Phone number

#### Searching For (input):
All inputs that may be entered into whichever solution are as follows:
- Name {First, and/or last}
- Username (ex. grg27487)
- User ID
- Department Name (ex. Department of Math and Computer Science)

#### Return from Search:
Two types of return, based on general role:
- Student:
    - Name
    - Email
    - PO #
    - User ID
    - Address
    - Major/Minor/Program/Year
    - Location/Room
    - Image URL
- Faculty/Staff:
    - Name
    - Email
    - PO # (if applicable)
    - User ID
    - Address
    - Department
    - Job Title
    - Ext. #
