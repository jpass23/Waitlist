# Waitlist

This was a project I did for a friend of mine at [Sketchonic Design](https://www.sketchonicdesign.com/). She does live portraits of people and ran into the issue of people wanting their portrait done while she was working with others. She needed a way to add them to a waitlist and contact them when she was ready so that they could keep exploring Asheville while they waited. 

Plenty of waitlist apps exist but they all use a paid feature to contact the customer. Since she was using a phone already, she's paying for service anyway and should be able to use that to contact the customer. This was the problem I set out to solve.

## Description

There are 3 main pages to this waitlist app:

1. The join page
2. The page to show the customer their place in line
3. The actual waitlist

Join the waitlist [here](https://waitlist-1-c5006775.deta.app/join-waitlist) and it will redirect to the next page. Check the waitlist [here](https://waitlist-1-c5006775.deta.app/waitlist/3014707)

If the [waitlist page](https://waitlist-1-c5006775.deta.app/waitlist/3014707) is accessed via a mobile device, clicking the phone number of the next person in line will automatically redirect to the messaging app and populate a text with the desired information to contact the client. 

Pages 1 and 2 are customer facing which is why there is CSS. The waitlist page not being customer facing allows for no CSS and a goofy title.

## Screenshots:
<div align=center>

<img src="https://raw.githubusercontent.com/jpass23/Waitlist/main/Screenshots/Join%20Page.png" width="525"/>

<img src="https://raw.githubusercontent.com/jpass23/Waitlist/main/Screenshots/Place%20In%20Line%20Page.png" width="400"/>

</div>

<div align=center>
<img src="https://raw.githubusercontent.com/jpass23/Waitlist/main/Screenshots/Waitlist%20Page.png" width="925"/>
</div>

## Design Structure

This is a fullstack webapp. It is hosted on [Deta.Space](https://deta.space/). The data persists through Collections, a database feature offered by Deta. The API is written is Python using FastAPI. There is no framework used for the frontend since it is so simple. The HTML is served directly from an endpoint using Jinja2.
