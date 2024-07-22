#!/usr/bin/env python3

import sys, re, operator, csv

users = {}
errors_type = {}

# regex pattern level info for group/index 1, message for group/index 2, 
# ticket number for group/index 3, and username for group/index 4 
pattern = r"ticky: (ERROR|INFO) ([\w ]*) ?(\[[#\d]{5}\])? ?\((.*)\)"

with open(sys.argv[1]) as f:
    for line in f.readlines():

        result = re.search(pattern, line)

        if result is None:
            continue
        
        # extract the grouping result
        level = result[1]
        message = result[2]
        username = result[4]

        if level not in ['INFO', 'ERROR']:
            continue

        if username not in users:
            users[username] = {'INFO': 0, 'ERROR': 0}

        users[username][level] += 1

        if level == 'ERROR':
            errors_type[message] = errors_type.get(message, 0) + 1

# sort the result
sorted_errors_type = sorted(errors_type.items(), key=operator.itemgetter(1), reverse=True)
sorted_users = sorted(users.items(), key=operator.itemgetter(0))

# writing users dict to csv
user_keys = ['Username', 'INFO', 'ERROR']

## transform users data
transformed_users = []
for username, user_level_counts in sorted_users:
    row = { 'Username': username }
    row.update(user_level_counts)
    transformed_users.append(row)

## write users to csv
with open('user_statistics.csv', 'w') as user_stat:
    writer = csv.DictWriter(user_stat, fieldnames=user_keys)
    writer.writeheader()
    writer.writerows(transformed_users)

# writing errors dict to csv
error_keys = ['Error', 'Count']

## transform errors data
transformed_errors = [{'Error': error_type, 'Count': count} for error_type, count in sorted_errors_type]

## write errors_type to csv
with open('error_message.csv', 'w') as error_msg:
    writer = csv.DictWriter(error_msg, fieldnames=error_keys)
    writer.writeheader()
    writer.writerows(transformed_errors)
