import os
import pandas as pd

class DataExtractor:
    def __init__(self, files, excluded_list):
        self.files = files
        self.valid_files = []
        for file in files:
            if os.path.exists(file):
                self.valid_files.append(file)
        self.young_person_file = excluded_list

    def reader(self):
        file_list = []
        for file in self.valid_files:
            file_base_name = os.path.splitext(file)[0]
            specific_file_name = f'{file_base_name}.csv'
            try:
                df = pd.read_csv(file)[['staff','client', 'sched start', 'sched end', 'clocked start']]
                df.drop_duplicates(inplace=True)
                df.to_csv(specific_file_name, index=False)
                file_list.append(specific_file_name)
                print(f'File successfully saved: {specific_file_name}')
            except Exception as e:
                print(f'Failed to process file: {file}. Error: {e}')
        return file_list

    def filter(self):
        young_persons = []
        filtered_file_list = []
        with open(self.young_person_file, 'r') as yp_file:
            for line in yp_file:
                young_persons.append(line.strip())

        # Read the CSV file once
        for file in self.valid_files:
            df = pd.read_csv(file)
            file_base_name = os.path.splitext(file)[0]
            specific_file_name = f'{file_base_name}_filtered.csv'

            # Filter and sort data
            filtered_df = df[~df['client'].isin(young_persons)]
            sorted_df = filtered_df.sort_values(by='staff')

            # Save filtered data to CSV
            try:
                sorted_df.to_csv(specific_file_name, index=False)
                filtered_file_list.append(specific_file_name)
                sorted_df.to_csv(specific_file_name, index=False)
                print(f'Filtered file successfully saved: {specific_file_name}')
            except Exception as e:
                print(f'Failed to process file: {file}. Error: {e}')

        return filtered_file_list

    # Display all young persons
    def get_excluded_list(self):
        with open(self.young_person_file, 'r') as yp_file:
            return [name.strip() for name in yp_file.readlines()]

    # Add a young person to the young person file
    def add_young_person(self, name):
        young_persons = self.get_young_persons()
        young_persons.append(name)
        self._save_file(young_persons)
        return young_persons

    # Delete a young person from the list
    def delete_young_person(self, name):
        try:
            young_persons = self.get_young_persons()
            young_persons_set = set(young_persons)
            young_persons_set.remove(name)
            updated_young_persons = list(young_persons_set)
            self._save_file(updated_young_persons)
            return updated_young_persons
        except KeyError:
            print(f"Young person {name}' does not exist in the list.")
        return young_persons

    # Save changes to the young person file
    def _save_file(self, young_persons):
        with open(self.young_person_file, 'w') as yp_file:
            for name in young_persons:
                yp_file.write(f'{name}\n')


