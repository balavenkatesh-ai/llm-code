Task Updates:

We've processed 4 manifest files, converted them to CSV format, and pushed them to the Faiss vector database.
A conversation chain has been created to retrieve data based on prompts.
To address function calling, we initially used the Phidata library. However, it's not compatible with the Llama 2 model.
The Llama model has been hosted on Databricks and integrated with LangChain. However, the associated costs are proving to be too high.
We've utilized the Instruct library for function calls.
A custom chain has been developed to retrieve item IDs and component details in JSON format.
Challenges:

When users prompt for generating an MSBR report, we need the system to call the "generate MABR" function. Essentially, we need to route user prompts to the appropriate function based on their input.
Handling parallel calls to the LLM model poses a challenge. If 20 users hit the system simultaneously, the processing currently occurs sequentially.
RAG Retrieval Technique:

Backend retrieval is done through the Vector Store backend retriever.
We've implemented contextual compression and filtering techniques for efficient retrieval.
