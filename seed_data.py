from app import Group, db

db.create_all()

group1 = Group('G1', 'Trip to New York')
group2 = Group('G2', 'Weekend at SPA')
group3 = Group('G3', 'Weekend trip to Palanga')
group4 = Group('G4', 'Trip to Turkey')
group5 = Group('G5', 'Trip to Rome')
group6 = Group('G6', 'Dinner in Steakhouse')
group7 = Group('G7', 'Lunch in London grill')
group8 = Group('G8', 'Domino pizza')
group9 = Group('G9', 'Trip to Norway')
group10 = Group('G10', 'McDonalds')
group11 = Group('G11', 'Night out')
group12 = Group('G12', 'Bussiness trip')

db.session.add_all([group1, group2, group3, group4, group5, group6, group7, group8, group9, group10, group11, group12])
db.session.commit()

