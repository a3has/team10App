

## Functional Requirements
1. *Visualize note connections (Visualization of the note pages with sub folders)
2. *Connect with any external API (google translate box )
3. *Advance search items with regular expressions or filters by categories (Abiltiiy to search for key words in the notes)
4. Edit User profiles (Ability to change user profile name, password, and picture)
5. Change note background color (Ability to change the color of the background)
6. Create note (Ability to create a new blank note)
7. Read Note (Ability to view previous notes written)
8. Update Note (Ability to update the notes )
9. Delete note (Ability to delete a note )
10. share note as text via email (Ability to share notes with others)
11. login account, alternate sequence is create account (Ability to create an account or log into an exsisting account)
12. support text formatting (Adding bold, italic, and underline)

## Non-functional Requirements
1. *Multilingual support (Support other languages)
2. Password Hashing for login Security (Storing passwords with hash for protection)

<using the syntax [](images/ui1.png) add images in a folder called images/ and place sketches of your webpages>

![image info](images/testimage.png)



## Use Cases 
Author: Sammy

1. Edit User Profile 
- **Pre-condition:** 
1) User must have exsisting account
2) User must be logged in 
- **Trigger:** 
1. Click Profile Icon
2. Click Edit USer Profile
- **Primary Sequence:**
1. User logs in with verified account
2. Navagate to User Profile
3. System will display the users information such as email username ect. 
4. Select field to edit
5. After editing user must save the changes
6. System checks to see if information is valid 
7. System updates the information
8. Get notification that the information has been update
- **Primary Postconditions:** 
Users profile has been updated
User can view their update profiels
- **Alternate Sequence:** 
1. User inputed invalid data
2. User must change to valid data
- **Alternate Sequence <optional>:** 
1. User able to cancel the request to edit profile
2. Return to old user profile information


## Use Cases 
Author: Sammy
1. Todo Checklist
- **Pre-condition:** 
1) USer must be logged in
- **Trigger:** 
1) User clicks Todo button
- **Primary Sequence:**
1. User logs in
2. User clicks on todo button
3. Creates an option to create a new task
4. Able to apply a checkmark when done
5. Able to delete a todo 
6. User can edit the name 
7. System can set remiders 
- **Primary Postconditions:** 
1) Check list is updated with newly created task 
2) User can choose to edit, delete, or mark as done
- **Alternate Sequence:** 
1. User can choose to do the task at antoher time


## Use Cases 
Author: Sammy
1. Advance search items with regular expressions or filters by categories
- **Pre-condition:** 
1) User must be logged in
2) System should have a database with searchable items
- **Trigger:** 
1) Click on search
2) Click on advance search
- **Primary Sequence:**
1. User access the search functionality
2. User sees advance seach button
3. Can type in expression to seacrh for
4. Can use filters from dropdown list
5. System will search the data bases for the information 
6. System displays the results of the search 
7. User can chaneg their search expression
- **Primary Postconditions:** 
1) User gets a lst of the search expression or the filtered content 
- **Alternate Sequence:** 
1. Invalid Search
2. Retype another expression
- **Alternate Sequence <optional>:**
1. Expression not found
2. Retype new expression

## Use Cases
Author: Nikko

1. *Visualize note connections (Visualization of the note pages with subfolders)
**Pre-condition:**
1)Users must have an existing account
**Trigger:**
1. User logs in
**Primary Sequence**
1. User logs in with a verified account
2. The system sends the user to the home page and displays the highest-level folder(s) within the system
3. The user selects right clicks folder and selects the visualize option
4. System displays a tree with all folders and all notes within them
- **Primary Postconditions:**
Users can view the note and open subsequent folders when selected from the tree
Users can manipulate the note and its subfolders by moving them around changing text, or deleting
- **Alternative Sequence:**
1. User fails to log in with a verified account
Prompt the user to try again 
- **Alternative Sequence:**
1. The user does not have any existing notes or folders in the system
The system prompts users that they do not have any notes and to create one now.


Author: Nikko

1. Create note (Ability to create new blank note)
**Pre-condition:**
1) The user must have an existing account
2) The user must be logged in
-**Trigger:**
1) The user selects to create a new note
-**Primary Sequence**
1. The user navigates to the folder they would like to put the note in
2. User clicks create a new note
3. The system prompts the user to write the name of the note in a text box
4. The user types the name of the note.
5. User clicks create
6. The system saves the information creates a note in the folder, and displays the note to the user.
-**Primary Postconditions:**
Users can manipulate the contents of the note such as adding or removing text or displaying images
Users can delete the note
Users can move the note
-Alternative Sequence
1. The user fails to write a title for the note
The system displays an error stating no title was given to the note and to give one before selecting create

## Use Cases
Author Nikko

1. Support text formatting (Adding bold, italic, and underlining)
- **Pre-condition:**
1. User must be logged in
2. The user must be in an existing note.
- **Trigger:**
1. The user selects one of the supported text-formatting options when typing in a textbox or highlighting selected text.
- **Primary Sequence:**
1. The user navigates to the folder where the note they want to edit is contained
2. The user selects the note that they want to edit.
3. The system opens the note and displays the contents to the user.
4. The user clicks on a textbox within the note
5. The system allows the user to type in the note and shows options to bold, italicize, or underline the text the user is inputting.

- **Primary Post-conditions:**
Users can select one of the options and it will change the upcoming text or highlighted text to be bolded, italicized, or underlined
Users can select one of these options if already selected to turn off the option for upcoming text or remove it on the highlighted text.

-**Alternative sequence:**
N/a

## Use Cases
Author: Nikko

1.*Multilingual support (Support other languages)
**Pre-condition:**
1. The user is on the website.
-**Trigger:**
1. The user selects a different language on a drop-down list of languages.
-**Primary Sequence:**
1. The user navigates to the website.
2. The user selects language on the top right corner of the screen.
3. The system displays a drop-down with different language options for the user to choose from.
4. The user selects a language that they prefer.
5. The system refreshes the page and converts all text to an alternative language.
-**Primary Post-conditions:**
Users can see all text displayed on the site in the selected language.
Users can undo the selection by navigating back to the dropdown in the top right and selecting a different language.

-**Alternative sequence:**
N/a



 


 

