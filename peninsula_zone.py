import json
import os
from world import NamedLocatable, Location, Passage, to_json


OUTPUT_FILE = "peninsula_zone.json"

# Setting up the party
the_party = NamedLocatable(name="The Party")
caltrop = NamedLocatable(name="Caltrop Bloodless")
gromag = NamedLocatable(name="Brother Gromag")
maximus = NamedLocatable(name="Gluteus Maximus")
kilvin = NamedLocatable(name="Kilvin")
the_party.members = [caltrop, gromag, maximus, kilvin]
the_party.caltrop = caltrop
the_party.gromag = gromag
the_party.maximus = maximus
the_party.kilvin = kilvin
caltrop.party = the_party
gromag.party = the_party
maximus.party = the_party
kilvin.party = the_party


# The kingdom or whatever
kingdom = Location(name="The Kingdom")


# The city
city = Location(name="The City", location=kingdom)
city.description = "A medium sized coastal city"

city.town_hall = Location(name="Town Hall", location=city)
city.town_hall.description = "{location:0}'s Town Hall"

city.militia_barracks = Location(name="Militia Barracks", location=city)
city.militia_barracks.description = "The local militia's barracks"

city.market = Location(name="Market", location=city)
city.market.description = "The local marketplace. Doubles as an open air trading space, and a caravan park, where traveling caravaneers stay for days to weeks at a time."

Location(name="a", location=city)
Location(name="b", location=city)
Location(name="c", location=city)
Location(name="d", location=city)
Location(name="e", location=city)
Location(name="f", location=city)
Location(name="g", location=city)


# The Go'Val race
go_val = NamedLocatable(name="Go'Val")


# Maran
maran = NamedLocatable(name="Maran")
maran.tribe = go_val

# Maran's Caravan
marans_caravan = NamedLocatable(name="Maran Go'Val's Caravan")
maran.location = marans_caravan
the_party.location = marans_caravan


# The party arrives in the city
marans_caravan = NamedLocatable(name="Maran Go'Val's Caravan")
marans_caravan.location = city


# Passage One : Arrival
arrival = Passage(name="Arrival in {location}", location=city, body="""
{the_party} arrives in {location:0} by way of a {tribe} caravan under the guidance of {caravan_leader}.

{caravan_leader}: Now that we've reached {location:0}, we're going to head to the market to trade. We'll be here, eh..., three to four days, depending on how things go. In the meantime, if you'd like to keep busy, there are a couple places around that usually have jobs posted.

{caravan_leader} (pointing left): If you head over to {city.town_hall:0} they usually have some postings about issues affecting the locals, weird happenings by the farms or rats in the sewer, that sort of thing.

{caravan_leader} (pointing behind): There's a {city.militia_barracks:0} back the way we came, near where we entered town.  They're always looking for able bodies to help with bandits and criminals.

{caravan_leader} (pointing ahead): Oh, and I almost forgot, the {city.market:0}! Sometimes wares go missing and the merchants there need someone to look into it, or, if it suits your fancy, there are usually caravans packing up to head to another town, and every caravan needs an escort.

{caravan_leader} (handing each of you 1gp): Here's your pay for this leg of the journey, and I hope to be hearing from you in three days. Good luck out there!

{caravan_leader} walks back over to the wagons shouting "Ok everybody, let's head down to the market and get set up!"

Shifty Guy (pointing right): We're going to head down this way, visit some friends, and get a drink. Besides, they've usually got some odd jobs that need doing.

Shifty Guy and a Hunter walk off to the right toward a shadier looking part of town.

Two others in mail with swords and shields head back toward the {city.militia_barracks:0}.

{the_party} decides to head over to {city.town_hall:0} to see what they can find.

""")
arrival.the_party = the_party
arrival.city = city
arrival.tribe = go_val
arrival.caravan_leader = maran


# The party heads to town hall
the_party.location = city.town_hall

# Maran's Caravan heads to the market
marans_caravan.location = city.market


# The party takes their first job
disturbing_disappearances_taken = Passage(
    name="Disturbing Disappearances Taken",
    location=city.town_hall,
    body="""
Two other members of the roughly ten person caravan escort. The first is a tall slender man wearing a full length robe and and carrying a pouch around his neck, a small pack, and an ornate jeweled dagger on his hip. The second is wearing a chain mail vest, plate greaves, and gauntlets, with a spear over one shoulder and a quiver with several javelins over the other and a large pack on his back.

{the_party.caltrop} tries attempts to pick pocket the robed man, but ends up roughly bumping into him. {the_party.caltrop} manages to play it off as though he stumbled, raising the suspicious of both men, but not inciting anything worse.

Once {the_party} reaches {location:0}, they look over the job board, deciding between a rat infestation and mysterious disappearances in the woods. They choose to investigate the disappearances, hearing that a couple of farmers went missing and the three person militia squad that went out in search of them only had one member return. The remaining member is stable, recovering from wounds, at the {city.militia_barracks:0}.
""")
disturbing_disappearances_taken.the_party = the_party
disturbing_disappearances_taken.city = city



disturbing_disappearances_investigation = Passage(
    name="Disturbing Disappearances Investigation", 
    location=city.militia_barracks, 
    body="""
{the_party} heads over to the {city.militia_barracks:0} and learn that the surviving militiaman is named Frankie. After convincing someone that {the_party.caltrop} is Frankie's friend, they head up to Frankie's room and ask him some questions. Frankie was clearly scratched and bitten by something and he still seems shocked or horrified by whatever he saw. He tells {the_party} that he found "it" in the forest west of town, just to the north of the giant birch on the right.
""")
disturbing_disappearances_investigation.the_party = the_party
disturbing_disappearances_investigation.city = city


# Dump the data out
with open(OUTPUT_FILE, "w") as fl:
    json.dump(
        {
            "name": "The Peninsula Zone",
            "objects": to_json(kingdom),
        },
        fl
    )


"""
Head to the market, leaving Kilvin behind to keep an eye out

Approach a teen playing in the market and ask about Frankie.
"Who's that?"
Party starts to babble about stuff
"Hold on one sec kid"
"Uh, ok"
Kid returns to kicking around a ball and running around with his friends
Ask about the birch tree, kid saw some on the way to town.
Ask about local kids, he doesn't really know much, except they come down sometimes with their parents

Go to more permanent looking booth occupied by a local farmer

Maximus flies back to get Kilvin and they meet up with the others by the western road out of town

Fight the zombies

Return to town with their heads as proof.  While 

Ryan robs some people of their iron silverware

Spend the night with the caravan

Head to town hall in the morning to get payment for the zombies.  Suspicious of the clerk for hiding the ledger sheet, they ask about it.  Was 3gp originally, increased to 5 + 1 per monster after the militia patrol failed.

"""
