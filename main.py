import argparse
from datetime import datetime
from plate_solver import solve_plate
from location_calculator import calculate_location

def main():
    parser = argparse.ArgumentParser(description="Celestial Navigation System")
    parser.add_argument("image_path", help="Path to the star image")
    parser.add_argument("--datetime", help="Observation date and time (ISO format)")
    args = parser.parse_args()

    if args.datetime:
        observation_time = datetime.fromisoformat(args.datetime)
    else:
        observation_time = datetime.now()

    print("Solving plate...")
    solved_data = solve_plate(args.image_path)

    print("Calculating location...")
    latitude, longitude = calculate_location(solved_data, observation_time)

    print(f"Estimated location: {latitude:.6f}°, {longitude:.6f}°")

if __name__ == "__main__":
    main()