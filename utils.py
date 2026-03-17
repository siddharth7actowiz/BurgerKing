import json
def read_html(Path):
    try:
        with open(Path,"r",encoding="utf-8") as f:
            data=f.read()
            return data
    except Exception as e:
        print("Error",read_html.__name__,e)    


def read_json(path):
   try:
        with open(path,'r') as f:
            data=json.loads(f) 
   except Exception as e:
        print("Error",read_json.__name__,e)    
                