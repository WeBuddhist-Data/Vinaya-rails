import importlib.util,re,glob,pathlib
spec=importlib.util.spec_from_file_location('x','4-SYSTEM/scripts/tipitaka-xml-to-json/xml_to_json.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
LAYER={'mul':('mula','Mūla','Vinayapiṭaka','11'),'att':('atthakatha','Aṭṭhakathā','Vinayapiṭaka (aṭṭhakathā)','21'),'tik':('tika','Tīkā','Vinayapiṭaka (ṭīkā)','31'),'nrf':('tika','Tīkā','Vinayapiṭaka (ṭīkā)','31')}
for f in sorted(glob.glob('0-INBOX/raw-data/tipitaka-xml/*.xml')):
    name=pathlib.Path(f).name; stem,lt=name.split('.')[:2]
    t=open(f,encoding='utf-16').read()
    books=[re.sub('<[^>]+>','',b).strip() for b in re.findall(r'rend="book">(.*?)</',t)]
    title=books[0] if books else re.sub('<[^>]+>','',re.findall(r'rend="chapter">(.*?)</',t)[0])
    layer,top,mid,fts=LAYER[lt]
    d=m.convert(f,f'0-INBOX/raw-data/{stem}.json',title,f'{top} > {mid} > {title}','vinaya',layer,fts)
