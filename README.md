# w4111-proj1
# Leo Sun and Julia Ding
# UNIs: lys2121, jld2251

The URL of your web application. Once again, please do not turn off your virtual machine after you are done modifying your code and when you are ready to submit, so that your IP address does not change and the URL that you include with your project submission works.

PostgreSQL account: jld2251

URL of web application: **TODO**


Continuity with Part 1:

We successfully implemented the display of dining halls and dining hall items on one singular page, making figuring out where to go eat much more efficient. We successfully implemented a review and rating system for the dining halls and their food items, which accomplishes the core original goal of allowing the database to store an accumulation of thoughts on dining halls and their food. 

We did not implement scraping of the dining websites - this is because we populated the database already with realistic data in Part 2, so we were able to work off that data to demonstrate the database and front-end interaction capabilities without scraping. Given more time in the future, we may add to this application to implement this, but for this class we were initially a bit overambitious with planning to web scrape, and we decided to focus on the databases aspect of this project more.
Additionally, we do not have a sorting feature but as we worked we realized that the important part was displaying and that a search or sorting feature would add unnecessary complications to this part of the project, especially since it would not use database-centered skills. 

We decided not to implement "clicking into" dining hall pages, as that defeats a primary purpose of the application which is to view dining halls conveniently on one page.

Extra features we added include the many UI features, such as being able to save the user's inputted user_id to attach to reviews and being able to DELETE reviews from both the UI and from the database, which is a nice use of database knowledge. There are many examples of SELECT and INSERT queries used throughout the app. Another improvement we made on our original plan is the display of average rating for reviews of each dining hall, and we slightly altered the evaluates and discusses tables to contain the rating attribute so that ratings can be a part of reviews.

Notes:
A UNI must be inputted upon the running of the app before review deletion is allowed. 
The same item can be repeatedly reviewed. This would of course become a problem on a larger scale but for now this helps to populate the database.

Other possible improvements: 
Filtering the Item Name dropdown by the dining hall name selected. 
Making the front-end error checking (e.g. preventing certain actions before UNI is inserted) more seamless.
Populating more dining hall item data with more accuracy (this would naturally be improved as the app persists long-term)


The most interesting web pages are: 
1. The main page. 
- There are 2 primary forms. 
    - First, the User ID form acts as a form where the user can "log in" by inputting their User ID and username. Should the User ID not already exist in the Users table, this form adds the user to the database. If the inputted User ID is already in the database but receives a different than initially recorded username input, this form also updates the username for that corresponding user. Most importantly, however, this form saves the user information so that the user can delete their own reviews on the Delete reviews page. Moreover, once the user logs in, the navbar will update to reflect the User ID information of the current logged in user for clarity, and this is saved when the user proceeds to see all reviews or delete reviews.
        - This is particularly interesting since the User ID input here is stored across all pages and can reduce redundancy in submitting the same information later on. We weren't sure if this was even possible at first, so we felt proud after figuring this out.
        - This is also an example of how one singular form can be used in multiple ways for various database purposes!
    - Second, the user can write a review by inputting their user ID, selecting other attributes fo the meal, and providing a rating on a scale of 1-10 and review. Upon submission, the data associated with the review is stored in several tables (Menu_is_from, Posts_Reviews, Evaluates, Discusses) from which data is retrieved for the reviews display. The user is then brought to a page of all reviews. Alternatively, one can bypass needing to submit a review to see all reviews by simply clicking the See All Reviews button.
        - This shows how just one simple form interacts with so many entity sets and relationship sets. Since reviews is a major part of our application, this feature is particularly important.
- The core component of our web application is to display dining hall info all in one page. To do so, we iterate through all dining halls and extract information about them to display. We also iterate through all dining hall stations to display the items of each dining hall under each station, which was difficult to implement at first. With each item that is displayed, we also indicate the specific mealtime that it is shown for, as well as any dietary restrictions. Most uniquely, each dining hall also displays an average rating, calculated by taking the average of all the reviews for each item under one dining hall.
    - This feature also interacts with several different tables, such as the Menu_is_from, has_item, and contains. 
    - Displaying the average rating using an aggregate operator was particularly satisfying to accomplish, as it felt like a cohesive effort in connecting the dining hall info part of our application to the reviews part. It was cool to see how two different parts of our application could interact in such a natural manner.

2. The Delete reviews page. 
- First of all, the user navigates to this page with the button to select reviews for deletion -- this exists so that this page can be presented where only the user's reviews are present (assuming they have inserted their UNI). This provides not only a clear way to view one's own past reviews, but also to prevent the user from deleting any reviews other than their own. 
    - When the Delete Review button is pressed on any given review, that review's associated data is removed from the evaluates, discusses, and posts_reviews tables. 
    - We designed it so that the data for a review must be present in these three tables to display them, meaning that the review also disappears off the display instantly! We really enjoy this feature and think it is a great use of the database. With one click of a button, several tables are manipulated seamlessly.
        - The menu_is_from table is not removed from; this is because the menu_is_from table is meant to contain menus from each mealtime for each dining hall, and should only become more and more populated. This table was not used much in this application, except that it is inserted into when reviews are posted to help with seamless population of its data. 
    - The Back to Home button is also present on this page so the user can navigate back when done deleting or viewing reviews of their choice.

AI Tools:
ChatGPT and Claude were used for front-end and syntax purposes only. In particular, a significant amount of the styling and front-end organization of the app was done by AI. When our code logic was correct but there were some minor syntax issues that blocked our progression, we employed some AI usage as well. Queries were AI-free but some Googling was used.