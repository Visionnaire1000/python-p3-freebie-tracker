from lib.models import get_session, Dev, Company, Freebie

session = get_session()

def list_dev_freebies():
    dev_name = input("Enter the developer's name:(e.g Musk,Louis) ")
    dev = session.query(Dev).filter_by(name=dev_name).first()
    if dev:
        if dev.freebies:
            print(f"{dev_name} owns the following freebies:")
            for freebie in dev.freebies:
                print(f"- {freebie.item_name} from {freebie.company.name} (Value: {freebie.value})")
        else:
            print(f"{dev_name} has no freebies.")
    else:
        print("Developer not found.")

def list_company_freebies():
    company_name = input("Enter the company name:(e.g OpenAI,Grok) ")
    company = session.query(Company).filter_by(name=company_name).first()
    if company:
        if company.freebies:
            print(f"{company_name} has given the following freebies:")
            for freebie in company.freebies:
                print(f"- {freebie.item_name} given to {freebie.dev.name}")
        else:
            print(f"{company_name} has not given any freebies.")
    else:
        print("Company not found.")

def list_company_devs():
    company_name = input("Enter the company name:(e.g Grok,OpenAI) ")
    company = session.query(Company).filter_by(name=company_name).first()
    if company:
        devs = {freebie.dev.name for freebie in company.freebies}
        if devs:
            print(f"Developers who received freebies from {company_name}: {', '.join(devs)}")
        else:
            print(f"No developers have received freebies from {company_name}.")
    else:
        print("Company not found.")

def give_freebie():
    company_name = input("Enter the company name:(e.g Grok,OpenAI) ")
    dev_name = input("Enter the developer's name: (e.g Musk,Louis)")
    item_name = input("Enter the freebie item name:(e.g Laptop if Louis,T-shirt if Musk) ")
    value = int(input("Enter the value of the freebie:(e.g 2000 for Laptop,20 for T-shirt ) "))

    company = session.query(Company).filter_by(name=company_name).first()
    dev = session.query(Dev).filter_by(name=dev_name).first()

    if company and dev:
        freebie = company.give_freebie(dev, item_name, value)
        session.add(freebie)
        session.commit()
        print(f"{company_name} gave a {item_name} to {dev_name}.")
    else:
        print("Company or Developer not found.")

def find_oldest_company():
    oldest = Company.oldest_company(session)
    if oldest:
        print(f"The oldest company is {oldest.name}, founded in {oldest.founding_year}.")
    else:
        print("No companies found.")

def check_freebie_ownership():
    dev_name = input("Enter the developer's name:(e.g Musk,Louis) ")
    item_name = input("Enter the freebie item name:(e.g Laptop if Louis,T-shirt if Musk) ")
    dev = session.query(Dev).filter_by(name=dev_name).first()

    if dev:
        if dev.received_one(item_name):
            print(f"{dev_name} owns a {item_name}.")
        else:
            print(f"{dev_name} does not own a {item_name}.")
    else:
        print("Developer not found.")

def transfer_freebie():
    from_dev_name = input("Enter the name of the developer giving away the freebie:(e.g Louis,Musk) ")
    to_dev_name = input("Enter the name of the developer receiving the freebie:(e.g Musk,Louis) ")
    item_name = input("Enter the name of the freebie being transferred:(Laptop from Louis,T-shirt from Musk) ")

    from_dev = session.query(Dev).filter_by(name=from_dev_name).first()
    to_dev = session.query(Dev).filter_by(name=to_dev_name).first()

    if from_dev and to_dev:
        freebie = next((f for f in from_dev.freebies if f.item_name == item_name), None)
        if freebie:
            from_dev.give_away(to_dev, freebie)
            session.commit()
            print(f"{from_dev_name} gave {item_name} to {to_dev_name}.")
        else:
            print(f"{from_dev_name} does not own a {item_name}.")
    else:
        print("One or both developers not found.")

def main():
    while True:
        print("\nChoose an option:")
        print("1. List a developer's freebies")
        print("2. List a company's freebies")
        print("3. List developers who received freebies from a company")
        print("4. Give a freebie from a company to a developer")
        print("5. Find the oldest company")
        print("6. Check if a developer owns a freebie")
        print("7. Transfer a freebie from one developer to another")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            list_dev_freebies()
        elif choice == "2":
            list_company_freebies()
        elif choice == "3":
            list_company_devs()
        elif choice == "4":
            give_freebie()
        elif choice == "5":
            find_oldest_company()
        elif choice == "6":
            check_freebie_ownership()
        elif choice == "7":
            transfer_freebie()
        elif choice == "8":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
