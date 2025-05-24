# Paytracker
#### Video Demo:  https://youtu.be/qyknkRDPqS4
#### Description: A web app that calculates and tracks sales and commission for sales people

## Overview
Paytracker is a web app built using the Django framework and Bootstrap. I really enjoyed the Finance project when I was first exposed to back-end development,
so much that I immediately jumped into CS50Web. I got the idea for this app based on my previous experience in automotive sales. Most of my colleagues and I kept
track of our pay through pen-and-paper, whether it was ledgers, bulletin boards or sticky-notes stuffed haphazardly into our desks.
I recognized this as an inefficiency. Paper records get lost and extrapolating information from them requires manual calculations. So I decided to apply what I learned in CS50
to create a web app that would allow me as a salesperson to log my sales, sort them by month, and view relevant metrics regarding my performance.

## Models
I created several models to store the information I want in a database.

### Sale Model
The first model I created was a model that would store profit earned from a sale, as well as the user who received credit for the sale,
and also the date the sale was recorded so that I could then manipulate and sort this information later.
I used a foreign key to link the field where sale credit is recorded so that I could easily associate who sold what with the currently logged in user.
The field for the date when the sale was logged has a default value of the current time by timezone, so that
the time the user logs their sale will always be saved without any additional input required from the user.

### Payplan Model
The purpose of my next model is to store relevant information about the user's commission.
The Payplan model records the commission percentage the user received for profit on their sales,
and if relevant the amount of sales the user must complete before receiving that commission percent.
#### For example, a user receives 20% of the profit for each sale as a base, then if that user makes 10 sales
#### that commission percent is bumped up to 25%, calculated retroactively with the sales they've already made.
The same as the Sale model, the Payplan model has a foreign key for the User model so that the details of the payplans
stored in the database are associated with the approriate logged in user.

### VolumeBonus model
The VolumeBonus model, when relevant, stores any additional pay the user receives for hitting a sales milestone.
Like the Payplan model, it stores the amount of sales required to achieve the additional payable amount, as well as a foreign key
for the user.

### Flat model
If a user's calculated commission for a sale falls below a certain threshold, then that salesperson instead receives
what's commonly referred to as a "flat." The flat amount for the user is stored in this model, and to account for the potential of a scaling
flat amount, the Flat model has a field for required sales to receive a higher amount in flats.
Same as before, this model uses the User model as a foreign key.

### User model
Lastly, I created my own model for users in addition to the model I imported from Django.
The purpose was so that I could display the user's information back to them when they are logged in on
their user account page.


## Apps
I have four apps inside my Paytracker app that each handle a specific function.

### Homepage App
The first app is simply an app that gives Paytracker a place to redirect, with only two HTML files:
an index file and a layout file. I found that each app having it's own layout file made it easier to make modifications if they
became necessary, instead of using a single layout for the entire web app.
The Homepage app's index displays some introductory text about Paytracker, and invites the visitor to register for the site.

### Payplan App
The Payplan app handles everything related to creating a newly registered user's first payplan,
modifying the current payplan, and adding parameters like a sales volume bonus for the user, scaling commission
percentages, and the amount they receive for a flat.
This app has the most templates, since I found that compartmentalizing the app's functions made it easier for me to organize
how everything works and how all the components relate to one another.
#### Payplan.views
The app's first view is the index() view, which first checks if a user is authenticated, and if they're not
calls reverse on the User's app 'login' path, sending a user that's not logged in back to the login page.

Second is select_payplan(), a view that checks for an authenticated user, and if they are renders a page where the user can select
how they would like to manage the details of their pay plan.

Next is add_payplan(), a function that checks if the user has already entered an amount they receive for commission.
If the user already has a percent entered for commission, a template is rendered where the user can now add levels to their payplan,
with the additional amount and the sales required for that amount rendered in a form on the page.
When the user completes the form, this view evaluates the request type, and if the type is POST,
evaluates the form for validity and saves it in the Payplan model.

The add_level() function saves the additional sales required and increased commission amount to hit a milestone increased
a scaling commission-based payplan. Same as add_payplan() the function checks the request for type. If request is POST
the info is saved in the Payplan model, otherwise a GET request will render current payplan info of the user, and if the user
reaches this page without a payplan saved an error message will display informing them they have no payplan saved.

update_payplan() is what allows the user to make changes to their pay plan. From here they can delete an entry they made, for example a user that receives
20% base commission and now longer receives 25% after 10 sales can delete the part of their payplan that scales, so that calculations later on will be accurate.
The user can also edit commission percentages if they've changed.

add_flat() allows the user to record the amount they receive for flats. Request methods are evaluated similar to previous functions,
a GET request renders a form and a POST requests saves a valid form's cleaned data in the appropriate database.

add_volume_bonus() allows the user to record any additional dollar amounts they will be compensated for selling a certain number of units.


### Saletracker App

The saletracker app is what displays metrics on a user's sales. It makes calculations, allows the user to record a sale
filter by month sold, and allows the user to delete a logged sale.

#### saletracker.views

The largest function here is saletracker's index function. I wanted the logic to be extensive, so that
any of the varies queries would not create any errors in how program. This function authenticates the user, displays their recorded sales,
analyzes amounts of sold units, flat earned, current commission percents, any volume bonuses, and the total amount
the user can expect to earn.
Everything is dynamic, accounting for scaling commission percentages, deleted sales, and increased or decreased volume bonuses.

The log() function allows the user to record a sale, a form I created is passed to a template, then when completed the POST request saves the information
in the Sale model, and the user is redirected back to the index where their sale information is displayed.

The remove_log() function simply deletes a user's recorded sale. The index is then rendered without any additional kwargs.

### Users App

The user's app manages logins, registration and logout.

### Django implementation

I used Django to style this page, using their form and table templates extensively.