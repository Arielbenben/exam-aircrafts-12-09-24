from service.api_service import write_cities_data_to_json
from service.mission_service import turn_on_create_missions


def menu():
    while True:
        print("\nMenu:")
        print("1. Load files from JSON")
        print("2. Display recommendation table")
        print("3. Save attacks to CSV")
        print("4. Exit")

        choice = input("Choose an option (1-4): ")

        if choice == '1':
            write_cities_data_to_json()
            print("Files loaded successfully.")
        elif choice == '2':
            print(turn_on_create_missions())
        # elif choice == '3':
        #     all_missions = missions()
        #     write_missions_to_csv(all_missions)
        #     print("Missions saved to CSV.")
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")