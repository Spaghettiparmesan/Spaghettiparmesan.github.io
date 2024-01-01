# Fuel Efficiency Tracker
#### Video Demo:  <URL HERE>
#### Description:
I always used a little note on my phone to track how much i fill up the gas tank of my car and how far i can drive with that, so that i can roughly estimate my consumption since my car is not able to do that on its own. From here i got the idea to just ease that tracking for the future and combine it with a few usefull features. So the thought behind this developed into my little web application for the final project. I thought it will be the easiest form to track this, since i can use it on my smartphone to input data and on the pc to analyze and get an overview. So my Fuel Efficiency Tracker is a web application that allows users to record and analyze their personal gas consumption, related expenses, and price developments over time. To create that i oriented on the Finance project of lecture 9 and tried to build my own version for a completely different purpuse with new features. But so I used the same environment as in the finance application to run the whole website.

## Project Structure

### Files

- **app.py**: The main Python/Flask application file that defines routes, handles user authentication, and connects to the database.

- **functions.py**: Contains utility functions used in the main application, such as user authentication and calculations.

- **data.db**: SQLite database file that stores user data and history entries.

- **style.css**: The main stylesheet for the application, providing styles for various elements in a static folder.

- **templates folder**:
  - **layout.html**: The base HTML layout file shared across all pages, containing the common structure and styles.
  - **index.html**: HTML template for the homepage where users can input gas consumption data.
  - **login.html**: HTML template for the login page.
  - **register.html**: HTML template for the registration page.
  - **history.html**: HTML template for displaying user transaction history.
  - **analytics.html**: HTML template for displaying analytics on consumption, expenses, and costs over time.
  - **edit.html**: HTML template for allowing users to edit previous inputs.
  - **tips.html**: HTML template for providing fuel efficiency tips in an interactive way.
  - **apology.html**: HTML template for displaying error messages and codes to the user.


## Usage

- **Home (/)**: Input your gas consumption data.
- **History (/history)**: View a list of your past transactions.
- **Analytics (/analytics)**: Analyze your personal development of consumption and costs over time.
- **Edit (/edit/<event_id>)**: Edit previous inputs.
- **Tips (/tips)**: Explore fuel efficiency tips in an interactive way.
