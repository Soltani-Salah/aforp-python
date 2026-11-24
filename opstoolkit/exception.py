import logging 
from  pathlib import Path

def read():
	logging.basicConfig(filename="events.log",
	level=logging.DEBUG,
	format="%(asctime)s - %(levelname)s - %(message)s"
	)

	try:
		logging.info("Je suis dans le bloc try")
		folder = Path("../data")
		if not folder.is_dir():
			logging.error("le dossier est introuvable")
		else:
			for file in folder.glob("*.txt"):
				taille = file.stat().st_size
				with open(file, "r", encoding="utf-8") as f:
					content = f.read()
				logging.info(
					"Fichier lu: %s, taille : %s octets",
					file.name,
					taille
				)
				print("Fichier :", file.name)
				print("Taille :", taille)
				print("Contenu :", content)
	
	except ValueError:
		logging.error("Le dossier est introuvable")
	finally:
		print("Continuons!!!!")	
read()
