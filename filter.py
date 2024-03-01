import re
import sys

from glob import glob
from collections import defaultdict
from filter_intersection import filter_intersection
from checkers import bs_checker

if __name__ == "__main__":
    # folder_path = sys.argv[1]
    folder_path = "html/"
    filenames = glob(folder_path + "*.json")
    
    # Set for ended filenames in dataset 
    good_filenames = set()
    
    # For app_example.com_86.json group name is app_example.com
    filename_groups = defaultdict(list)
    
    for filename in filenames:
        group_name = re.search(r'.*(?=_)', filename)
        filename_groups[group_name[0]].append(filename)
    
    # Intersection filtration stage
    before = 0
    after = 0
    for group_name in filename_groups.keys():
        
        before += len(filename_groups[group_name])
        try:
            a = filter_intersection(filename_groups[group_name])
            good_filenames = good_filenames.union(a)
            after += len(a)
        except Exception:
            print(group_name)
        
        
    
    print(f"Was filtered (intersection): {before - after}")
    print(f"After filtration (intersection) : {after}")

    # BS soup checker stage
    before = 0
    after = 0
    to_filter = good_filenames.copy()
    for filename in to_filter:
        before += 1
        after += 1
        if not bs_checker(filename) :
            good_filenames.remove(filename)
            after -= 1
        
    
    print(f"Was filtered (BS checker): {before - after}")
    print(f"After filtration (BS checker) : {after}")
