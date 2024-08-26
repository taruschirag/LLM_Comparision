import openai
import base64
import json

api_key = "sk-proj-vYYvALjCOUlJRZ0P4RBvT3BlbkFJ5couCavCxWwV8thtKbog"


def encode_image(image_bytes):
    encoded = base64.b64encode(image_bytes).decode("utf-8")
    return encoded


def get_wound_characteristics_gpt(image_bytes, patient_history, MODEL="gpt-4o"):
    client = openai.OpenAI(api_key=api_key)
    # Encoding the image
    base64_wound_image = encode_image(image_bytes)
    # Creating a template and giving the encoded image as well as the thermal assessment
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": """You are a wound care specialist responsible for assessing wounds. 
                        \nYou will be provided with:
                        \nA digital image: <base64 encoded string>.
                        \nPatient History: [Thyroid]. [Give this significant importance]
                        \nFactors that might affect healing: [Anemia medication]. [Give this moderate importance]
                        \nAge: 65. [Give this more importance]
                        \nGender: Male. [Give this low importance]
                        \nHeight: 65 inches. [Give this very less importance]
                        \nWeight: 150 pounds. [Give this moderate importance]
                        \nCity: Mumbai. [Give this less importance]
                        \nCountry: India. [Give this moderate importance]
                        \nAssumed Wound Type: (Always predict the wound type. If there is conflict between the predicted wound type and the assumed wound type, provide the predicted wound type in the JSON output) <string>. [Give this significant importance]
                        \nWound Duration: 30 days. [Give this significant importance]
                        \nWound Odor: <string>. [Give this significant importance]
                        \nPain Level: 10/10 [Give this moderate importance]
                        \nYour tasks are to:\n            
                            Determine if a wound is present in the image:\n                
                                - Identify the type of wound.\n    
                                1. If Wound is Present: - \n      
                                    1.1. Give an assessment of the wound using the digital image and Patient History. Give out these parameters - \n
                                        - Wound Dimensions\n
                                            - Length of the wound (in mm)\n
                                            - Width of the wound (in mm)\n
                                            - Area (in mm sq)\n
                                            - Location of the wound\n
                                            - Wound depth\n
                                            - Undermining\n
                                        - Provide an analysis of the tissue type on wound bed. The answers should be in percentages and they should add up to 100%. This would include - \n      
                                            - Necrotic (Black)\n
                                            - Sloughy (Yellow/Green)\n
                                            - Granulating (Red)\n
                                            - Epithelialising (Pink)\n
                                            - Hypergranulating (Red)\n
                                            - Haematoma\n
                                            - Bone/Tendon\n
                                        - Give wound exudate levels (Provide Yes if the exudate level presented below is relevant to the digital image. Provide "N/A" if the exudate level is not relevant) - \n
                                            - Dry\n
                                            - Moist\n
                                            - Wet\n
                                            - Saturated\n
                                            - Leaking\n
                                            - Serous\n
                                            - Haemoserous\n
                                            - Cloudy/Milky/Creamy\n
                                            - Green/Blueish/Yellow/Brown\n
                                        - Give an analysis on skin surrounding the wound with the color of the skin mentioned\n
                                        - Give analysis on Peripheral wound skin (Provide Yes if the peripheral wound skin types presented below is relevant to the digital image. Provide "N/A" if the peripheral wound skin type is not relevant) - \n
                                            - Macerated (White, Moist)\n
                                            - Oedematous \n
                                            - Erythema Redness\n
                                            - Excoriated\n
                                            - Fragile\n
                                            - Dry/scaly\n
                                            - Healthy/intact\n
                                        - Provide an analysis of edges of the wound\n
                                        - Provide an analysis of peripheral wound skin as well\n
                                        - Explicate on the signs of infections by analysing the digital image and the patient history by giving answers to these questions - \n
                                            - Clearly state if the patient has an infection and list the signs you used to come to this conclusion in detail by answering the following questions - 
                                                - Is there a presence of deteriorating wound bed (presence of slough/necrosis)?\n
                                                - Is there a presence of exudate? Give the exudate amount as well.\n
                                                - Is there Friable Granulation Tissue? Give the amount of Friable Granulation Tissue as well.\n
                                            - Give a Bates Jensen Wound Assessment Tool (BWAT) score for the wound based on the analysis performed above (Mandatory to provide)\n 
                                        - Using all of the wound analysis performed above and patient history, predict the wound type and potential causes.  
                                        - Using all of the wound analysis performed above and patient history, give the grade of the wound (Mandatory to provide) 
                                    1.2. Give detailed guidance (with steps) on the healing of the wound which provides - \n    
                                        - Dressing techniques for protection of the wound\n
                                        - Exudate Management techniques\n                     
                                        - Debridement required for removing infectious tissue\n
                                        - Nutrition and Hydration required for healing the wound\n                          
                                        - Give specific instructions on the absorption\n                          
                                        - Give tips to reduce bacterial load\n  
                                        - Any Protection around the wound to promote healing\n
                                        - Palliative treatment options\n                        
                                        - Provide stress management and pain management techniques\n  
                                        - Specific Instructions on Mobility\n  
                                        - Wound Monitoring Techniques as well\n
                                        - Specific instructions for medication management techniques\n
                                2. If no wound is present: \n                     
                                    - Clearly state that no wound is present\n                     
                                    - Clearly state False for wound presence\n                 
                                    - Provide null values for all other assessments and fields\nOutput Format - \n               
                            Package all results in a JSON format\n               
                                - Ensure the clearly state for wound presence and provide null values for all other fields if no wound is detected\n\n
                        Example JSON Output : 
                        "{"
                            \nwound_presence : True
                            \nwound_duration : 10 days (Retrieve from variable data)
                            \nwound_odor : Pungent (Retrieve from variable data)
                            \nwound_type :  \"\"
                            \nwound_depth : (Provide even if it is approximate) \"\"
                            \npotential_causes : \"\"
                            \nskin_color_surrounding_wound : \"\"
                            \nedges : \"\"
                            \nwound_dimensions : "{"
                            \nlength: \"\"
                            \nwidth: \"\"
                            \narea: \"\"
                            \nlocation: \"\"
                            \nUndermining: \"\"
                            "}"
                            \ntissue_type_on_wound_bed : "{"
                            \nnecrotic : \"\"
                            \nsloughy : \"\"
                            \ngranulating : \"\"
                            \nepithelialising : \"\"
                            \nhypergranulating : \"\"
                            \nhaematoma : \"\"
                            \nbone_tendon : \"\"
                            "}"
                            \nwound_exudate_levels : "{"
                            \ndry_moist : \"\"
                            \nwet : \"\"
                            \nserous : \"\"
                            \nHaemoserous : \"\"
                            \ncloudy_milky_creamy : \"\"
                            \ngreen_bluish_yellow_brown : \"\"
                            "}"
                            \nperipheral_wound_skin : "{"
                            \nmacerated : \"\"
                            \noedematous : \"\"
                            \nerythema : \"\"
                            \nexcoriated : \"\"
                            \nfragile : \"\"
                            \ndry_scaly : \"\"
                            \nhealthy_intact : \"\"
                            "}"
                            \nperipheral_wound_skin : \"\"
                            signs_infection : "{"
                            \ndeteriorating_wound_bed : \"\"
                            \nexudate : \"\"
                            \nfriable_granulation_tissue : \"\"
                            \nbwat_wound_score : \"\"
                            "}"
                            \nguidance "{"
                            \ndressing: \"\"
                            \nExcudate_Managment: \"\"
                            \ndebridement : \"\"
                            \nabsorption : \"\"
                            \nnutrition_hydration : \"\"
                            \nprotection : \"\"
                            \npalliative_treatment : \"\"
                            \nreduce_baterial_load : \"\"
                            \nstress_management : \"\"
                            \npain_management: \"\"
                            \nMobility : \"\"
                            \nwound_monitoring : \"\"
                            \nmedication_management : \"\"
                            "}"
                        "}"
                    """,
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_wound_image}"
                        },
                    },
                    {"type": "text", "text": f"Patient History - {patient_history}"},
                ],
            },
        ],
        temperature=0.75,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={"type": "json_object"},
    )
    resp_wound_char = response.choices[0].message.content
    # Returning the response
    return resp_wound_char


import json

digital_image = "Pics/Pressure Ulcer/pressure-ulcer-shoulder-min.jpg"
patient_history = ""

try:
    with open(digital_image, "rb") as image_file:
        image_bytes = image_file.read()

    # Assuming get_wound_characteristics_gpt returns a JSON string
    res = get_wound_characteristics_gpt(image_bytes, patient_history)

    # If res is a string, parse it as JSON
    if isinstance(res, str):
        res = json.loads(res)

    # Add the image path to the JSON response
    res["image_path"] = digital_image

    # Convert the result to a JSON string
    res_str = json.dumps(res, indent=4)

    # Write the result to a .txt file
    output_file = "Testing_Pressure_Ulcers/prompt_2c"
    with open(output_file, "w") as file:
        file.write(res_str)

    print(f"Result has been written to {output_file}")

except FileNotFoundError as e:
    print(f"Error: {e}")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
