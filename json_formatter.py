import json
import sys

# formats the specified json file 
# (adds brackets and commas to the file if there is not, gets the value of old_key and make it to a value of new_key(cane see it in "out.json" file))
def main():
    try: 
        # contains the json data that specified key has
        json_data = []
        in_file = str(sys.argv[1])
        old_key = str(sys.argv[2])
        new_key = str(sys.argv[3])
        with open(in_file, 'r') as file:
            for obj in file:
                data = json.loads(obj)
                try:
                    value = data.pop(old_key)
                    json_data.append({new_key: value})
                except TypeError:
                    try:
                        for keys in data:
                            value = keys.pop(old_key)
                            json_data.append({new_key: value})
                    except KeyError:
                        pass
                except KeyError:
                    pass

        if not json_data:
            print('Error: The specified key \'' + old_key + '\' does not exist')
            exit(1)

        with open('out.json', 'w') as out_file:
            json.dump(json_data, out_file, indent=2)
            print('Formatted Json in \"out.json\" file')
    except IndexError:
        print('Usage: json_formatter.py [file_name] [old_key (case sensitive)] [new_key]')


if __name__ == '__main__':
    main()
