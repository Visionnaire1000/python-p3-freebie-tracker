from models import get_session, Dev, Company, Freebie

session = get_session()

musk = Dev(name="Musk")
louis = Dev(name="Louis")

grok = Company(name="Grok", founding_year=2023)
openai = Company(name="OpenAI", founding_year=2015)

session.add_all([musk, louis, grok, openai])
session.commit()

freebie1 = Freebie(item_name="T-shirt", value=20, dev=musk, company=openai)
freebie2 = Freebie(item_name="Laptop", value=2000, dev=louis, company=grok)

session.add_all([freebie1, freebie2])
session.commit()

print("Database seeded successfully!")
