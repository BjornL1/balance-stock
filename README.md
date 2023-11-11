# STOCK BALANCE TESTER 

This site provides a tool which supports maintaining the number of items in a warehouse at a level which balances the available space and still prevents potential shortages.

![landing page](readme_images/landingpage_.png)

Link to the site:
[STOCK BALANCE TESTER](https://bjornl1.github.io/bankloan-calculator/)

## CONTENTS

- [STOCK BALANCE TESTER](#bank-loan-payoff-calculator)
  - [CONTENTS](#contents)
  - [User Experience (UX)](#user-experience-ux)
    - [User Stories](#user-stories)
  - [Design](#design)
    - 
  - [Features](#features)
    - [Future Implementations](#future-implementations)
    - [Accessibility](#accessibility)
  - [Technologies Used](#technologies-used)
    - [Languages Used](#languages-used)
    - [Frameworks, Libraries \& Programs Used](#frameworks-libraries--programs-used)
  - [Deployment \& Local Development](#deployment--local-development)
    - [Deployment](#deployment)
    - [Local Development](#local-development)
      - [How to Fork](#how-to-fork)
      - [How to Clone](#how-to-clone)
  - [Testing](#testing)
    - [Testing User Stories from (UX) Section](#testing-user-stories-from-ux-section)
      - [Validator Testing](#validator-testing)
      - [Further Testing](#further-testing)
  - [Credits](#credits)
    - [Code Used](#code-used)
    - [Content](#content)
    - [Acknowledgments](#acknowledgments)

---

## User Experience (UX)

- __Initiation of concept__
Keeping track of the available storage space capacity in a warehouse and avoiding items occupying shelves and still keeping items to support demand can be a complex task. By providing a tool that allows users to set the minimum and maximum quantities for specific items, the user will be notified of any risk of exceeding these boundaries. This function enables the warehouse owner to order correct quantities at the right time.

  
- __Key goals for the site__

  - To offer a service which monitors high- and low volume items.
  - To offer a possibility to optimize stock balance by user input.
  - To check how the input changes with updated quantities added by the user.


### User Stories

- __First time user:__
    I am:
  - Learning about the main purpose of the site.
  - Understanding how the site could support planning of production or sales.


- __Returning User:__
    I am:  
  - Actively trying to add various level of critical levels to check the impact
  - Trying to a longer range of values to investigate how average of stock can be calculated 
    for various items.

## Design
This project is a command line based program with a user prepared input window run through heroku, no exclusive design besides the interface provided by heroku are added.

### Flowchart
The image below illustrates the basic flowchart structure for the project.

![](readme_images/flowchart.png)

## Features
   
   The result of the code is written to a gspread sheet which contains five different tabs further described below
 - Stock 
   - These values are written one time period (day, week, month) before other the other sheets, which represents the stock quantity to be available before the next consumption of the items. Initially the gspread sheet will be populated with '0' for each item, however the user can update to another value to be used as the base before calculating next stock. The purpose with stock data is to display what stock level or quantity to prepare for the next production run, sales or similar. The stock values are calculated by multiplying the user's chosen "critical level" with the average sales from previous weeks, hence the first sales averages will be the same as the entered values. By using a critical level, the target is to optimize and handle temporary fluctuations e.g. avoiding to order more than necessary both for financial or physical space reasons after temporary peak in sales (which could be the case if the calculation for next stock was simply based on the previous sale). A similar purpose is also valid for the opposite scenario where the suggested stock level can prevent the risk of delaying deliveries due to shortage. 
      
 - Critical level
   - The "critical level" is a value that the user can choose to use as a way to control the minimum share quantities (based on sales) to be available before the next order of them. In the delivered code the value is integers between 1 to 50 representing 1 to 50 % of average sales, however this can easily be updated by changing these values to change the range per user request.
     - Error handling:
       - If the user entered non-integer characters or nothing an error message will be prompted as follows "You entered invalid data. Please try again".

![](readme_images/critical_level_error.png)
 - Sales
   - When a user adds sales data which can also be equivalent to any type of order, the actual calculation of stock, surplus and planned sales starts.
     - Error handling:
       - If the user entered non-integer characters or nothing an error message will be prompted as follows "You entered invalid data. Please try again".
       - If the user entered the wrong number or values or five values where at least one is negative, the error message will be the following: "Exactly 5 positive values required."

![](readme_images/sales_error.png)

- Surplus 
  - The surplus value illustrates how the latest sales or orders affected the current balance between existing stock and sales, the value written to the gspread can be interpreted as the number of orders to prepare to maintain the current stock without using the calculation of average sales and critical level.

- Planned sales
  - The planned sales values represent the actual values needed to produce or prepare for achieving the target value of stock. These values are calculated by adding the surplus value with the product of average sales and the critical level value.

### Program procedures
In the following description, the definition of "session" is equivalent to a program run without existing and restarting the program.

The program can be run in one or multiple sessions, where the first mentioned handles one time of adding critical level, sales and then exiting the program.
If no invalid data is entered, the following steps will be performed from a user perspective with a single session:
1. Run program.
2. Enter critical level data.
3. Enter sales data.
4. Enter "no" when being asked for adding more sales data (yes or no).
5. A list from the latest sales (maximum four sessions) will be presented to the user in the program, this is followed by a goodbye
   message and the program is exiting.


#### Program procedure - multiple sessions

When a user wish to perform several sessions, the program will return to step 3 instead of exiting program from step 4 and as long as the user enters
"yes" in step 4 this will continue.


For a "two-session" program run, these will be the steps.

1. Run program.
2. Entered critical level data.
3.(1) Enter sales data.
4.(1) Enter "yes" when being asked for adding more sales data (yes or no).
3.(2) Enter sales data.
4.(2) Enter "no" when being asked for adding more sales data (yes or no).
5. A list from the latest sales (maximum four sessions) will be presented to the user in the program, this is followed by a goodbye
   message and the program is exiting.  

In the below example a session with two runs will be presented, also images from the gspread sheet will be added to visualize the data flow and how values are fetched and written to the gspread sheets. In the example three sessions has already been stored and two more sessions will be added.

Adding two sessions of values to gspread:

- Before running the program the state of the sales sheets has been updated with three sessions, note that all sheets except the stock sheet will have three rows of data added to them once the sessions has completed successfully. An addtional row will allways be present on the stock sheet after a session since this is the data that which will be the basis to use for the next session.

Although the stock data has a one row "offset" compared to the other sheets, once the critical data has been entered by the user the critical value sheet will have the equal number temporary after the user has entered this value but has not yet added sales data.

----------------------------------------------------------------------------
-- Status of sales and critical level sheets before any update--:

SALES

![](readme_images/sales_before_enter.png)

CRITICAL LEVEL

![](readme_images/critical_level_before_sales.png)

-----------------------------------------------------------------------------

-- Status of sales and critical level sheets after enter the critical level--:
The value of 15 was entered.

FROM PROGRAM

![](readme_images/fifteen_percent.png)

CRITICAL LEVEL (Note the latest value added to the fifth row)

![](readme_images/criticlevel_before_sales.png)

-----------------------------------------------------------------------------

-- Status of sales after enter sales data--:
Following values were entered: 100,4000,300,20000,3

![](readme_images/sales_second_last.png)

-----------------------------------------------------------------------------

-- Status of sales, critical level after enter yes on "add more sales data"--:

Note that in this stage, when the user enters "yes" the critical level values are copied from the latest valid values entered by the user and these 
values are used to calculate the current session for stock and planned sales data.

FROM PROGRAM

![](readme_images/sales_yes.png)

CRITICAL LEVEL SHEET

![](readme_images/final_critical_level.png)

STOCK SHEET

![](readme_images/final_stock.png)


----------------------------------------------------------------------------

-- Status of sales, critical level after enter no on "add more sales data"--:

FROM PROGRAM 

Note that the trend for the last four sessions are presented, the latest values (20000, 30, 58, 850, 3000) are the ones at the end of each line.



![](readme_images/sales_after_no_answer.png)

SALES SHEET

![](readme_images/final_sales.png)

----------------------------------------------------------------------------


### Future Implementations
  - Use "bars” for the input fields that the user can move either with the mouse pointer (laptop) or fingers (phone/tablet), the calculation results would be updated continuously once the bar is dragged across the screen.
  - Connect the page to a database to let users add either a valid currency that can be added after the amount, by using a database the currency will be updated continuously. Furthermore, this type of functionality could also be used to use ratios between different currencies (e.g. compare the loan in euro and dollars).

### Accessibility

- I have been mindful during coding to ensure that the website is as accessible and friendly as possible. I have achieved this by:
- Coding according to PEP8 standard.
- 

## Technologies Used

### Languages Used
- Python
### Frameworks, Libraries & Programs Used

- [Am I Responsive](https://ui.dev/amiresponsive) & [Responsinator](http://www.responsinator.com/) - To show the website image on a range of devices.

- [EmailJS](https://www.emailjs.com/) - Mail service to send mail directly from javascript code.

- [Balsamiq](https://balsamiq.com/) - Used to create wireframes.

- [Favicon.io](https://favicon.io/) To create favicon.

- Git - For version control.

- Github - To save and store the files for the website.

- [Google Dev Tools](https://developer.chrome.com/docs/devtools/) - To troubleshoot and test features, and solve issues with responsiveness and styling.

- [Google Fonts](https://fonts.google.com/) - To import the fonts used on the website.



## Deployment & Local Development

The project was deployed using GitHub pages. The steps to deploy using GitHub pages are:

Go to the repository on GitHub.com
Select 'Settings' near the top of the page.
Select 'Pages' from the menu bar on the left of the page.
Under 'Source' select the 'Branch' dropdown menu and select the main branch.
Once selected, click the 'Save'.
Deployment should be confirmed by a message on a green background saying "Your site is published at" followed by the web address.

# Deployment
Codeanywhere IDE was used to write the code for this project and the Application has been deployed from GitHub to Heroku using the steps below with version releasing active.

## Heroku deployment
Deployment steps are as follows, after account setup:

* Select New in the top-right corner of your Heroku Dashboard, and select Create new app from the dropdown menu.
* Add a unique app name and then choose a region closest to you (EU or USA).
* Click on Create App.

In order for the project to run on Heroku, Heroku is needed to install the dependencies. 
* In the terminal write the following commando `pip3 freeze > requirements.txt` to create a list of requirements. The list of dependencies will go into the `requirements.txt` file.

The sensitive data needs to be kept secret and Heroku will build the app using the code in the Github. The creds.json file is protected in the gitignore file and these credentials are needed in order to connect to the API. To allow the Heroku Application to access the spreadsheet the following steps are needed:

* From the new app Settings, click Reveal Config Vars, and set the value of KEY to **CREDS** (all capital letters), and go to the repository, copy the entire`creds.json` then paste it into the VALUE field. Then click "Add". Add another KEY called **PORT** and VALUE **8000**, then click "Add".
* Further down, to support dependencies, select Add Buildpack.
* The order of the buildpacks is important, select Python first, then click "Save changes". Then add Node.js second and click "Save changes" again. If they are not in this order, you can drag them to rearrange them.
* Go to "Deploy" and select "GitHub" in "Deployment method".
* To connect Heroku app to your Github repository code enter your repository name, click 'Search' and then 'Connect' when it shows below
* Choose the branch you want to build your app from.
* If preferred, click on "Enable Automatic Deploys", which keeps the app up to date with your GitHub repository.
* Wait for the app to build. Once ready you will see the “App was successfully deployed” message and a 'View' button to take you to your deployed link.

[GitHub repository](https://github.com/luandretta/quiz-python) 

## Run locally
**Making a Local Clone**
1. Login or Sign Up to GitHub.
2. Open the project [repository](https://github.com/luandretta/quiz-python).
3. Click on the code button, select whether you would like to clone with HTTPS, SSH or GitHub CLI and copy the link shown.
4. Open the terminal in the code editor of your choice and change the current working directory to the location you want to use for the cloned directory.
5. Type 'git clone' into the terminal and then paste the link you copied in step 3. Press enter.

Add the files in your new local repository. This stages them for the first commit:
```bash
$ git add .
```

To unstage a file, use:
```bash
$ git reset HEAD YOUR-FILE
```

Commit the files that you've staged in your local repository:
```bash
$ git commit -m "First commit"
# Commits the tracked changes and prepares them to be pushed to a remote repository. To remove this commit and modify the file, use 'git reset --soft HEAD~1' and commit and add the file again.
```

Push the changes in your local repository to GitHub.com:
```bash
$ git push origin main
# Pushes the changes in your local repository up to the remote repository you specified as the origin
```

**Forking the GitHub Repository**
To fork this website to either propose changes or to use as an idea for another website, follow these steps:
1. Login or Sign Up to GitHub.
2. Open the project [repository](https://github.com/luandretta/quiz-python).
3. Click the Fork button in the top right corner.
4. Copy of the repository will be in your own GitHub account.

To deploy from GitHub, follow these steps:

1. Log into your GitHub repository, create a GitHub account if necessary.
2. Click 'Settings' in the main Repository menu.
3. Click 'Pages' from the left-hand side navigation menu.
4. Within the Source section, click the "Branch" button and change from 'None' to 'Main'.
5. The page should automatically refresh with a url displayed.
6. Test the link by clicking on the url.

The url for this website can be found [here](https://quizpython.herokuapp.com/) 
## Create data model and integrate using an API

- **Create a Spreadsheet (Data Model)**

1. Login to your Google account, create an account if necessary.
2. Navigate to Sheets, Google's version of Microsoft Excel.
3. Start a new spreadsheet, amend the title at the top i.e., quiz_python.
4. Create 2 Sheets/Tabs, titling 'questions' and 'answers'.
5. Add the data according to the screenshot in [Used-technologies](#used-technologies).


- **Setup API**

1. Navigate to Google Cloud Platform.
2. If you do not already have a profile then follow the basic steps for creating an Account, via clicking on the 'Get Started for Free' button in the upper right corner.
3. Once the previous step is complete, create a new project with a unique title.
4. Click on the "Select Project" button to bring you to your project page.
5. You should now arrive at the project dashboard and be ready to setup the required credentials:
- Access the navigation menu from clicking on the burger icon (three horizontal lines menu icon) in the top left corner of the page.
- Select APIs and Services, followed by 'Library'.
- Search for and select Google Drive API -> Enable.
- Search for and select Google Sheets API -> Enable.
- Click Enable to navigate to 'API and Services Overview'.
- Click Create Credentials in the upper left of the screen.
- For Credential Type, select 'Google Drive' from the dropdown.
- For 'What data will you be accessing' select Application Data.
- For 'Are you planning to use this API with Compute Engine...?' choose 'No, I'm not...'.
- Click Next.
- Within the Create Service Account page, enter a Service Account Name, then click Create.
- Next within 'Grant this service account access to project', choose Basic -> Editor from the 'Select a Role' dropdown and click Continue.
- Next within 'Grant users access to this service account', choose 'Done'.
- On the following, click on the 'Service Account Name' you created to navigate to the config page.
- Navigate to the Keys section.
- Select 'Add Key' dropdown -> Create New Key.
- Select 'JSON' and then click Create. This will trigger the json file with your API credentials in it to download to your machine.
- Go back to the library and search for "google sheets".
- Click Enable.
- From your local downloads folder, add the file directly to your Gitpod workspace, and rename the file to creds.json.
- Within the file, copy the value for 'client email'. 
- Paste this email address into the 'Share' area of your Google Sheet, assign the role of Editor, untick "Notify People" and then click "share".


Enable API within IDE

- From within your GitPod IDE terminal, enter 'pip3 install gspread google-auth'.

- At the top of your Python file add the following lines:
```python
import gspread
from google.oauth2.service_account import Credentials
```

- Below this add the following code:
```phyton
    SCOPE = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
       ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD.open("quiz_python")
```

---

## Testing

### Testing User Stories from (UX) Section
-  As a user I am interested in the website's purpose and eager to test the calculator.
  - The site has a clean look with few distractions, the fields are labeled and placeholder text to facilitate a short lead time to start calculations. 

- As a user I am understanding how to alternate values for retrieving different results.
  - The clear button indicates the fields can be updated continuously and the drop down menu indicates that several calculations can be performed.


- Using the send result function and comparing various results.
  - By sending the result the user can save the result if needed and compare the result with updated calculations or send the result to others.

####  Validator Testing
W3C Markup Validator
  - 

  ![lighthouse_test](readme_images/lighthouse.png)

####  Further Testing

- Calculation field
  - The form has been tested to ensure it would not enable the calculation button if the bank loan is less than <10000 or the interest field is empty.
  - The clear button is working independently from input field values as intended, meaning it will clear the fields regardless of value.

- Result: output testing
  - The result is presented as intended, loans at the lower range and with too high value of payoff years are displayed with red if the minimum requirements (minimum 100 amortization per month) are not met, whereas values passing minimum requirements are displayed with green and costs presented. Re-calculation and new results can be generated without reloading the page. 

- Send result
The name and email field was tested individually, the error message is shown for the name field regardless of the status for the email field and vice versa. The send result button is only enabled once both fields are valid, and if any field is changed before sending the mail, the button is set to disabled again.


- Browser Testing
  - The Website was tested on Google Chrome, Firefox, Microsoft Edge, and Safari browsers with no issues noted, except the deviations described in "known bugs/compromise" section below. 

- Device Testing
  - The website was viewed on a variety of devices such as Laptop, iPhone 11, and iPad to ensure responsiveness on various screen sizes. The website performed as intended. The responsive design was also checked using Chrome developer tools across multiple devices with structural integrity holding for the various sizes.

I also used the following website to test responsiveness:
- Responsinator
- Am I responsive

- Solved bugs
  -  A problem with the input field on Iphone 11 was detected during the late stage of testing, the restriction of number, letters or other characters did not behave the same way as for the laptop version. Some re-coding was needed to have a consistent function between laptop and phone. Especially solving how to allow digits and a dot only but no other characters and also only allowing two decimal digits used in the text field for interest rate required a major investigation.


- Known Bugs/compromise
  - When the program is run in codeanywhere it seems like, in certain conditions, (due to server connection issue or high load) a timeout error could occur, the operation and interaction could be interrupted leading to an error while the program tries to update the sheets after a calculation is performed. 
    

## Credits
### Code Used 

- Specific coding
  - The coding has similarities with "love sandwiches" walkthrough project, more specifically it is the way to update the worksheets (the code block called def update_worksheet(data, worksheet):. This process to update the sheets after each calculation could be seen as a rather general method, furthermore this code is concise and inventing a new alternative code doing the same thing was considered as irrational and did not add any user value.
  To summarize; the uniqueness for the project code is rather the concept of how the critical level, average sales are calculating stock and planned sales.

 - General coding
   - For inspiration and tips the major sources were:
   - [W3 Schools](https://www.w3schools.com)
   - [Mozilla](https://developer.mozilla.org/en-US/docs/Learn)


### Content

The idea is my own on how to code the calculation model, though some basics (as mentioned in the previous section) on how to connect the gspread sheets are inspired by the love sandwich project.


### Acknowledgments

- I would like to thank the following:
  - Antonio Rodriguez (mentor) for guidance and support. 
  - My family - for their patience with having me coding sometimes late evenings and nights.  