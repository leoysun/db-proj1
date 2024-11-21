# w4111-proj1

The PostgreSQL account where your database on our server resides. (This should be the same database that you used for Part 2, but we need you to confirm that we should check that database.)

The URL of your web application. Once again, please do not turn off your virtual machine after you are done modifying your code and when you are ready to submit, so that your IP address does not change and the URL that you include with your project submission works.

A description of the parts of your original proposal in Part 1 that you implemented, the parts you did not (which hopefully is nothing or something very small), and possibly new features that were not included in the proposal and that you implemented anyway. If you did not implement some part of the proposal in Part 1, explain why.


Briefly describe two of the web pages that require (what you consider) the most interesting database operations in terms of what the pages are used for, how the page is related to the database operations (e.g., inputs on the page are used in such and such way to produce database operations that do such and such), and why you think they are interesting.
A careful description of what AI tools you have used for the project, if any, and how, following strictly our project policies on usage of AI tools.

PostgreSQL account: jld2251

URL of web application: 

Continuity with Part 1:

We successfully implemented the display of dining halls and dining hall items on one singular page, making figuring out where to go eat much more efficient. We successfully implemented a review and rating system for the dining halls and their food items, which accomplishes the core original goal of allowing the database to store an accumulation of thoughts on dining halls and their food. 

We did not implement scraping of the dining websites - this is because we populated the database already with realistic data in Part 2, so we were able to work off that data to demonstrate the database and front-end interaction capabilities without scraping. Given more time in the future, we may add to this application to implement this, but for this class we were initially a bit overambitious with planning to web scrape, and we decided to focus on the databases aspect of this project more.
Additionally, we do not have a sorting feature but as we worked we realized that the important part was displaying and that a search or sorting feature would add unnecessary complications to this part of the project, especially since it would not use database-centered skills. 

We decided not to implement "clicking into" dining hall pages, as that defeats a primary purpose of the application which is to view dining halls conveniently on one page.

Extra features we added include the many UI features, such as being able to save the user's inputted user_id to attach to reviews and being able to DELETE reviews from both the UI and from the database, which is a nice use of database knowledge. There are many examples of SELECT and INSERT queries used throughout the app. 

Notes:
The same item can be repeatedly reviewed. 


The most interesting web pages are: 
1. The main page. 
- There are 2 primary forms. 
    - First, the User ID form acts as a form where the user can "log in" by inputting their User ID and username. Should the User ID not already exist in the Users table, this form adds the user to the database. If the inputted User ID is already in the database but receives a different than initially recorded username input, this form also updates the username for that corresponding user. Most importantly, however, this form saves the user information so that the user can delete their own reviews on the Delete reviews page. Moreover, once the user logs in, the navbar will update to reflect the User ID information of the current logged in user for clarity, and this is saved when the user proceeds to see all reviews or delete reviews.
        - This is particularly interesting since the User ID input here is stored across all pages and can reduce redundancy in submitting the same information later on. We weren't sure if this was even possible at first, so we felt proud after figuring this out.
        - This is also an example of how one singular form can be used in multiple ways for various database purposes!
    - Second, the user can write a review by inputting their user ID, selecting other attributes fo the meal, and providing a rating on a scale of 1-10 and review. Upon submission, the review is stored in several tables (Menu_is_from, Posts_Reviews, Evaluates, Discusses). The user is then brought to a page of all reviews. Alternatively, one can bypass needing to submit a review to see all reviews by simply clicking the See All Reviews button.
        - This shows how just one simple form interacts with so many entity sets and relationship sets. Since reviews is a major part of our application, this feature is particularly important.
- The core component of our web application is to display dining hall info all in one page. To do so, we iterate through all dining halls and extract information about them to display. We also iterate through all dining hall stations to display the items of each dining hall under each station, which was difficult to implement at first. With each item that is displayed, we also indicate the specific mealtime that it is shown for, as well as any dietary restrictions. Most uniquely, each dining hall also displays an average rating, calculated by taking the average of all the reviews for each item under one dining hall.
    - This feature also interacts with several different tables, such as the Menu_is_from, has_item, and contains. 
    - Displaying the average rating was particularly satisfying to accomplish, as it felt like a cohesive effort in connecting the dining hall info part of our application to the reviews part. It was cool to see how two different parts of our application could interact in such a natural manner.
2. The Delete reviews page. First of all,





AI Tools:
ChatGPT and Claude were used for front-end and syntax purposes only. In particular, the styling of the app was done mostly by AI