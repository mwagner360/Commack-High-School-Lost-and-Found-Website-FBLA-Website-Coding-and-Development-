"""
adds some sample items to the database so the site isnt empty for fbla purposes
"""
from app import app, db
from models import Item, Claim, Transaction

sampleItems = [
    {
        "title": "Blue North Face Backpack",
        "category": "Accessories",
        "description": "found this by the vending machines after lunch. its a dark blue north face borealis, has a dinosaur keychain and some stickers on the front pocket. kinda heavy so theres probably textbooks in it",
        "location": "Cafeteria",
        "dateFound": "2026-02-25",
        "finderName": "Jake Torres",
        "finderEmail": "jtorres@stu.commack.k12.ny.us",
        "status": "approved",
    },
    {
        "title": "TI-84 Calculator",
        "category": "Electronics",
        "description": "someone left their graphing calculator on the desk in room 212 after 5th period. its a TI-84 plus CE and theres a name on the back in silver sharpie that says S. Patel",
        "location": "Room 212",
        "dateFound": "2026-02-26",
        "finderName": "Maria Chen",
        "finderEmail": "mchen@stu.commack.k12.ny.us",
        "status": "approved",
    },
    {
        "title": "Gray Nike Hoodie",
        "category": "Clothing",
        "description": "gray nike pullover left on the bleachers after the game on friday. size medium, no name on the tag. its been sitting there all weekend",
        "location": "Gym",
        "dateFound": "2026-02-24",
        "finderName": "Ryan Murphy",
        "finderEmail": "rmurphy@stu.commack.k12.ny.us",
        "status": "approved",
    },
    {
        "title": "AirPods Pro Case",
        "category": "Electronics",
        "description": "found an airpods case on the floor by the water fountain upstairs. just the case though, no airpods inside. white, normal looking, no engravings or anything",
        "location": "2nd Floor Hallway",
        "dateFound": "2026-02-27",
        "finderName": "Emma Vitale",
        "finderEmail": "evitale@stu.commack.k12.ny.us",
        "status": "approved",
    },
    {
        "title": "Car Keys w/ Honda Fob",
        "category": "Keys",
        "description": "found a set of keys in the senior parking lot by the back entrance. honda key fob plus like 3 other keys on a plain silver ring. no other keychains or anything",
        "location": "Student Parking Lot",
        "dateFound": "2026-02-27",
        "finderName": "Aiden DeLuca",
        "finderEmail": "adeluca@stu.commack.k12.ny.us",
        "status": "approved",
    },
    {
        "title": "Teal Hydro Flask",
        "category": "Water Bottles",
        "description": "32oz hydro flask, teal color, covered in stickers. one of them is a smiley face and another says long island. theres a dent on the bottom. was left in mr garcias room",
        "location": "Room 104",
        "dateFound": "2026-02-28",
        "finderName": "Sofia Reyes",
        "finderEmail": "sreyes@stu.commack.k12.ny.us",
        "status": "approved",
    },
    {
        "title": "APUSH Textbook",
        "category": "Books",
        "description": "american pageant textbook, 17th edition. someone highlighted like all of chapter 12. no name written anywhere in it, could be anyones honestly",
        "location": "Library",
        "dateFound": "2026-02-26",
        "finderName": "Lucas Ferraro",
        "finderEmail": "lferraro@stu.commack.k12.ny.us",
        "status": "approved",
    },
    {
        "title": "Black Adidas Cleats",
        "category": "Sports",
        "description": "pair of black adidas predator cleats size 10. left in the locker room after practice on tuesday. theyre pretty beat up but still wearable",
        "location": "Boys Locker Room",
        "dateFound": "2026-02-25",
        "finderName": "Dylan Park",
        "finderEmail": "dpark@stu.commack.k12.ny.us",
        "status": "approved",
    },
    {
        "title": "Silver Bracelet",
        "category": "Accessories",
        "description": "thin silver bracelet with a little heart charm, found on the sink in the first floor girls bathroom. looks like it might be real silver idk",
        "location": "1st Floor Bathroom",
        "dateFound": "2026-02-28",
        "finderName": "Olivia Santos",
        "finderEmail": "osantos@stu.commack.k12.ny.us",
        "status": "pending",
    },
    {
        "title": "Red USB Flash Drive",
        "category": "Electronics",
        "description": "found a red sandisk flash drive plugged into one of the media center computers. 64gb. has a label that says english project but no name",
        "location": "Media Center",
        "dateFound": "2026-02-28",
        "finderName": "Noah Brennan",
        "finderEmail": "nbrennan@stu.commack.k12.ny.us",
        "status": "pending",
    },
]

claimedItem = {
    "title": "Student ID - James Rodriguez",
    "category": "Keys",
    "description": "found james rodriguez's student ID on the floor outside room 301. grade 11",
    "location": "3rd Floor Hallway",
    "dateFound": "2026-02-20",
    "finderName": "Chloe Anderson",
    "finderEmail": "canderson@stu.commack.k12.ny.us",
    "status": "claimed",
}

with app.app_context():
    Transaction.query.delete()
    Claim.query.delete()
    Item.query.delete()
    db.session.commit()

    for data in sampleItems:
        db.session.add(Item(**data))

    db.session.add(Item(**claimedItem))
    db.session.commit()

    backpack = Item.query.filter_by(title="Blue North Face Backpack").first()
    if backpack:
        db.session.add(Claim(
            itemId=backpack.id,
            claimantName="Daniel Kim",
            claimantEmail="dkim@stu.commack.k12.ny.us",
            message="thats my backpack i left it in the cafeteria on tuesday. it has my precalc notebook and a phone charger inside, the keychains are a dinosaur and a carabiner",
            status="open",
        ))

    calc = Item.query.filter_by(title="TI-84 Calculator").first()
    if calc:
        db.session.add(Transaction(
            itemId=calc.id,
            buyerName="Priya Patel",
            buyerEmail="ppatel@commack.k12.ny.us",
            cardLast4="4819",
            amount=2.99,
        ))

    db.session.commit()
    print("added " + str(len(sampleItems) + 1) + " items, 1 claim, 1 transaction")