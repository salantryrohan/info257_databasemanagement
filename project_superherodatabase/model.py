from sqlalchemy import create_engine,Table, Column, Integer, ForeignKey,String, Date
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from config import Base,engine


# methods to initalize database and have it up and running 

def init_db():
    Base.metadata.create_all(bind=engine)


class User(Base):

    __tablename__ = 'USER'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(50))
    

    def __init__(self,email=None,pwd = None):
        self.name = email
        self.email = email
        self.password = pwd
        

    def __repr__(self):
        return self.name



class Characters(Base):
    
    __tablename__ = 'CHARACTERS'

    CharacterID = Column(Integer, primary_key=True)
    CharacterTitle = Column(String(45))
    CharacterFName = Column(String(45))
    CharacterLName = Column(String(45))
    CharacterAlias = Column(String(45))
    CharacterAlignment = Column(String(45))
    CharacterGender = Column(String(45))
    CharacterRace = Column(String(45))
    CharacterImage = Column(String(45))
    CharacterYearCreated = Column(Integer)
    SuperHeroAge = Column(String(45))
    UNIVERSE_UniverseID = Column(Integer)
    CREATORS_CreatorID = Column(Integer)
    CharacterOrigin = Column(String(1000))

        
    def __repr__(self):
        return self.CharacterAlias


class Teams(Base):

    __tablename__ = 'TEAM'

    TeamID = Column(Integer,primary_key = True)
    TeamName = Column(String(45))
    TeamDesc = Column(String(200))

    def __repr__(self):
        return self.TeamName
        


class TeamHasChars(Base):

    __tablename__ = 'TEAM_HAS_CHARS'

    RowID = Column(Integer,primary_key = True)
    TeamID = Column(Integer,ForeignKey('TEAM.TeamID'))
    CharcterID = Column(Integer,ForeignKey('CHARACTERS.CharacterID'))
    CharRole = Column(String(45))

    def __repr__(self):
        return str(self.RowID)


class HeroHasVillians(Base):
    __tablename__ = 'HERO_HAS_VILL'

    RowID = Column(Integer,primary_key = True)
    HeroID = Column(Integer,ForeignKey('CHARACTERS.CharacterID'))
    VillainID = Column(Integer,ForeignKey('CHARACTERS.CharacterID'))
    


class Ability(Base):
    __tablename__ = 'ABILITY'

    AbilityID = Column(Integer,primary_key = True)
    AbilityName = Column(String(45))
    AbilityType = Column(String(45))

class CharHasAbility(Base):
    __tablename__ = 'CHAR_HAS_ABIL'

    RowID = Column(Integer,primary_key = True)
    CharacterID = Column(Integer,ForeignKey('CHARACTERS.CharacterID'))
    AbilityID = Column(Integer,ForeignKey('ABILITY.AbilityID'))

class Equipment(Base):
    __tablename__ = 'ALLEQUIPMENT'

    EquipmentID = Column(Integer,primary_key = True)
    Name = Column(String(50))
    Type = Column(String(50))
    EquipmentType = Column(String(45))

class CharHasEquip(Base):

    __tablename__ = 'CHAR_HAS_EQUIP'

    RowID = Column(Integer,primary_key = True)
    CharacterID = Column(Integer,ForeignKey('CHARACTERS.CharacterID'))
    EquipmentID = Column(Integer,ForeignKey('ALLEQUIPMENT.EquipmentID'))


class Creator(Base):
    
    __tablename__ = 'CREATORS'

    CreatorID = Column(Integer,primary_key = True)
    CreatorFirstName = Column(String(45))
    CreatorLastName = Column(String(45))
    

class Universe(Base):
    __tablename__ = 'UNIVERSE'

    UniverseID = Column(Integer,primary_key = True)
    UniverseName = Column(String(50))

class Discussion(Base):
    __tablename__ = 'DISCUSSION'
    
    DiscussionID = Column(Integer,primary_key = True)
    Title = Column(String(50))
    CreatedBy = Column(Integer,ForeignKey('USER.id'))

class Comments(Base):
    __tablename__ = 'COMMENTS'
    
    CommentID = Column(Integer,primary_key = True)
    DiscussionID = Column(Integer,ForeignKey('DISCUSSION.DiscussionID'))
    Title = Column(String(50))
    CreatedBy = Column(Integer,ForeignKey('USER.id'))

