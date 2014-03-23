from model import *
from config import db_session

def process():
	recs = db_session.query(Eq).filter_by().all()
   
	for record in recs:

		wpname = record.WeaponName
		wptype = record.WeaponType
		arname = record.ArmorName
		artype = record.ArmorType
		charid = record.CHARACTERS_CharacterID
		
		
		print wpname,wptype,arname,artype,charid
		if wpname != None:
			rec = db_session.query(Equipment).filter_by(Name = wpname, Type = wptype, EquipmentType = 'Weapon').first()
			
		else:
			rec = db_session.query(Equipment).filter_by(Name = arname, Type = artype, EquipmentType = 'Armor').first()
		
		obj = CharHasEquip(record.CHARACTERS_CharacterID,rec.RowID)	
		db_session.add(obj)
		db_session.commit()		
				
if __name__ == "__main__":
	process()





