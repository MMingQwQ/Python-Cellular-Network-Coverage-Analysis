# COMP348 A2
# Student Name: Mingming Zhang
# Student ID: 40258080

import json
import sys
import random

def load_json(file_path):
    # Load the JSON data 
    with open(file_path, 'r') as file:
        return json.load(file)

def calculate_global_statistics(data):
    base_stations = data['baseStations']
    total_base_stations = len(base_stations)  
    total_antennas = sum(len(bs['ants']) for bs in base_stations)  
    antenna_counts = [len(bs['ants']) for bs in base_stations]  
    max_antennas = max(antenna_counts)  
    min_antennas = min(antenna_counts) 
    avg_antennas = total_antennas / total_base_stations  
    
    all_points = {}  # Dictionary to store all covered points
    antenna_point_counts = {}  # Dictionary to count points covered by each antenna
    
    # Iterate over each base station and antenna to populate all_points and antenna_point_counts
    for bs in base_stations:
        for ant in bs['ants']:
            antenna_point_counts[(bs['id'], ant['id'])] = len(ant['pts'])  
            for point in ant['pts']:
                point_key = (point[0], point[1])
                if point_key in all_points:
                    all_points[point_key].append((bs['id'], ant['id'], point[2]))
                else:
                    all_points[point_key] = [(bs['id'], ant['id'], point[2])]
    
    # Count points covered by exactly one antenna and by more than one antenna
    points_covered_by_exactly_one_antenna = sum(1 for point in all_points.values() if len(point) == 1)
    points_covered_by_more_than_one_antenna = sum(1 for point in all_points.values() if len(point) > 1)
    
    # Calculate total grid points
    lat_steps = round((data['max_lat'] - data['min_lat']) / data['step']) + 1
    lon_steps = round((data['max_lon'] - data['min_lon']) / data['step']) + 1
    total_points = lat_steps * lon_steps
    
    # Calculate points not covered by any antenna
    points_not_covered = total_points - points_covered_by_exactly_one_antenna - points_covered_by_more_than_one_antenna
    
    # Calculate the percentage of the covered area
    percentage_covered_area = (points_covered_by_exactly_one_antenna + points_covered_by_more_than_one_antenna) / total_points * 100
    
    # Calculate total coverage instances and average antennas covering a point
    total_coverage_instances = sum(len(point) for point in all_points.values())
    avg_antennas_cover_point = total_coverage_instances / len(all_points)  

    # Find the point with the maximum number of antennas covering it
    max_antennas_cover_point = max(len(point) for point in all_points.values())
    max_covered_point = max(antenna_point_counts.items(), key=lambda x: x[1])
    max_covered_base_station, max_covered_antenna = max_covered_point[0]
    
    # Return the calculated statistics
    return {
        'total_base_stations': total_base_stations,
        'total_antennas': total_antennas,
        'max_antennas': max_antennas,
        'min_antennas': min_antennas,
        'avg_antennas': avg_antennas,
        'points_covered_by_one': points_covered_by_exactly_one_antenna,
        'points_covered_by_multiple': points_covered_by_more_than_one_antenna,
        'points_not_covered': points_not_covered,
        'max_antennas_cover_point': max_antennas_cover_point,
        'avg_antennas_cover_point': avg_antennas_cover_point,
        'percentage_covered_area': percentage_covered_area,
        'max_covered_base_station': max_covered_base_station,
        'max_covered_antenna': max_covered_antenna,
        'total_points': total_points,
        'total_covered_points': points_covered_by_exactly_one_antenna + points_covered_by_more_than_one_antenna,
        'total_coverage_instances': total_coverage_instances
    }

def display_global_statistics(statistics):
    # Display global statistics
    print(f"\n➤ The total number of base stations = {statistics['total_base_stations']}")
    print(f"➤ The total number of antennas = {statistics['total_antennas']}")
    print(f"➤ The max, min and average of antennas per BS = {statistics['max_antennas']}, {statistics['min_antennas']}, {statistics['avg_antennas']:.1f}")
    print(f"➤ The total number of points covered by exactly one antenna = {statistics['points_covered_by_one']}")
    print(f"➤ The total number of points covered by more than one antenna = {statistics['points_covered_by_multiple']}")
    print(f"➤ The total number of points not covered by any antenna = {statistics['points_not_covered']}")
    print(f"➤ The maximum number of antennas that cover one point = {statistics['max_antennas_cover_point']}")
    print(f"➤ The average number of antennas covering a point = {statistics['avg_antennas_cover_point']:.1f}")
    print(f"➤ The percentage of the covered area = 100 * {statistics['total_covered_points']} / {statistics['total_points']} = {statistics['percentage_covered_area']:.2f}%")
    print(f"➤ The id of the base station and antenna covering the maximum number of points = base station {statistics['max_covered_base_station']}, antenna {statistics['max_covered_antenna']}")

def display_base_station_statistics(data, base_station_id):
    # Find the base station with the specified ID
    base_station = None
    for bs in data['baseStations']:
        if bs['id'] == base_station_id:
            base_station = bs
            break
    
    if not base_station:
        print(f"No base station found with ID {base_station_id}")
        return
    
    total_antennas = len(base_station['ants'])  # Total number of antennas in this base station
    all_points = {}  # Dictionary to store all covered points
    antenna_point_counts = {}  # Dictionary to count points covered by each antenna
    
    # Iterate over each antenna to populate all_points and antenna_point_counts
    for ant in base_station['ants']:
        antenna_point_counts[ant['id']] = len(ant['pts'])  # Count of points covered by this antenna
        for point in ant['pts']:
            point_key = (point[0], point[1])
            if point_key in all_points:
                all_points[point_key].append((base_station['id'], ant['id'], point[2]))
            else:
                all_points[point_key] = [(base_station['id'], ant['id'], point[2])]
    
    # Count points covered by exactly one antenna and by more than one antenna
    points_covered_by_exactly_one_antenna = sum(1 for point in all_points.values() if len(point) == 1)
    points_covered_by_more_than_one_antenna = sum(1 for point in all_points.values() if len(point) > 1)
    
    # Calculate total grid points
    lat_steps = round((data['max_lat'] - data['min_lat']) / data['step']) + 1
    lon_steps = round((data['max_lon'] - data['min_lon']) / data['step']) + 1
    total_points = lat_steps * lon_steps
    
    # Calculate points not covered by any antenna
    points_not_covered = total_points - points_covered_by_exactly_one_antenna - points_covered_by_more_than_one_antenna
    percentage_covered_area = ((points_covered_by_exactly_one_antenna + points_covered_by_more_than_one_antenna) / total_points) * 100
    max_antennas_cover_point = max(len(point) for point in all_points.values())
    avg_antennas_cover_point = sum(len(point) for point in all_points.values()) / len(all_points)  

    max_covered_antenna = max(antenna_point_counts.items(), key=lambda x: x[1])[0]
    
    # Display statistics for the base station
    print(f"\n➤ Base Station ID = {base_station_id}")
    print(f"➤ The total number of antennas = {total_antennas}")
    print(f"➤ The total number of points covered by exactly one antenna = {points_covered_by_exactly_one_antenna}")
    print(f"➤ The total number of points covered by more than one antenna = {points_covered_by_more_than_one_antenna}")
    print(f"➤ The total number of points not covered by any antenna = {points_not_covered}")
    print(f"➤ The maximum number of antennas that cover one point = {max_antennas_cover_point}")
    print(f"➤ The average number of antennas covering a point = {avg_antennas_cover_point:.1f}")
    print(f"➤ The percentage of the covered area = 100 * {points_covered_by_exactly_one_antenna + points_covered_by_more_than_one_antenna} / {total_points} = {percentage_covered_area:.2f}%")
    print(f"➤ The id of the antenna covering the maximum number of points = antenna {max_covered_antenna}")

def check_coverage(data, lat, lon):
    # Dictionary to store all covered points
    all_points = {}
    
    # Iterate over each base station and antenna to populate all_points
    for bs in data['baseStations']:
        for ant in bs['ants']:
            for point in ant['pts']:
                point_key = (point[0], point[1])
                if point_key in all_points:
                    all_points[point_key].append((bs['id'], ant['id'], point[2]))
                else:
                    all_points[point_key] = [(bs['id'], ant['id'], point[2])]
    
    point_key = (lat, lon)
    if point_key in all_points:
        print(f"The point ({lat}, {lon}) is covered by the following base stations and antennas:")
        for bs_id, ant_id, power in all_points[point_key]:
            print(f"Base Station ID: {bs_id}, Antenna ID: {ant_id}, Power: {power}")
    else:
        print(f"The point ({lat}, {lon}) is not covered by any antenna.")
        # Find the nearest point
        min_distance = float('inf')
        nearest_bs = None
        nearest_ant = None
        nearest_coord = None  
        for bs in data['baseStations']:
            for ant in bs['ants']:
                for point in ant['pts']:
                    distance = (point[0] - lat) ** 2 + (point[1] - lon) ** 2
                    if distance < min_distance:
                        min_distance = distance
                        nearest_bs = bs['id']
                        nearest_ant = ant['id']
                        nearest_coord = (point[0], point[1])
        print(f"The nearest antenna is at Base Station ID: {nearest_bs}, Antenna ID: {nearest_ant}, Coordinates: {nearest_coord}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 <your_code.py> <test_file.json>")
        return
    
    json_file_path = sys.argv[1]
    data = load_json(json_file_path)
    
    statistics = calculate_global_statistics(data)
    
    while True:
        print("\nChoose an option:")
        print("1. Display Global Statistics")
        print("2. Display Base Station Statistics")
        print("  2.1. Statistics for a random station")
        print("  2.2. Choose a station by Id.")
        print("3. Check Coverage")
        print("4. Exit")
        
        choice = input("\nEnter your choice: ")
        
        if choice == '1':
            display_global_statistics(statistics)
        elif choice == '2.1':
            random_bs_id = random.choice([bs['id'] for bs in data['baseStations']])
            display_base_station_statistics(data, random_bs_id)
        elif choice == '2.2':
            try:
                bs_id = int(input("Enter the base station ID: "))
                display_base_station_statistics(data, bs_id)
            except ValueError:
                print("Invalid input. Please enter a valid base station ID.")
        elif choice == '3':
            try:
                lat = float(input("Enter the latitude: "))
                lon = float(input("Enter the longitude: "))
                check_coverage(data, lat, lon)
            except ValueError:
                print("Invalid input. Please enter valid coordinates.")
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

    """
    # summary for sample average
    For global:
    Base station 1, antenna 1 covers 4 points.
    Base station 1, antenna 2 covers 5 points.
    Base station 2, antenna 3 covers 4 points.
    Total coverage instances = 4 (Antenna 1) + 5 (Antenna 2) + 4 (Antenna 3) = 13 
    Unique points covered: 10 (7 unique +3)
    Average = 13/10 = 1.3

    Base station 1:
    Total coverage instances = 4 (Antenna 1) + 5 (Antenna 2) = 9
    Total unique covered points by Base Station 1 = 7 (since (45.01, -73.02) and (45.02, -73.02) appear multiple times, they are counted once)
    Average = 9/7 = 1.3
    
    Base station 2:
    Total coverage instances = 4 (Antenna 3) = 4
    Total unique covered points by Base Station 2 = 4
    Average = 4/4 = 1
    """
