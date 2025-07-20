from tabulate import tabulate
from datetime import datetime, timedelta

# === Data Master ===
car_stock = {
    "Mitsubishi Expander": {"price": 550000, "stock": 5},
    "Toyota Fortuner": {"price": 1100000, "stock": 6},
    "Pajero Sport": {"price": 1200000, "stock": 6},
    "Hyundai Creta": {"price": 700000, "stock": 3},
    "Suzuki Ertiga": {"price": 500000, "stock": 4},
    "Toyota Avanza": {"price": 400000, "stock": 8},
    "Kijang Innova": {"price": 750000, "stock": 5},
    "Honda Mobilio": {"price": 650000, "stock": 5},
    "Toyota Alphard": {"price": 1500000, "stock": 2},
}

reservation_list = [
    {
        'booking_id': 'UR001',
        'name': 'Ahmad Al-Farouq',
        'unit': 'Mitsubishi Expander',
        'start_date': '18-07-2025',
        'finish_date': '20-07-2025',
        'payment_status': 'Paid'
    },
    {
        'booking_id': 'UR002',
        'name': 'Katharina Edelweis',
        'unit': 'Toyota Fortuner',
        'start_date': '19-07-2025',
        'finish_date': '30-07-2025',
        'payment_status': 'Unpaid'
    },
    {
        'booking_id': 'UR003',
        'name': 'Siti Nurhaliza',
        'unit': 'Pajero Sport',
        'start_date': '19-07-2025',
        'finish_date': '29-07-2025',
        'payment_status': 'Paid'
    },
    {
        'booking_id': 'UR004',
        'name': 'Kenzo Takahashi',
        'unit': 'Hyundai Creta',
        'start_date': '20-07-2025',
        'finish_date': '31-07-2025',
        'payment_status': 'Paid'
    },
    {
        'booking_id': 'UR005',
        'name': 'Indah Permata Sari',
        'unit': 'Suzuki Ertiga',
        'start_date': '20-07-2025',
        'finish_date': '27-07-2025',
        'payment_status': 'Unpaid'
    }
]

# menu 1:
def get_today():
    today = datetime.today()
    day = today.strftime('%A')
    month = today.strftime('%B')
    date = today.day
    year = today.year

    def suffix(d):
        return 'th' if 11 <= d <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')

    return f"{day}, {month} {date}{suffix(date)} {year}"

def car_available():
    print("====== URESS Car Rental =====")
    print("\n🚘 Car Available for", get_today())
    headers = ["Car Name", "Price (Rp/day)", "Stock"]
    table = [
        [car, f"Rp {info['price']:,}", info['stock']]
        for car, info in car_stock.items()
    ]
    print(tabulate(table, headers=headers, tablefmt="grid", colalign=("left", "right", "center")))

# menu 2 :
def is_available(unit_name, new_start, new_end):
    new_start = datetime.strptime(new_start, "%d-%m-%Y")
    new_end = datetime.strptime(new_end, "%d-%m-%Y")
    count = 0
    for rsvp in reservation_list:
        if rsvp['unit'] == unit_name:
            existing_start = datetime.strptime(rsvp['start_date'], "%d-%m-%Y")
            existing_end = datetime.strptime(rsvp['finish_date'], "%d-%m-%Y")
            if new_start <= existing_end and new_end >= existing_start:
                count += 1
    return count < car_stock[unit_name]['stock']

def reservation():
    print("\n=== Make a Reservation ===")

    # Booking ID otomatis
    next_id = max([int(r['booking_id'][2:]) for r in reservation_list], default=0) + 1
    booking_id = f"UR{next_id:03}"

    name = input("Full name: ").strip().title()
    gender = input("Gender (M/F): ").strip().upper()
    id_type = input("ID type (KTP/Passport): ").strip().upper()
    id_number = input("ID number: ").strip()

    car_available()
    car_input = input("Enter the car name you want to rent: ").strip()

    # Case-insensitive car name check
    car_choice = None
    for car in car_stock:
        if car.lower() == car_input.lower():
            car_choice = car
            break

    if not car_choice:
        print("❌ Car not found in stock.")
        return

    try:
        rent_days = int(input("How many days do you want to rent? "))
        if rent_days <= 0:
            print("❌ Rental days must be at least 1.")
            return
    except ValueError:
        print("⚠️ Invalid number of days.")
        return

    start_date_input = input("Enter rental start date (DD-MM-YYYY): ")
    try:
        start_date = datetime.strptime(start_date_input, "%d-%m-%Y")
        finish_date = start_date + timedelta(days=rent_days - 1)
        start_date_str = start_date.strftime("%d-%m-%Y")
        finish_date_str = finish_date.strftime("%d-%m-%Y")
    except ValueError:
        print("⚠️ Invalid date format.")
        return

    if not is_available(car_choice, start_date_str, finish_date_str):
        print("❌ Sorry, the selected car is already booked on those dates.")
        return

    daily_price = car_stock[car_choice]["price"]
    subtotal = daily_price * rent_days
    discount = 0.05 * subtotal if rent_days >= 7 else 0
    total = subtotal - discount

    # Tambah ke data reservasi
    reservation_list.append({
        'booking_id': booking_id,
        'name': name,
        'unit': car_choice,
        'start_date': start_date_str,
        'finish_date': finish_date_str,
        'payment_status': 'Unpaid'
    })

    headers = ["Booking ID", "Name", "Gender", "ID Type", "ID Number", "Car", "Days", "Daily Price", "Discount", "Total", "Start", "Finish"]
    data = [[
        booking_id, name, gender, id_type, id_number, car_choice, rent_days,
        f"Rp {daily_price:,.0f}", f"Rp {discount:,.0f}", f"Rp {total:,.0f}",
        start_date_str, finish_date_str
    ]]
    print("\n✅ Reservation Summary:")
    print(tabulate(data, headers=headers, tablefmt="grid"))

# menu 3:
def reservation_new_update():
    print("\n=== Reservation List ===")
    headers = ['Booking ID', 'Name', 'Unit', 'Start Date', 'Finish Date', 'Rent Days', 'Payment Status']
    table = []

    for rsvp in reservation_list:
        start = datetime.strptime(rsvp['start_date'], "%d-%m-%Y")
        finish = datetime.strptime(rsvp['finish_date'], "%d-%m-%Y")
        rent_days = (finish - start).days + 1
        table.append([
            rsvp['booking_id'], rsvp['name'], rsvp['unit'],
            rsvp['start_date'], rsvp['finish_date'], rent_days,
            rsvp['payment_status']
        ])

    print(tabulate(table, headers=headers, tablefmt="grid"))

# menu 4:
def reservation_edit():
    booking_id = input("Enter Booking ID to edit: ").strip().upper()

    for rsv in reservation_list:
        if rsv['booking_id'] == booking_id:
            print("\nCurrent Reservation Info:")
            print(f"Name        : {rsv['name']}")
            print(f"Start Date  : {rsv['start_date']}")
            print(f"Finish Date : {rsv['finish_date']}")
            print(f"Unit        : {rsv['unit']}")

            new_name = input("New Name (press Enter to keep current): ").strip().title()
            new_start = input("New Start Date (dd-mm-yyyy) (press Enter to keep current): ").strip()
            new_days = input("New Rent Days (press Enter to keep current): ").strip()
            new_unit = input("New Unit (press Enter to keep current): ").strip().title()
            if new_unit and new_unit not in car_stock:
                print("❌ Car not found in stock.")
                return

            if new_name:
                rsv['name'] = new_name
            if new_unit:
                rsv['unit'] = new_unit
            if new_start:
                rsv['start_date'] = new_start
                if new_days:
                    start_obj = datetime.strptime(new_start, "%d-%m-%Y")
                    finish_obj = start_obj + timedelta(days=int(new_days) - 1)
                    rsv['finish_date'] = finish_obj.strftime("%d-%m-%Y")
            elif new_days:
                    start_obj = datetime.strptime(rsv['start_date'], "%d-%m-%Y")
                    finish_obj = start_obj + timedelta(days=int(new_days) - 1)
                    rsv['finish_date'] = finish_obj.strftime("%d-%m-%Y")

            print("✅ Reservation updated successfully!")
            return

    print("❌ Booking ID not found.")

# menu 5:
def reservation_cancel():
    print("\n=== Cancel Reservation ===")
    booking_id = input("Booking ID: ").strip().upper()

    for i, rsvp in enumerate(reservation_list):
        if rsvp["booking_id"] == booking_id:
            confirm = input(f"Are you sure to cancel reservation for {rsvp['name']} (Y/N)? ").upper()
            if confirm == "Y":
                del reservation_list[i]
                print("✅ Reservation cancelled successfully!")
            else:
                print("❌ Cancellation aborted.")
            return

    print("❌ Booking ID not found.")

# menu 7:
def promotion():
        print("\n========================================")
        print("Apply 5% discount for rentals >= 7 days")
        print("========================================\n")

# menu 6:
def payment():
    print("\n=== Payment Menu ===")
    booking_id = input("Enter Booking ID: ").strip().upper()

    for rsvp in reservation_list:
        if rsvp["booking_id"] == booking_id:
            start = datetime.strptime(rsvp["start_date"], "%d-%m-%Y")
            finish = datetime.strptime(rsvp["finish_date"], "%d-%m-%Y")
            rent_days = (finish - start).days + 1
            unit = rsvp["unit"]
            price_per_day = car_stock[unit]["price"]
            total_price = rent_days * price_per_day

            print(f"\nName       : {rsvp['name']}")
            print(f"Car        : {unit}")
            print(f"Rent Days  : {rent_days} day(s)")
            print(f"Daily Rate : Rp{price_per_day:,}")

            discount = 0
            if rent_days >= 7:
                promotion()
                discount = 0.05 * total_price
                total_price -= discount
                print(f"Discount   : Rp{int(discount):,}")

            print(f"Total Pay  : Rp{int(total_price):,}")

            while True:
                try:
                    paid = int(input("Enter payment amount (Rp): "))
                    if paid < total_price:
                        print(f"❌ Insufficient. You still owe Rp{int(total_price - paid):,}")
                    elif paid > total_price:
                        rsvp["payment_status"] = "Paid"
                        print(f"✅ Payment successful. Change: Rp{int(paid - total_price):,}")
                        break
                    else:
                        rsvp["payment_status"] = "Paid"
                        print("✅ Payment successful. No change.")
                        break
                except ValueError:
                    print("⚠️ Invalid amount. Please enter a number.")
            return

    print("❌ Booking ID not found.")


# === Menu Utama ===
def main_menu():
    while True:
        print("\n=== Welcome to URESS Car Rental ===")
        print("\n🚗 === CAR RENTAL MENU ===")
        print("1. Show Available Cars")
        print("2. Make a Reservation")
        print("3. View Reservations")
        print("4. Edit Reservation")
        print("5. Cancel Reservation")
        print("6. Make Payment")
        print("7. Promotions")
        print("8. Exit")
        choice = input("Choose menu (1-8): ")

        if choice == "1":
            car_available()
        elif choice == "2":
            reservation()
        elif choice == "3":
            reservation_new_update()
        elif choice == "4":
            reservation_edit()
        elif choice == "5":
            reservation_cancel()
        elif choice == "6":
            payment()
        elif choice == "7":
            promotion()
        elif choice == "8":
            print("👋 Thank you for using our service!")
            break
        else:
            print("⚠️ Invalid choice. Please choose 1-7.")

main_menu()
