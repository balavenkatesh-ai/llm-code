from langchain_community.document_loaders import JSONLoader
import json
import yaml
import tempfile
import os
from pathlib import Path

def load_yaml(source_path, yaml_file):
    tmp = tempfile.NamedTemporaryFile(delete=False, mode="w+")
    with open(Path(source_path, yaml_file).resolve()) as stream:
        yaml_data = yaml.safe_load_all(stream)
        mydict = {}
        for result in yaml_data:
            mykey=list(result.keys())
            for key in mykey:
                mydict[key] = result.get(key)
        json.dump(mydict, tmp)
        tmp.flush()
    loader = JSONLoader(tmp.name, jq_schema='.', text_content=False)
    pages = loader.load_and_split()
    os.unlink(tmp.name)
    return [{
        "metadatas": json.dumps({
            "metadata_type": "yaml", 
            "page": x.metadata['seq_num']+1, 
            "path": source_path, 
            "filename": yaml_file
            }),
        "documents": x.page_content
    } for x in pages]
