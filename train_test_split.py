from collections import defaultdict


if (True):
        similar_data = []
        filename_groups = defaultdict(list)
        
        for filename in good_filenames:
            group_name = re.search(r'.*(?=_)', filename)
            filename_groups[group_name[0]].append(filename)
        
        all_pages = 0
        
        for first_domain in filename_groups.keys():
            for second_domain in filename_groups.keys():
            
                first_domain_len = len(filename_groups[first_domain])
                all_pages += first_domain_len
                second_domain_len = len(filename_groups[second_domain])
            
                similar_data.append((similar(first_domain, second_domain),
                                    first_domain_len + second_domain_len,
                                    first_domain, second_domain))
        
        max_similar = 0.8
        similar_data = list(filter(lambda x : 1.0 > x[0] > max_similar, similar_data))
        similar_data = sorted(similar_data)[::2]