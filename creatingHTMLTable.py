import json
import json2table
from json2table import convert
with open('json.json', 'r') as jsonFile:
    with open("htmlTable.html", "w") as html: 
        infoFromJson = json.load(jsonFile)
        build_direction = "LEFT_TO_RIGHT"
        table_attributes = {"style": "width:100 ; border: 1px solid black"}
        htmlTable= json2table.convert(infoFromJson,build_direction=build_direction,table_attributes=table_attributes)
        print(htmlTable)
        html.writelines(htmlTable)