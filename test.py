from langchain_community.document_loaders import JSONLoader
import json
import yaml
import tempfile
import os
from pathlib import Path

Task Details:
Performing RAG with JSON format of manifest data.

Challenge:
Encountering accuracy issues with the LLM model when extracting data from JSON format. Specifically, when querying for item IDs, it refers to app-ID key values instead.

Actions to Overcome:
1. Added item IDs into the metadata field in the database, but other details are still inaccurate.
2. Attempted splitting JSON into multiple documents using the chunk option, but results were still incorrect.
3. Converted JSON into flattened JSON format and stored it in the vector database, yet accuracy remained an issue.
4. Changed the LLM model and tested for improved accuracy.
5. Crafted prompts to reference the correct keys for retrieving values.
7. Implemented the MapReduceDocumentsChain technique to retrieve each document and filter the contents using the LLM model for improved accuracy. However, it continues to reference app-ID instead of item ID details.

#MapReduceDocumentsChain #LLMModel #DataFiltering #AccuracyIssues
#RAG #JSON #LLM #DataExtraction #AccuracyChallenges

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
