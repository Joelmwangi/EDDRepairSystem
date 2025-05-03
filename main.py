from models.customer import Customer
from models.technician import Technician
from models.equipment import Equipment
from models.admin import Admin
from models.supplier import Supplier
from services.job_service import JobService
from services.notification_service import NotificationService
from services.supplier_service import SupplierService
from utils.helpers import generate_job_id
from utils.exceptions import JobNotFoundError

job_service = JobService()
supplier_service = SupplierService()

# In-memory stores
customers = {}
technicians = {}

# Default Admin
admin = Admin("A001", "System Admin")

def main_menu():
    while True:
        print("\n=== EDDTech Repair Job Management (Admin Panel) ===")
        print("1. Create Customer")
        print("2. Register Equipment")
        print("3. Assign Job to Technician")
        print("4. Assess Job")
        print("5. Add Supplier")
        print("6. View Jobs")
        print("7. View Customers")
        print("8. View Technicians")
        print("9. Save Jobs to CSV")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            create_customer()
        elif choice == "2":
            register_equipment()
        elif choice == "3":
            assign_job()
        elif choice == "4":
            assess_job()
        elif choice == "5":
            add_supplier()
        elif choice == "6":
            view_jobs()
        elif choice == "7":
            view_customers()
        elif choice == "8":
            view_technicians()
        elif choice == "9":
            job_service.save_jobs_to_csv()
            supplier_service.save_suppliers_to_csv()
            print("Data saved to CSV.")
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

def create_customer():
    user_id = input("Customer ID: ")
    name = input("Customer Name: ")
    email = input("Customer Email: ")
    customer = Customer(user_id, name, email)
    customers[user_id] = customer
    print(f"Customer {name} created.")

def register_equipment():
    cust_id = input("Enter Customer ID: ")
    if cust_id not in customers:
        print("Customer not found.")
        return
    equipment_id = input("Equipment ID: ")
    name = input("Equipment Name: ")
    desc = input("Description: ")
    eq = Equipment(equipment_id, name, desc)
    customers[cust_id].add_equipment(eq)
    print("Equipment registered.")

def assign_job():
    tech_id = input("Technician ID: ")
    if tech_id not in technicians:
        name = input("Technician Name: ")
        email = input("Technician Email: ")
        expertise = input("Expertise: ")
        tech = Technician(tech_id, name, email, expertise)
        technicians[tech_id] = tech
    else:
        tech = technicians[tech_id]

    cust_id = input("Customer ID: ")
    if cust_id not in customers:
        print("Customer not found.")
        return
    cust = customers[cust_id]
    if not cust.equipment_list:
        print("Customer has no equipment registered.")
        return
    print("Available Equipment:")
    for i, eq in enumerate(cust.equipment_list):
        print(f"{i + 1}. {eq.name} - {eq.description}")
    eq_choice = int(input("Select equipment number: ")) - 1
    eq = cust.equipment_list[eq_choice]
    job_id = generate_job_id(len(job_service.jobs) + 1)
    job = job_service.create_job(job_id, tech, eq)
    NotificationService.notify_customer(cust, f"Job {job_id} created.")
    print(f"Job {job_id} assigned to technician {tech.name}.")

def assess_job():
    job_id = input("Enter Job ID: ")
    try:
        job = job_service.get_job(job_id)
        tasks = input("Enter tasks (comma separated): ").split(",")
        job_service.assess_job(job_id, [task.strip() for task in tasks])
        print(f"Job {job_id} assessed.")
    except JobNotFoundError as e:
        print(str(e))

def add_supplier():
    name = input("Supplier Name: ")
    location = input("Supplier Location: ")
    supplier = Supplier(name, location)
    supplier_service.add_supplier(supplier)
    print("Supplier added.")

def view_jobs():
    for job_id, job in job_service.jobs.items():
        print(f"{job_id}: {job.status} | Equipment: {job.equipment.name} | Technician: {job.technician.name}")

def view_customers():
    if not customers:
        print("No customers found.")
        return
    print("\n--- Customers ---")
    for cid, cust in customers.items():
        print(f"ID: {cust.user_id} | Name: {cust.name} | Email: {cust.email}")
        for eq in cust.equipment_list:
            print(f"   - Equipment: {eq.name} ({eq.description})")

def view_technicians():
    if not technicians:
        print("No technicians found.")
        return
    print("\n--- Technicians ---")
    for tid, tech in technicians.items():
        print(f"ID: {tech.user_id} | Name: {tech.name} | Email: {tech.email} | Expertise: {tech.expertise}")

if __name__ == "__main__":
    job_service.load_jobs_from_csv()
    supplier_service.load_suppliers_from_csv()
    main_menu()
