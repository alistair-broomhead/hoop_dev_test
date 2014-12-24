"""
The `rest` app handles serialisation and views of the models in the `data` app
as a RESTful service. For the purposes of this coding test the two apps could be
combined, but in a real-world scenario we may want more than one service that
consumes the `data` app's models. Keeping them separated as such also helps to
more explicitly mark the separation of our concerns.

The default rendering of the endpoints provided by this app is a web page with
a pretty-formatted version of the json output - if you log in with valid
credentials (set when you perform the first syncdb - on heroku I have used
'admin' for both username and password) then you will see further interactions
at the bottom of the page, such as to POST a new item on a list view, or
PUT/DELETE an existing item on an individual view.

The event list can be sorted by adding a query parameter of 'order_by' - this
explicitly supports location and category, but I have not disabled other options
- further to the spec I have made it possible to add 'location' or 'category'
specifiers to the query string in order to filter your output.

Seeing as it was simple and easy I have added endpoints representing locations
and categories so you can see how many events each has, and if you follow the
url to an individual location or category you will see a list of the events for
said location or category.
"""