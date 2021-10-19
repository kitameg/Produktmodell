import glob
import logging
import csv
import yaml

FORMAT = '[yaml2csv] %(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

def all():
  logging.info("Alle YAML-Dateien werden nach CSV konvertiert")
  anwendungen()

def anwendungen():
  logging.info("Anwendungen werden konvertiert")
  fieldnames_anwendung = ['Anwendung', 'Langname', 'Produktteam', 'Produkttypen']
  fieldnames_anwendungsversion = ['Anwendung', 'Version', 'Produkttypversionen']

  anwendungen_csv = []
  anwendungsversionen_csv = []

  for yaml_file in glob.glob('Anwendung/**/*.yaml', recursive=True):
    logging.info(f'{yaml_file} wird konvertiert')
    anw = yaml.load(open(yaml_file, 'r'), Loader=yaml.BaseLoader)
    logging.debug(anw)
    anw_csv = {
      'Anwendung': anw['Anwendung'],
      'Langname': anw['Langname'],
      'Produktteam': anw['Produktteam'],
    }

    ptn = ""
    for pt in anw.get('Produkttypen', []):
      ptn = ptn + "||" if ptn != "" else ptn
      ptn = ptn + pt['Type-Id']

    anw_csv['Produkttypen'] = ptn

    anwendungen_csv.append(anw_csv)

    for anwver in anw['Versionen']:
      anwver_csv = {
        'Anwendung': anw['Anwendung'],
        'Version': anwver['Version'],
      }
      anwendungsversionen_csv.append(anwver_csv)
      ptvn = ""
      for ptv in anwver.get('Produkttypversionen', []):
        ptvn = ptvn + "||" if ptvn != "" else ptvn
        ptvn = ptvn + ptv['Type-Id']
      
      anwver_csv['Produkttypversionen'] = ptvn


  with open('Insight/Anwendung.v2.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames_anwendung, delimiter=';')
    writer.writeheader()
    writer.writerows(anwendungen_csv)

  with open('Insight/Anwendungsversion.v2.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames_anwendungsversion, delimiter=';')
    writer.writeheader()
    writer.writerows(anwendungsversionen_csv)
      