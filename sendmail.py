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

def check_and_notify():
    """Check the blood stock and send notifications if the stock is below critical levels."""
    
    # This dictionary will track which donors have already been emailed
    emailed_donors = set()
    
    try:
        # Print available databases for debugging purposes (could be removed in production)
        print(client.listDatabases())
        
        # Get all documents from the 'blood_db' database
        groups = client.listDocuments('blood_db')
        for group in groups:
            stock = client.getDocument('blood_db', group)
            # Assume stock and critical stock levels are strings ending with liter, e.g., '50 liters'
            current_stock = int(stock.get('stock', '0 liters').split()[0])
            critical_stock = int(stock.get('criticalstock', '0 liters').split()[0])
            
            if current_stock < critical_stock:
                logging.info(f"Low stock for blood type {stock.get('type')}: {stock.get('stock')}")
                
                # Identify all possible donors for this blood type, considering universal donors like O-
                possible_donors = find_possible_donors(stock.get('type'))

                # Filter out donors who have already been emailed
                unique_donors = [donor for donor in possible_donors if donor not in emailed_donors]
                
                # Update the set of emailed donors
                emailed_donors.update(unique_donors)
                
                if unique_donors:
                    send_emails(unique_donors, stock.get('type'))
                else:
                    logging.info("No new donors found for blood type %s who haven't been emailed yet.", stock.get('type'))
                    
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
    """Update the blood stock in the database by giving a new quantity in liters to the specified blood type."""
    try:
        # Fetch all document identifiers in the 'blood_db'
        doc_ids = client.listDocuments('blood_db')
        for doc_id in doc_ids:
            # Fetch each document to check if it's the right blood type
            stock = client.getDocument('blood_db', doc_id)
            if stock.get('type') == blood_type:

                new_stock = int(quantity_liters)
                # Update the document with new stock value
                stock['stock'] = f"{new_stock} liters"
                client.replaceDocument('blood_db', doc_id, stock)
                logging.info(f"Updated stock for {blood_type}: {new_stock} liters")
                return
        logging.error(f"No stock entry found for blood type {blood_type}")
    except Exception as e:
        logging.error(f"Failed to update stock for {blood_type}: {traceback.format_exc()}")


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
            quantity = input("Enter the new quantity in liters: ")
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
