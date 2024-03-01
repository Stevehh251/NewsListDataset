import re
import sys

from glob import glob
from collections import defaultdict
from filter_intersection import filter_intersection


if __name__ == "__main__":
    # folder_path = sys.argv[1]
    folder_path = "html/"
    filenames = glob(folder_path + "*.json")
    
    # For app_example.com_86.json group name is app_example.com
    filename_groups = defaultdict(list)
    
    for filename in filenames:
        group_name = re.search(r'.*(?=_)', filename)
        filename_groups[group_name[0]].append(filename)
     
    before = 0
    after = 0
    for group_name in filename_groups.keys():
        try:
            print(len(filename_groups[group_name]))
            a = filter_intersection(filename_groups[group_name])
        except Exception:
            print(group_name)
        after += len(a)
        before += len(filename_groups[group_name])
        
    
    print(f"Was filtered (intersection): {before - after}")
    print(f"After filtration (intersection) : {after}")
