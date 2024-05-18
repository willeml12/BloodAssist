import ssl
import smtplib
from email.message import EmailMessage
import logging
import traceback

import CouchDBClient as CouchDBClient



# CouchDB client initialization
client = CouchDBClient.CouchDBClient()

def setup_views():
    map_function = """
    function (doc) {
        if (doc.type === 'user' && doc.bloodType) {
            emit(doc.bloodType, {email: doc.email});
        }
    }
    """
    try:
        client.installView('users_db', 'donorQueries', 'byBloodType', map_function)
        logging.info("View 'byBloodType' installed successfully.")
    except Exception as e:
        logging.error("Failed to install view 'byBloodType': %s", e)

def find_donors_by_blood_type(btype):
    try:
        # Execute view assuming the view 'byBloodType' correctly set up and exists
        results = client.executeView('users_db', 'donorQueries', 'byBloodType', btype)
        # Assuming the value contains an 'email' field
        return [row['value']['email'] for row in results if 'email' in row['value']]
    except Exception as e:
        logging.error("Error fetching donors by blood type %s: %s", btype, traceback.format_exc())
        return []


def send_emails(recipients, blood_type):
    """Send emails to a list of recipients regarding the need for blood donations."""
    sender = "jeanpython6@gmail.com"
    password = "gbfd vjme zsye uack"
    subject = "Urgent Need for Blood Donations"
    body = f"Dear Donor, \n\nWe urgently need donations of blood type {blood_type}. Please consider donating if you are able."

    em = EmailMessage()
    em['From'] = sender
    em['To'] = ", ".join(recipients)
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, password)
        smtp.send_message(em)
        logging.info("Emails sent successfully.")

# TODO : Use executeView + find a way to retrieve critical
def check_and_notify():
    """Check the blood stock and send notifications if the stock is below critical levels."""
    emailed_donors = set()
    
    try:
        print(client.listDatabases())
        
        # Execute view to get all blood stock entries
        groups = client.executeView('blood_db', 'banks', 'by_bloodtype')
        critical = client.executeView('blood_db', 'entries', 'by_type', key='criticalstocks')[0]
        
        stock_dict = {}
        for stock in groups:
            key = stock['key']
            value = stock['value']
            if key in stock_dict:
                stock_dict[key] += value
            else:
                stock_dict[key] = value

        for blood_type, total_stock in stock_dict.items():
            critical_stock = critical['value'].get(blood_type, 0)
            if total_stock < critical_stock:
                logging.info(f"Low stock for blood type {blood_type}: {total_stock} liters")
                
                # Identify all possible donors for this blood type, considering universal donors like O-
                possible_donors = find_possible_donors(blood_type)

                # Filter out donors who have already been emailed
                unique_donors = [donor for donor in possible_donors if donor not in emailed_donors]
                
                # Update the set of emailed donors
                emailed_donors.update(unique_donors)
                
                if unique_donors:
                    send_emails(unique_donors, blood_type)
                else:
                    logging.info("No new donors found for blood type %s who haven't been emailed yet.", blood_type)
                    
    except Exception as e:
        logging.error("Error during stock check: %s", traceback.format_exc())

def find_possible_donors(blood_type):
    """
    Extend this function to include compatible donors based on the ABO and Rh blood type system.
    """
    all_donors = []

    # Map of blood types to their possible donors
    compatible_donors = {
        "A+": ["A+", "A-", "O+", "O-"],
        "O+": ["O+", "O-"],
        "B+": ["B+", "B-", "O+", "O-"],
        "AB+": ["A+", "O+", "B+", "AB+", "A-", "O-", "B-", "AB-"],
        "A-": ["A-", "O-"],
        "O-": ["O-"],
        "B-": ["B-", "O-"],
        "AB-": ["AB-", "A-", "B-", "O-"]
    }

    # Check if the blood type is valid
    if blood_type in compatible_donors:
        # Add donors of the specific types that are compatible
        for donor_type in compatible_donors[blood_type]:
            all_donors.extend(find_donors_by_blood_type(donor_type))
    else:
        raise ValueError(f"Invalid blood type: {blood_type}")

    return list(set(all_donors))  # Remove duplicates
def update_blood_stock(blood_type, quantity_liters):
    """Add a new stock entry in the database for the specified blood type."""
    try:
        # Retrieve current stock for the blood type
        current_stock = 0
        groups = client.executeView('blood_db', 'banks', 'by_bloodtype')
        for stock in groups:
            if stock['key'].lower() == blood_type.lower():
                current_stock += stock['value']
        
        # Calculate new total stock
        new_total_stock = current_stock + quantity_liters
        
        # Check if the new total stock is negative
        if new_total_stock < 0:
            raise ValueError(f"Total stock for {blood_type} cannot be negative. Current stock: {current_stock}, attempted addition: {quantity_liters}")
        
        # Add a new document with the updated stock quantity
        client.addDocument('blood_db', {'type': 'entry', 'btype': blood_type, 'stock': quantity_liters, 'unit': 'l'})
        logging.info(f"Added new stock entry for {blood_type}: {quantity_liters} liters. New total stock: {new_total_stock} liters.")
    except ValueError as ve:
        logging.error(f"Invalid stock update for {blood_type}: {ve}")
        print(f"Error: {ve}")
    except Exception as e:
        logging.error(f"Failed to add stock entry for {blood_type}: {traceback.format_exc()}")


if __name__ == "__main__":
    setup_views()
    
    # Continuously ask the user what they want to do
    while True:
        print("Choose an option:")
        print("1. Check and notify donors based on current stock.")
        print("2. Update blood stock.")
        print("3. Exit.")
        
        user_choice = input("Enter your choice (1, 2, or 3): ")
        
        if user_choice == '1':
            check_and_notify()
        elif user_choice == '2':
            blood_type = input("Enter the blood type to update (e.g., A+, O-): ")
            quantity = input("Enter the quantity to add or to retrieve in liters: ")
            try:
                quantity_liters = float(quantity)  # Ensure the input is a valid float
                update_blood_stock(blood_type, quantity_liters)
            except ValueError:
                print("Invalid quantity. Please enter a numeric value.")
        elif user_choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid option. Please choose a valid number from the menu.")
