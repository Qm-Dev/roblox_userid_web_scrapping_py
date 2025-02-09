<p style="text-align: center">
    <img src="logo.jpg" width="350" height="150">
</p>
<h1 style="text-align:center">RuwsPy</h1>
<h2 style="text-align:center">Roblox User Web Scraper made in Python</h2>
<p style="text-align: center">This is a small side-project I made in Python with the purpose to retrieve
information about any <b>available</b> user in the Roblox platform website.</p>

## Features
* Retrive current username, alias, join date, ammount of friends and followers of any user.
## How to use
1. Execute ```ruws.py```
2. Indicate the User ID where you want to start the scrapping. You may retrieve the User ID by looking at any profile
in the platform:
```https://www.roblox.com/users/{USER_ID}/profile```
3. Indicate how many users you would like to skip during the scrapping. For example, if I start at ID `1` and choose a 
value of `10` for this field, the next scrapped user will be the one under ID `11`.
4. Indicate how many users you want to store once the scrapping finishes. The users successfully scrapped during the
execution of the program will be stored in a comma-separated value (CSV) file once the scrapping finishes (this may take
a while to be created).
