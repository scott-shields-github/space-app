from launch_info import LaunchInfo, ImproperLaunchRequest, MissingLaunchData

launch_info_obj: LaunchInfo = LaunchInfo()

launch_info_obj.fetch_launch_data()


spacer: str = "========================="

print(f"{spacer}\nBad Fetch Request\n{spacer}\n")
try:
    launch_info_obj.get_next_launch(-1)
except ImproperLaunchRequest as e:
    print(e)

print(f"{spacer}\nFetch single Launch\n{spacer}\n")
print(launch_info_obj.get_formatted_launch_data(launch_info_obj.get_next_launch()[0]))

print(f"{spacer}\nFetch multiple launches\n{spacer}\n")
for launch in launch_info_obj.get_next_launch(5):
    print(launch_info_obj.get_formatted_launch_data(launch))




