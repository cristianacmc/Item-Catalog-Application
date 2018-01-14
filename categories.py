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


# Catalog for Soccer
category1 = Category(name="Soccer")

session.add(category1)
session.commit()


# Catalog for Basketball
category1 = Category(name="Basketball")

session.add(category1)
session.commit()

# Catalog for Baseball
category1 = Category(name="Baseball")

session.add(category1)
session.commit()

# Catalog for Frisbee
category1 = Category(name="Frisbee")

session.add(category1)
session.commit()

# Catalog for Snowboarding
category1 = Category(name="Snowboarding")

session.add(category1)
session.commit()

# Catalog for Rock Climbing
category1 = Category(name="Rock Climbing")

session.add(category1)
session.commit()

# Catalog for Foosball
category1 = Category(name="Foosball")

session.add(category1)
session.commit()

# Catalog for Skating
category1 = Category(name="Skating")

session.add(category1)
session.commit()

categoryitem1 = CategoryItem(name="Outdoor Skates",
							  description ="These skates are simply meant for the outdoors. Outdoor skates come in either low top or high top boots and the wheels are specifically designed to skate outdoors where the ground is not as smooth.",
							  create_date = datetime.datetime.now(),
							  category = category1)

session.add(categoryitem1)
session.commit()

categoryitem2 = CategoryItem(name="Indoor Skates",
							  description="These are traditional style skates that are for those wanting to skate in a skating rink, artistically dance, and those that want to rhythm skate.",
					          create_date = datetime.datetime.now(),
					          category = category1)

session.add(categoryitem2)
session.commit()


# Catalog for Hockey
category1 = Category(name="Hockey")

session.add(category1)
session.commit()

categoryitem1 = CategoryItem(name="Bandy", 
	                          description="Bandy is played with a ball on a football pitch-sized ice arena (bandy rink), typically outdoors, and with many rules similar to association football.",
					          create_date = datetime.datetime.now(),
					          category = category1)

session.add(categoryitem1)
session.commit()

print "added menu items!"