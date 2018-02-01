from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime

from database import *

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

#Create User
'''User1 = User(name="Cristiana Costa", email="cristianacmc@gmail.com",
             picture='https://lh6.googleusercontent.com/-ugZkUxkqwbc/AAAAAAAAAAI/AAAAAAAAAcw/-SnX5O_Ng3s/photo.jpg')
session.add(User1)
session.commit()'''


# Catalog for Soccer
soccer = Category(name="Soccer")
session.add(soccer)
session.commit()


# Catalog for Basketball
basketball = Category(name="Basketball")
session.add(basketball)
session.commit()

# Catalog for Baseball
baseball = Category(name="Baseball")
session.add(baseball)
session.commit()

# Catalog for Frisbee
frisbee = Category(name="Frisbee")
session.add(frisbee)
session.commit()

# Catalog for Snowboarding
snowboarding = Category(name="Snowboarding")
session.add(snowboarding)
session.commit()

# Catalog for Rock Climbing
climbing = Category(name="Rock Climbing")
session.add(climbing)
session.commit()

# Catalog for Foosball
foosball = Category(name="Foosball")
session.add(foosball)
session.commit()

# Catalog for Skating
skating = Category(name="Skating")
session.add(skating)
session.commit()

'''categoryitem1 = CategoryItem( user_id=1, name="Outdoor Skates",
							  description ="These skates are simply meant for the outdoors. Outdoor skates come in either low top or high top boots and the wheels are specifically designed to skate outdoors where the ground is not as smooth.",
							  date = datetime.datetime.now(),
							  category = skating)

session.add(categoryitem1)
session.commit()

categoryitem2 = CategoryItem( user_id=1, name="Indoor Skates",
							  description="These are traditional style skates that are for those wanting to skate in a skating rink, artistically dance, and those that want to rhythm skate.",
					          date = datetime.datetime.now(),
					          category = skating)

session.add(categoryitem2)
session.commit()


# Catalog for Hockey
category1 = Category(name="Hockey")

session.add(category1)
session.commit()

categoryitem1 = CategoryItem( user_id=1, name="Bandy", 
	                          description="Bandy is played with a ball on a football pitch-sized ice arena (bandy rink), typically outdoors, and with many rules similar to association football.",
					          date = datetime.datetime.now(),
					          category = climbing)

session.add(categoryitem1)
session.commit()'''

print "added menu items!"