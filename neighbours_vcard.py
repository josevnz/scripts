#!/usr/bin/env python3
"""
Neighbours CSV to VCard converter - Because is a pain to add 45+ addresses by hand to your Iphone.
I took a few liberties how to add the data together. Check the code for details
Author: Jose Vicente Nunez
License: GPL3
"""
import sys
import csv
import os
import vobject

def read_csv(csvfile):
    """
    Read a CSV file into Python objects
    :param csvfile CSV File to read
    """
    common = {}
    people_with_phone = {}
    with open(csvfile, 'r') as csvfh:
        c_reader = csv.DictReader(csvfh, dialect='excel')
        for row in c_reader:
            street = "{} Walmsley Road".format(row['Address'].strip())
            if street not in common:
                common[street] = {}
            if row['Kids'] != '':
                if 'Kids' not in common[street]:
                    common[street]['Kids'] = []
                common[street]['Kids'].append(row['Kids'])
            if row['Pets'] != '':
                if 'Pets' not in common[street]:
                    common[street]['Pets'] = []
                common[street]['Pets'].append(row['Pets'])
            if row['Moved here'] is not None and row['Moved here'] != '':
                common[street]['Moved here'] = row['Moved here']
            last_name = row['Last']
            if last_name is not None and last_name != '':
                if street not in people_with_phone:
                    people_with_phone[street] = []
                person_details = {}
                if row['Phone'] != '':
                    person_details['Phone'] = row['Phone']
                if row['Type'] != '':
                    person_details['Phone type'] = row['Type']
                if row['Email'] != '':
                    person_details['Email'] = row['Email']
                if row['First'] != '':
                    person_details['First'] = row['First']
                person_details['Last'] = last_name
                people_with_phone[street].append(person_details)
    return people_with_phone, common

def create_vcards(persons, cmn):
    """
    :param persons Persons map
    :param common Common attributes map
    """
    vcards = []
    for address in persons:
        for person in persons[address]:
            # Main contact information
            neighbour_card = vobject.vCard()
            neighbour_card.add('adr').value = vobject.vcard.Address(
                street=address,
                city='Darien',
                region='CT',
                code='06820',
                country='United States'
                )
            neighbour_card.adr.type_param = ['HOME', 'pref']
            neighbour_card.add('fn').value = "{} {}".format(person['First'], person['Last'])
            neighbour_card.add('n').value = vobject.vcard.Name(
                family=person['Last'], given=person['First']
                )
            if 'Email' in person:
                neighbour_card.add('email').value = person['Email']
                neighbour_card.email.type_param = ['INTERNET', 'pref']
            if 'Phone' in person:
                neighbour_card.add('tel').value = person['Phone']
                neighbour_card.tel.type_param = [person['Phone type'].upper(), 'VOICE', 'pref']
            neighbour_card.serialize()
            # Optional information, added in notes
            notes = []
            if 'Kids' in cmn[address]:
                kids = ", ".join(cmn[address]['Kids'])
                notes.append("Kids: {}".format(kids))
            if 'Pets' in cmn[address]:
                pets = ", ".join(cmn[address]['Pets'])
                notes.append("Pets: {}".format(pets))
            if 'Moved here' in cmn[address]:
                notes.append("Moved here: {}".format(cmn[address]['Moved here']))
            if notes:
                neighbour_card.add('notes')
                neighbour_card.notes.value = "\n".join(notes)
            vcards.append(neighbour_card)
    return vcards

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise ValueError("Please provide the path to the CSV file and the destination directory!")
    (PPHN, CMN) = read_csv(sys.argv[1])
    VCARDS = create_vcards(PPHN, CMN)
    FILE_NAME = "neighbours.vcf"
    DEST_FILE = os.path.join(sys.argv[2], FILE_NAME)
    with open(DEST_FILE, 'w') as vcard_file:
        for vcard in VCARDS:
            vcard_file.write(vcard.serialize())
            vcard_file.flush()
    print("Wrote {}".format(DEST_FILE))
    print("DONE writting VCARDS")
