from iss_tracker.iss_tracker import ISSTracker

if __name__ == '__main__':
    tracker = ISSTracker()
    print(f"{tracker.get_current_location_of_iss()}")
