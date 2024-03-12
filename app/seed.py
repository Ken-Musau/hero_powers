import random
from app import app
from models import db, Hero, HeroPower, Power


with app.app_context():
    Hero.query.delete()
    HeroPower.query.delete()
    Power.query.delete()

    print("🦸‍♀️ Seeding powers...")
    powers = [
        {"name": "super strength",
            "description": "gives the wielder super-human strengths"},
        {"name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed"},
        {"name": "super human senses",
            "description": "allows the wielder to use her senses at a super-human level"},
        {"name": "elasticity", "description": "can stretch the human body to extreme lengths"}
    ]

    for power_dict in powers:

        power = Power(**power_dict)
        db.session.add(power)

    db.session.commit()
    print("Successfully seeded powers...")

    print("🦸‍♀️ Seeding heroes...")

    heroes = [
        {"name": "Kamala Khan", "super_name": "Ms. Marvel"},
        {"name": "Doreen Green", "super_name": "Squirrel Girl"},
        {"name": "Gwen Stacy", "super_name": "Spider-Gwen"},
        {"name": "Janet Van Dyne", "super_name": "The Wasp"},
        {"name": "Wanda Maximoff", "super_name": "Scarlet Witch"},
        {"name": "Carol Danvers", "super_name": "Captain Marvel"},
        {"name": "Jean Grey", "super_name": "Dark Phoenix"},
        {"name": "Ororo Munroe", "super_name": "Storm"},
        {"name": "Kitty Pryde", "super_name": "Shadowcat"},
        {"name": "Elektra Natchios", "super_name": "Elektra"}
    ]

    for hero_dict in heroes:

        hero = Hero(**hero_dict)
        db.session.add(hero)

    db.session.commit()

    print("Successfully seeded Heroes")

    print("🦸‍♀️ Adding powers to heroes...")

    hero_ids = [hero.id for hero in Hero.query.all()]
    power_ids = [power.id for power in Power.query.all()]

    for i in range(len(heroes)):
        strengths = ["Strong", "Weak", "Average"]
        heroPower = HeroPower(
            strength=random.choice(strengths),
            hero_id=random.choice(hero_ids),
            power_id=random.choice(power_ids)
        )
        db.session.add(heroPower)

    db.session.commit()

    print("🦸‍♀️ Done seeding!")
