from sqlalchemy import Integer, ForeignKey, String, Column, create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy import inspect
from sqlite3 import Cursor
from MySQLdb import _mysql

metadata = MetaData(engine)
Base = declarative_base()   

# I THINK I NEED TO MANUALLY CREATE THE DATABASE CODEX IN ORDER TO DO THE FOLLOWING
# UPGRADE PIP >>>> INSTALL SQLALCHEMY >>>> INSTALL MYSQLCLIENT

# The following code represents the connection protocols to sqlalchemy and the class maps for all associated object groups

def init_sqlalchemy(data='mysql://root:magic202@localhost:3306/codex'):
    global engine
    engine = create_engine(data)
                            # , echo = True
    
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

class Crystal(Base):
    __tablename__ = 'crystal'

    id = Column('id', Integer, primary_key=True, nullable=False)
    crystal_name = Column(String(60))
    symbolism = Column(String(500))
    link = Column(String(100))

    astro_ref = relationship('Astro_Sign', secondary='astro_sign_map')
    chakra_ref = relationship('Chakra', secondary='chakra_map')
    element_ref = relationship('Element', secondary='element_map')
    herb_ref = relationship('Herb', secondary='herb_map')
    planetary_ref = relationship('Planet', secondary='planet_map')
    def __repr__(self):
        return "<Crystal('%s'')>" % (
        self.crystal_name)

class Astro_Sign(Base):
    __tablename__ = 'astro_sign'

    id = Column('id', Integer, primary_key=True, nullable=False)
    astro_sign = Column(String(60))
    associated_diety = Column(String(60))
    dates = Column(String(60))
    symbolism = Column(String(500))
    
    crystal_ref = relationship('Crystal', secondary='crystal_map')
    chakra_ref = relationship('Chakra', secondary='chakra_map')
    element_ref = relationship('Element', secondary='element_map')
    herb_ref = relationship('Herb', secondary='herb_map')
    planetary_ref = relationship('Planet', secondary='planet_map')
    def __repr__(self):
        return "<Astro_Sign('%s'')>" % (
        self.astro_sign)

class Attribute(Base):
    __tablename__ = 'attribute'

    id = Column('id', Integer, primary_key=True, nullable=False)
    attribute = Column(String(60))
    symbolism = Column(String(500))
    
    herb_ref = relationship('Herb', secondary='herb_map')
    def __repr__(self):
        return "<Attribute('%s'')>" % (
        self.attribute)

class Chakra(Base):
    __tablename__ = 'chakra'

    id = Column('id', Integer, primary_key=True, nullable=False)
    chakra = Column(String(60))
    sanskrit_name = Column(String(60))
    body_port = Column(String(60))
    earth_port = Column(String(60))
    symbolism = Column(String(500))
    
    astro_sign_ref = relationship('Astro_Sign', secondary='astro_map')
    crystal_ref = relationship('Crystal', secondary='crystal_map')
    element_ref = relationship('Element', secondary='element_map')
    herb_ref = relationship('Herb', secondary='herb_map')
    planetary_ref = relationship('Planet', secondary='planet_map')
    def __repr__(self):
        return "<Chakra('%s'')>" % (
        self.chakra)

class Element(Base):
    __tablename__ = 'element'

    id = Column('id', Integer, primary_key=True, nullable=False)
    element = Column(String(60))
    symbolism = Column(String(500))
    
    astro_sign_ref = relationship('Astro_Sign', secondary='astro_map')
    crystal_ref = relationship('Crystal', secondary='crystal_map')
    chakra_ref = relationship('Chakra', secondary='chakra_map')
    herb_ref = relationship('Herb', secondary='herb_map')
    planetary_ref = relationship('Planet', secondary='planet_map')
    def __repr__(self):
        return "<Element('%s'')>" % (
        self.element)

class Herb(Base):
    __tablename__ = 'herb'

    id = Column('id', Integer, primary_key=True, nullable=False)
    herb = Column(String(60))
    symbolism = Column(String(500))
    
    attribute_ref = relationship('Attribute', secondary='astro_map')
    astro_sign_ref = relationship('Astro_Sign', secondary='astro_map')
    crystal_ref = relationship('Crystal', secondary='crystal_map')
    chakra_ref = relationship('Chakra', secondary='chakra_map')
    element_ref = relationship('Element', secondary='element_map')
    planetary_ref = relationship('Planet', secondary='planet_map')
    def __repr__(self):
        return "<Herb('%s'')>" % (
        self.herb)

class Planet(Base):
    __tablename__ = 'planet'

    id = Column('id', Integer, primary_key=True, nullable=False)
    planet = Column(String(60))
    metal = Column(String(60))
    day = Column(String(60))
    symbolism = Column(String(500))
    
    astro_sign_ref = relationship('Astro_Sign', secondary='astro_map')
    crystal_ref = relationship('Crystal', secondary='crystal_map')
    chakra_ref = relationship('Chakra', secondary='chakra_map')
    element_ref = relationship('Element', secondary='element_map')
    herb_ref = relationship('Herb', secondary='herb_map')
    def __repr__(self):
        return "<planet('%s'')>" % (
        self.planet)






class Crystal_Map(Base):
    __tablename__ = 'crystal_map'

    id = Column(Integer, primary_key = True, nullable = False, autoincrement=True)
    crystal_id = Column(Integer, ForeignKey('crystal.id'), primary_key=True)

    astro_sign_id = Column(Integer, ForeignKey('astro_sign.id'), primary_key=True)
    chakra_id = Column(Integer, ForeignKey('chakra.id'), primary_key=True)
    element_id = Column(Integer, ForeignKey('element.id'), primary_key=True)
    herb_id = Column(Integer, ForeignKey('herb.id'), primary_key=True)
    planet_id = Column(Integer, ForeignKey('planet.id'), primary_key=True)
    
    
    crystal = relationship(Crystal, backref=backref("crystal_map"))
    chakra = relationship(Chakra, backref=backref("crystal_chakra_map"))
    astro_sign = relationship(Astro_Sign, backref=backref("crystal_astro_map"))
    element = relationship(Element, backref=backref("crystal_element_map"))
    herb = relationship(Herb, backref=backref("crystal_herb_map"))
    planet = relationship(Planet, backref=backref("crystal_planet_map"))
   
class Astro_Map(Base):
    __tablename__ = 'astro_map'

    id = Column(Integer, primary_key = True, nullable = False, autoincrement=True)
    astro_sign_id = Column(Integer, ForeignKey('astro_sign.id'), primary_key=True)

    crystal = Column(Integer, ForeignKey('crystal.id'), primary_key=True)
    chakra_id = Column(Integer, ForeignKey('chakra.id'), primary_key=True)
    element_id = Column(Integer, ForeignKey('element.id'), primary_key=True)
    herb_id = Column(Integer, ForeignKey('herb.id'), primary_key=True)
    planet_id = Column(Integer, ForeignKey('planet.id'), primary_key=True)
    
    astro = relationship(Astro_Sign, backref=backref("astro_map"))
    chakra = relationship(Chakra, backref=backref("astro_chakra_map"))
    crystal = relationship(Crystal, backref=backref("astro_crystal_map"))
    element = relationship(Element, backref=backref("crystal_element_map"))
    herb = relationship(Herb, backref=backref("crystal_herb_map"))
    planet = relationship(Planet, backref=backref("crystal_planet_map"))

class Attribute_Map(Base):
    __tablename__ = 'attribute_map'

    id = Column(Integer, primary_key = True, nullable = False, autoincrement=True)
    attribute_id = Column(Integer, ForeignKey('attribute.id'), primary_key=True)
    herb_id = Column(Integer, ForeignKey('herb.id'), primary_key=True)  

    attribute = relationship(Attribute, backref=backref("attribute_assoc"))
    herb = relationship(Herb, backref=backref("attribute_herb_assoc"))
   

class Chakra_Map(Base):
    __tablename__ = 'chakra_map'

    id = Column(Integer, primary_key = True, nullable = False, autoincrement=True)
    chakra_id = Column(Integer, ForeignKey('chakra.id'), primary_key=True)

    astro_sign_id = Column(Integer, ForeignKey('astro_sign.id'), primary_key=True)
    crystal_id = Column(Integer, ForeignKey('crystal.id'), primary_key=True)
    element_id = Column(Integer, ForeignKey('element.id'), primary_key=True)
    herb_id = Column(Integer, ForeignKey('herb.id'), primary_key=True)
    planet_id = Column(Integer, ForeignKey('planet.id'), primary_key=True)
    
    chakra = relationship(Chakra, backref=backref("chakra_map"))
    astro_sign = relationship(Astro_Sign, backref=backref("chakra_astro_map"))
    crystal = relationship(Crystal, backref=backref("chakra_crystal_map"))
    element = relationship(Element, backref=backref("chakra_element_map"))
    herb = relationship(Herb, backref=backref("chakra_herb_map"))
    planet = relationship(Planet, backref=backref("crystal_planet_map"))

class Element_Map(Base):
    __tablename__ = 'element_map'

    id = Column(Integer, primary_key = True, nullable = False, autoincrement=True)
    element_id = Column(Integer, ForeignKey('element.id'), primary_key=True)
    
    astro_sign_id = Column(Integer, ForeignKey('astro_sign.id'), primary_key=True)
    crystal_id = Column(Integer, ForeignKey('crystal.id'), primary_key=True)
    chakra_id = Column(Integer, ForeignKey('chakra.id'), primary_key=True)
    herb_id = Column(Integer, ForeignKey('herb.id'), primary_key=True)
    planet_id = Column(Integer, ForeignKey('planet.id'), primary_key=True)
    
    element = relationship(Element, backref=backref("element_map"))
    chakra = relationship(Chakra, backref=backref("element_chakra_map"))
    astro_sign = relationship(Astro_Sign, backref=backref("element_astro_map"))
    crystal = relationship(Crystal, backref=backref("element_crystal_map"))
    herb = relationship(Herb, backref=backref("element_herb_map"))
    planet = relationship(Planet, backref=backref("element_planet_map"))

class Herb_Map(Base):
    __tablename__ = 'herb_map'

    id = Column(Integer, primary_key = True, nullable = False, autoincrement=True)
    herb_id = Column(Integer, ForeignKey('herb.id'), primary_key=True)
    
    astro_sign_id = Column(Integer, ForeignKey('astro_sign.id'), primary_key=True)
    attribute_id = Column(Integer, ForeignKey('attribute.id'), primary_key=True)
    crystal_id = Column(Integer, ForeignKey('crystal.id'), primary_key=True)
    chakra_id = Column(Integer, ForeignKey('chakra.id'), primary_key=True)
    element_id = Column(Integer, ForeignKey('element.id'), primary_key=True)
    planet_id = Column(Integer, ForeignKey('planet.id'), primary_key=True)
    
    herb = relationship(Herb, backref=backref("herb_map"))
    attribute = relationship(Attribute, backref=backref("herb_attribute_map"))
    chakra = relationship(Chakra, backref=backref("herb_chakra_map"))
    astro_sign = relationship(Astro_Sign, backref=backref("herb_astro_map"))
    crystal = relationship(Crystal, backref=backref("herb_crystal_map"))
    element = relationship(Element, backref=backref("herb_element_map"))
    planet = relationship(Planet, backref=backref("herb_planet_map"))

class Planet_Map(Base):
    __tablename__ = 'planet_map'

    id = Column(Integer, primary_key = True, nullable = False, autoincrement=True)
    planet_id = Column(Integer, ForeignKey('planet.id'), primary_key=True)
    
    astro_sign_id = Column(Integer, ForeignKey('astro_sign.id'), primary_key=True)
    crystal_id = Column(Integer, ForeignKey('crystal.id'), primary_key=True)
    chakra_id = Column(Integer, ForeignKey('chakra.id'), primary_key=True)
    element_id = Column(Integer, ForeignKey('element.id'), primary_key=True)
    herb_id = Column(Integer, ForeignKey('herb.id'), primary_key=True)
    
    planet = relationship(Planet, backref=backref("planet_map"))
    chakra = relationship(Chakra, backref=backref("planet_chakra_map"))
    astro_sign = relationship(Astro_Sign, backref=backref("planet_astro_map"))
    crystal = relationship(Crystal, backref=backref("planet_crystal_map"))
    element = relationship(Element, backref=backref("planet_element_map"))
    herb = relationship(Herb, backref=backref("planet_herb_map"))

init_sqlalchemy()