import csv
import time
from tqdm import tqdm
import random

us_head = ["user_id", "name", "age"]
users = []
names = ["Mario", "Francesco", "Lorenzo", "Gianni", "Franco", "Chiara", "Giulia", "Federica", "Francesca", "Simona", "Genoveffa", "Aurora", "Paolo", "Luca", "Sofia"]
surnames = ["Rossi", "Freschi", "Mini", "Cosottini", "Gironi", "Chiostrini", "Vanni", "Cappetti", "Casciaro",
            "Tinacci", "Casini", "Guzzesi", "Cherubini", "Guzzanti", "Moretti"]
for i in range(40):
    users.append([i, random.choice(names) + " " + random.choice(surnames), random.randint(16, 90)])

print(users)
monument_id = [random.randint(1, 222) for i in range(50)]
print(monument_id)
rating_head = ["user_id", "monument_id", "rating"]
user_ratings = [[us_id[0], random.choice(monument_id), random.randint(1, 10)] for us_id in users for i in range(5)]
print(user_ratings)
with open('users.csv', mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(us_head)
    # Write each data row
    for row in tqdm(users):
        writer.writerow(row)
        time.sleep(0.1)

print('Dataset created successfully!')
with open('data/user_ratings.csv', mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(rating_head)
    # Write each data row
    for row in tqdm(user_ratings):
        writer.writerow(row)
        time.sleep(0.1)

print('Dataset created successfully!')
