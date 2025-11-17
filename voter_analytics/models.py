# File: models.py
# Author: Anna LaPrade (alaprade@bu.edu), 10/28/2025
# Description: models for the voter_analytics app

from django.db import models

# Create your models here.

class Voter(models.Model):
    '''
    Store/represent data about a registered voter
    '''

    # id
    voter_id_number = models.CharField(unique=True)
    last_name = models.CharField()
    first_name = models.CharField()
    
    # address
    street_number = models.CharField()
    street_name = models.CharField()
    apartment_number = models.CharField(blank=True, null=True)
    zip_code = models.CharField()

    # birth date
    date_of_birth = models.DateField()
    
    # registration info
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=2)
    precinct_number = models.CharField()

    # participation in recent elections
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)

    # voter score
    voter_score = models.IntegerField()

    
    def __str__(self):
        '''return a string representation of this Voter.'''
        return f'{self.first_name} {self.last_name} ({self.party_affiliation}) – Precinct {self.precinct_number}'


def load_data():
    '''Function to load data records from CSV file into Django model instances.'''

    # very dangerious line
    Voter.objects.all().delete()

    filename = 'data/newton_voters.csv'
    f = open(filename)
    f.readline() # discard headers
 
    # read in those lines
    for line in f:
        fields = line.split(',')
       
        try:
            # create a new instance of Result object with this record from CSV
            voter = Voter(
                            # identification
                            voter_id_number=fields[0],
                            last_name=fields[1],
                            first_name=fields[2],

                            # address
                            street_number = fields[3],
                            street_name = fields[4],
                            apartment_number = fields[5] or None,
                            zip_code = fields[6],

                            # birth date
                            date_of_birth = fields[7],
 
                            # registration info
                            date_of_registration = fields[8],
                            party_affiliation = fields[9].strip(),
                            precinct_number = fields[10],
                        
                            # election info 
                            v20state = fields[11] in ['1', 'True', 'TRUE', 'true'],
                            v21town = fields[12] in ['1', 'True', 'TRUE', 'true'],
                            v21primary = fields[13] in ['1', 'True', 'TRUE', 'true'],
                            v22general = fields[14] in ['1', 'True', 'TRUE', 'true'],
                            v23town = fields[15] in ['1', 'True', 'TRUE', 'true'],
                            voter_score = fields[16]
                        )
        
 
 
            voter.save() # commit to database
            #print(f'Created result: {voter}')

        # print skipped feilds  
        except:
            print(f"Skipped: {fields}")
    
    print(f'Done. Created {len(Voter.objects.all())} Voters.')