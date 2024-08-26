from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict
from unstract.llmwhisperer.client import LLMWhispererClient, LLMWhispererClientException

from langchain_openai import OpenAIEmbeddings

import json
import os



from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


import json


from typing import List
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
#from langchain_text_splitters import CharacterTextSplitte
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from pydantic import BaseModel, Field
from typing import List, Optional
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate


from unstract.llmwhisperer.client import LLMWhispererClient



from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import List, Dict
import pandas as pd




from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request


app = FastAPI()

client = LLMWhispererClient(base_url="https://llmwhisperer-api.unstract.com/v1", api_key="")




# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure templates directory
templates = Jinja2Templates(directory="templates")

os.environ['OPENAI_API_KEY'] = 'sk-proj-'

class CompleteBloodCount(BaseModel):
    rbc: float = Field(description="Red Blood Cell count in millions/cmm")
    haemoglobin: float = Field(description="Haemoglobin level in gm/dl")
    packed_cell_volume: float = Field(description="Packed Cell Volume in %")
    mcv: float = Field(description="Mean Corpuscular Volume in fl")
    mch: float = Field(description="Mean Corpuscular Hemoglobin in pg")
    mchc: float = Field(description="Mean Corpuscular Hemoglobin Concentration in g/dl")
    rdw_cv: float = Field(description="Red Cell Distribution Width - Coefficient of Variation in %")
    platelet_count: float = Field(description="Platelet Count in thou/µL")
    total_wbc_count: float = Field(description="Total White Blood Cell count in thou/µL")
    tnc: float = Field(description="Total Nucleated Cells count")
    mpv: float = Field(description="Mean Platelet Volume in fl")
    pct: float = Field(description="Plateletcrit in %")
    pdw: float = Field(description="Platelet Distribution Width in fl")
    neutrophil: float = Field(description="Neutrophil count in %")
    lymphocyte: float = Field(description="Lymphocyte count in %")
    monocytes: float = Field(description="Monocytes count in %")
    eosinophils: float = Field(description="Eosinophils count in %")
    basophils: float = Field(description="Basophils count in %")
    absolute_neutrophils: float = Field(description="Absolute Neutrophil count in cells/µL")
    absolute_lymphocytes: float = Field(description="Absolute Lymphocyte count in cells/µL")
    absolute_monocytes: float = Field(description="Absolute Monocyte count in cells/µL")
    absolute_eosinophils: float = Field(description="Absolute Eosinophil count in cells/µL")
    neutrophil_lymphocyte_ratio: float = Field(description="Neutrophil-Lymphocyte Ratio")
    lymphocyte_monocyte_ratio: float = Field(description="Lymphocyte-Monocyte Ratio")
    platelet_lymphocyte_ratio: float = Field(description="Platelet-Lymphocyte Ratio")

class GlucoseFasting(BaseModel):
    glucose_fasting: float = Field(description="Glucose Fasting level in mg/dl")

class HbA1c(BaseModel):
    hba1c_ngsp: float = Field(description="HbA1c level (NGSP) in %")
    hba1c_ifcc: float = Field(description="HbA1c level (IFCC) in mmol/mol")
    estimated_average_glucose: float = Field(description="Estimated Average Glucose in mg/dl")

class PatientInfo(BaseModel):
    clinic_name: str = Field(description="Clinic name")
    barcode_no: str = Field(description="Barcode number")
    patient_name: str = Field(description="Patient name")
    age_sex: str = Field(description="Age and sex")
    referred_by: str = Field(description="Referred by")
    client_code_name: str = Field(description="Client code or name")
    reg_date: str = Field(description="Registration date")
    report_date: str = Field(description="Report date")

class KidneyFunctionTest(BaseModel):
    sample_type: str = Field(description="Sample Type")
    urea: float = Field(description="Urea level in mg/dl")
    creatinine: float = Field(description="Creatinine level in mg/dl")
    uric_acid: float = Field(description="Uric Acid level in mg/dl")
    sodium: float = Field(description="Sodium level (Na+) in mmol/L")
    potassium: float = Field(description="Potassium level (K+) in mmol/L")
    chloride: float = Field(description="Chloride level in mmol/L")

class LiverFunctionTest(BaseModel):
    bilirubin_total: float = Field(description="Bilirubin Total level in mg/dl")
    bilirubin_direct: float = Field(description="Bilirubin Direct level in mg/dl")
    bilirubin_indirect: float = Field(description="Bilirubin Indirect level in mg/dl")
    sgot_ast: float = Field(description="SGOT (AST) level in U/L")
    sgpt_alt: float = Field(description="SGPT (ALT) level in U/L")
    alkaline_phosphatase: float = Field(description="Alkaline Phosphatase (ALP) level in U/L")
    calcium: float = Field(description="Calcium level in mg/dl")
    protein_total: float = Field(description="Protein Total level in g/dl")
    albumin: float = Field(description="Albumin (Serum) level in g/dl")
    globulin: float = Field(description="Globulin level in g/dl")
    alb_glo_ratio: float = Field(description="ALB/GLO Ratio")

class LipidProfileBasic(BaseModel):
    total_cholesterol: float = Field(description="Total Cholesterol level in mg/dl")
    triglyceride: float = Field(description="Triglyceride level in mg/dl")
    hdl_cholesterol: float = Field(description="HDL Cholesterol level in mg/dl")
    non_hdl_cholesterol: float = Field(description="Non HDL Cholesterol level in mg/dl")
    vldl_cholesterol: float = Field(description="VLDL Cholesterol level in mg/dl")
    ldl_cholesterol: float = Field(description="LDL Cholesterol level in mg/dl")
    cholesterol_hdl_ratio: float = Field(description="Cholesterol/HDL Ratio")
    ldl_hdl_cholesterol_ratio: float = Field(description="LDL/HDL Cholesterol Ratio")
    hdl_ldl_cholesterol_ratio: float = Field(description="HDL/LDL Cholesterol Ratio")

class IronProfileBasic(BaseModel):
    iron_serum: float = Field(description="Iron, Serum level in µg/dl")
    total_iron_binding_capacity: float = Field(description="Total Iron Binding Capacity (TIBC) in µg/dl")
    uibc_serum: float = Field(description="UIBC (Unsaturated Iron Binding Capacity) in µg/dl")
    transferrin_saturation: float = Field(description="Transferrin Saturation in %")

class ThyroidProfile(BaseModel):
    triiodothyronine_total: float = Field(description="Triiodothyronine Total (T3) level in ng/dl")
    thyroxine_total: float = Field(description="Thyroxine Total (T4) level in µg/dl")
    tsh: float = Field(description="TSH (4th Generation) level in µIU/ml")

class VitaminB12(BaseModel):
    vitamin_b12_level: float = Field(description="Vitamin B12 Level in pg/ml")

class VitaminD3_25Hydroxy(BaseModel):
    vitamin_d_25_hydroxy: float = Field(description="Vitamin D, 25 Hydroxy level in ng/ml")

class LabTests(BaseModel):
    patient_info: PatientInfo
    cbc: CompleteBloodCount
    glucose_fasting: GlucoseFasting
    hba1c: HbA1c
    kft: KidneyFunctionTest
    lft: LiverFunctionTest
    lipid_profile: LipidProfileBasic
    iron_profile: IronProfileBasic
    thyroid_profile: ThyroidProfile
    vitamin_b12: VitaminB12
    vitamin_d3: VitaminD3_25Hydroxy

reference_ranges = {
    "cbc": {
        "rbc": (4.5, 5.5),
        "haemoglobin": (13, 17),
        "packed_cell_volume": (40, 50),
        "mcv": (80, 100),
        "mch": (27, 32),
        "mchc": (27, 48),
        "rdw_cv": (11.5, 14),
        "platelet_count": (150, 450),
        "total_wbc_count": (4000, 10000),
        "mpv": (9.1, 11.9),
        "pct": (0.18, 0.39),
        "pdw": (9.0, 15.0),
        "neutrophil": (40.0, 80.0),
        "lymphocyte": (20.0, 40.0),
        "monocytes": (2, 10),
        "eosinophils": (1, 6),
        "basophils": (0, 1),
        "absolute_neutrophils": (2.00, 7.00),
        "absolute_lymphocytes": (1.00, 3.00),
        "absolute_monocytes": (0.20, 1.00),
        "absolute_eosinophils": (0.002, 0.50)
    },
    "glucose_fasting": {
        "glucose_fasting": (70.0, 110.0)
    },
    "hba1c": {
        "hba1c_ngsp": (0, 5.7),
        "hba1c_ifcc": (0, 36.52),
        "estimated_average_glucose": (0, 111.2)
    },
    "kft": {
        "urea": (13.0, 43.0),
        "creatinine": (0.70, 1.40),
        "uric_acid": (4.40, 7.60),
        "sodium": (135.0, 145.0),
        "potassium": (3.50, 5.50),
        "chloride": (98, 109)
    },
    "lft": {
        "bilirubin_total": (0.2, 1.2),
        "bilirubin_direct": (0, 0.3),
        "bilirubin_indirect": (0.30, 1.00),
        "sgot_ast": (0, 31.0),
        "sgpt_alt": (0, 33.0),
        "alkaline_phosphatase": (40, 129),
        "calcium": (8.6, 10.2),
        "protein_total": (6.6, 8.7),
        "albumin": (3.97, 4.95),
        "globulin": (2.50, 3.50),
        "alb_glo_ratio": (1.20, 2.10)
    },
    "lipid_profile": {
        "total_cholesterol": (0, 200),
        "triglyceride": (0.0, 150),
        "hdl_cholesterol": (40, 60),
        "non_hdl_cholesterol": (0, 130),
        "vldl_cholesterol": (0, 130),
        "ldl_cholesterol": (0, 130),
        "cholesterol_hdl_ratio": (0, 3.5),
        "ldl_hdl_cholesterol_ratio": (0, 3.5)
    },
    "iron_profile": {
        "iron_serum": (59, 158),
        "total_iron_binding_capacity": (250, 400),
        "uibc_serum": (110, 370),
        "transferrin_saturation": (16, 50)
    },
    "thyroid_profile": {
        "triiodothyronine_total": (0.81, 1.81),
        "thyroxine_total": (5.0, 10.7),
        "tsh": (0.40, 5.50)
    },
    "vitamin_b12": {
        "vitamin_b12_level": (220, 914)
    },
    "vitamin_d3": {
        "vitamin_d_25_hydroxy": (20, 65)
    }
}

def identify_outliers(test_results: Dict, reference_ranges: Dict):
    outliers = {}
    for test_category, tests in test_results.items():
        if test_category == "patient_info":
            continue  # Skip patient_info as it is not a lab test
        for test, value in tests.items():
            # Use .get() to handle cases where test name is not found
            low, high = reference_ranges.get(test_category, {}).get(test, (None, None))
            if (low is not None and value < low) or (high is not None and value > high):
                if test_category not in outliers:
                    outliers[test_category] = {}
                outliers[test_category][test] = value
    return outliers



# Main endpoint for rendering the template
@app.get("/")
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile = File(...)):
#     try:
#         file_path = f"/tmp/{file.filename}"
#         with open(file_path, "wb") as buffer:
#             buffer.write(file.file.read())

#         result = client.whisper(
#             file_path=file_path,
#             processing_mode="text",
#             force_text_processing=True,
#         )
#         extracted_text = result["extracted_text"]

#         with open("extracted_text.md", "w", encoding="utf-8") as f:
#             f.write(extracted_text)




#         # embeddings = OpenAIEmbeddings(openai_api_key='sk-proj-23HXRDZ01kG4aOdKH4ZoT3BlbkFJyD8mJLeiZg7XoGT5cdy9')


#         # Set up prompt templates
#         preamble = ("You are a medical expert AI chatbot having a conversation with a human. Your task is to provide accurate "
#                     "and helpful answers based on the extracted parts of a medical health report. Pay close attention to the "
#                     "medical report's structure, language, and any cross-references to ensure comprehensive and precise "
#                     "extraction of information. Do not use prior knowledge or information from outside the context to answer "
#                     "the questions. Only use the information provided in the context to answer the questions.")

#         postamble = "Do not include any explanation in the reply. Only include the extracted information in the reply."

#         system_template = "{preamble}"
#         system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

#         human_template = "{format_instructions}\n\n{extracted_text}\n\n{postamble}"
#         human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

#         chat_prompt = PromptTemplate(
#             input_variables=["preamble", "format_instructions", "extracted_text", "postamble"],
#             template=human_template
#         )

#         print('chatprompts called')

#         parser = PydanticOutputParser(pydantic_object=LabTests)
#         request = chat_prompt.format_prompt(
#                 preamble=preamble,
#                 format_instructions=parser.get_format_instructions(),
#                 extracted_text=extracted_text,
#                 postamble=postamble
#             ).to_messages()
#         chat = ChatOpenAI()
#         response = chat(request, temperature=0.0)


#         print("###")
#         print("the response is",response.content)



#         # Assuming `response_content` is a string containing JSON formatted data
#         response_data = json.loads(response_content)  # Load it as a Python dictionary

#         # Save the data to a file named "all_extract_lab_tests.json"
#         with open("all_extract_lab_tests.json", "w", encoding="utf-8") as json_file:
#             json.dump(response_data, json_file, indent=4)  # Pretty print with indentation

#         print("Saved the response content to all_extract_lab_tests.json")




#         response_content = json.loads(response.content)


#         print("#### response_content",response_content)
#         outliers = identify_outliers(response_content, reference_ranges)



#         # Save the response content as a JSON file
#         with open('response_content.json', 'w') as json_file:
#             json.dump(response_content, json_file, indent=4)  # Saving in a pretty format with indentation

#         print("Saved response_content as response_content.json")

#         # Example outliers (assuming it's a list of dictionaries or pandas dataframe)
#         outliers = identify_outliers(response_content, reference_ranges)











#         # Save all parameters and outliers as CSV and JSON
#         # Save outliers as CSV
#         df_outliers = pd.DataFrame.from_dict({(i,j): outliers[i][j] 
#                                               for i in outliers.keys() 
#                                               for j in outliers[i].keys()}, orient='index', columns=['Value'])
#         df_outliers.to_csv('outliers.csv', index=True)

#         # Save outliers as JSON
#         with open('outliers.json', 'w') as json_file:
#             json.dump(outliers, json_file, indent=4)

#         # Save all parameters as CSV
#         df_all_parameters = pd.DataFrame.from_dict({(i,j): response_content[i][j] 
#                                                     for i in response_content.keys() 
#                                                     for j in response_content[i].keys()}, orient='index', columns=['Value'])
#         df_all_parameters.to_csv('all_parameters.csv', index=True)

#         # # Save all parameters as JSON
#         # with open('all_parameters.json', 'w') as json_file:
#         #     json.dump(response_content, json_file, indent=4)

#         # return {
#         #     "outliers": outliers,
#         #     "response_content": response_content
#         # }










#         # Save the outliers as a CSV file
#         if isinstance(outliers, pd.DataFrame):
#             outliers.to_csv('outliershhh.csv', index=False)
#         else:
#             # Convert to pandas DataFrame if it's not already one
#             df_outliers = pd.DataFrame(outliers)
#             df_outliers.to_csv('outliers.csv', index=False)

#         print("Saved outliers as outliers.csv")


#    # Prepare the input for the model
#         prompt_template = """
#         Given the patient's out-of-range test results, provide general causes and food suggestions for each abnormal value. Advise the patient to consult a doctor for these values.

#         Out-of-Range Test Results:
#         {outliers}
#         """

#         prompt = ChatPromptTemplate.from_template(prompt_template)
#         output_parser = StrOutputParser()
#         model = ChatOpenAI(model="gpt-4")
#         chain = prompt | model | output_parser

#         model_response = chain.invoke({
#             "outliers": outliers
#         })

#         return {
#             "outliers": outliers,
#             "model_response": model_response
#         }
#     except LLMWhispererClientException as e:
#         raise HTTPException(status_code=400, detail=str(e))







@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    try:
        # Save the uploaded file
        file_path = f"/tmp/{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        # Extract the text using the whisper client
        result = client.whisper(
            file_path=file_path,
            processing_mode="text",
            force_text_processing=True,
        )
        extracted_text = result["extracted_text"]

        with open("extracted_text.md", "w", encoding="utf-8") as f:
            f.write(extracted_text)

        # Prepare the chat prompts for the AI model
        preamble = ("You are a medical expert AI chatbot having a conversation with a human. Your task is to provide accurate "
                    "and helpful answers based on the extracted parts of a medical health report. Pay close attention to the "
                    "medical report's structure, language, and any cross-references to ensure comprehensive and precise "
                    "extraction of information. Do not use prior knowledge or information from outside the context to answer "
                    "the questions.")
        postamble = "Do not include any explanation in the reply. Only include the extracted information in the reply."

        human_template = "{format_instructions}\n\n{extracted_text}\n\n{postamble}"
        chat_prompt = PromptTemplate(
            input_variables=["preamble", "format_instructions", "extracted_text", "postamble"],
            template=human_template
        )

        print('chatprompts called')

        # Parsing the response
        parser = PydanticOutputParser(pydantic_object=LabTests)
        request = chat_prompt.format_prompt(
            preamble=preamble,
            format_instructions=parser.get_format_instructions(),
            extracted_text=extracted_text,
            postamble=postamble
        ).to_messages()

        # Send the request to OpenAI's API
        chat = ChatOpenAI()
        response = chat(request, temperature=0.0)

        # Now `response.content` is ready
        response_content = response.content
        print("###")
        print("The response is:", response_content)

        # Parse the response content to a Python dictionary
        try:
            response_data = json.loads(response_content)  # Convert JSON string to Python dictionary
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=500, detail="Error decoding the response content as JSON") from e

        # Save the response content as a JSON file
        with open("all_extract_lab_tests.json", "w", encoding="utf-8") as json_file:
            json.dump(response_data, json_file, indent=4)  # Pretty-print with indentation

        print("Saved the response content to all_extract_lab_tests.json")

        # Identify outliers from the response content
        outliers = identify_outliers(response_data, reference_ranges)


        print("Saved response_content as response_content.json")

        # Save outliers to CSV and JSON
        df_outliers = pd.DataFrame.from_dict({(i,j): outliers[i][j] 
                                              for i in outliers.keys() 
                                              for j in outliers[i].keys()}, orient='index', columns=['Value'])
        #df_outliers.to_csv('outliers.csv', index=True)

        with open('outliers.json', 'w') as json_file:
            json.dump(outliers, json_file, indent=4)

        # Save all parameters as CSV
        df_all_parameters = pd.DataFrame.from_dict({(i,j): response_data[i][j] 
                                                    for i in response_data.keys() 
                                                    for j in response_data[i].keys()}, orient='index', columns=['Value'])
        df_all_parameters.to_csv('all_parameters.csv', index=True)



   # Prepare the input for the model
        prompt_template = """
        Given the patient's out-of-range test results, provide general causes and food suggestions for each abnormal value. Advise the patient to consult a doctor for these values.

        Out-of-Range Test Results:
        {outliers}
        """

        prompt = ChatPromptTemplate.from_template(prompt_template)
        output_parser = StrOutputParser()
        model = ChatOpenAI(model="gpt-4")
        chain = prompt | model | output_parser

        model_response = chain.invoke({
            "outliers": outliers
        })

   
        return {
            "outliers": outliers,
            "response_content": model_response
        }

    except LLMWhispererClientException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


























#uvicorn app:app --reload --port 8080


# ## in the code i also wanted to return below things by passing this outliers to below model



# # Prepare the input for the model
# prompt_template = """
# Given the patient's out-of-range test results, provide general causes and food suggestions for each abnormal value. Advise the patient to consult a doctor for these values.

# Out-of-Range Test Results:
# {outliers}
# """

# prompt = ChatPromptTemplate.from_template(prompt_template)
# output_parser = StrOutputParser()


# model = ChatOpenAI(model="gpt-4")

# chain = prompt | model | output_parser

# response = chain.invoke({
#     "outliers": outliers
# })

# print(response)




