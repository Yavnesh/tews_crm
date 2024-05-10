import asyncio
import time
import requests
from aiohttp import ClientSession

# Replace with your actual API details
API_POST_URL = "https://stablehorde.net/api/v2/generate/async"
# API_GET_URL = "https://stablehorde.net/api/v2/generate/check"
# # Replace with your actual API details
# POST_URL = "https://stablehorde.net/api/v2/generate/async"  # URL for initiating the task
STATUS_URL = "https://stablehorde.net/api/v2/generate/check/{job_id}"  # URL to check status
RESULT_URL = "https://stablehorde.net/api/v2/generate/status/{job_id}"  # URL to fetch data

import requests
import json

# Replace with your actual API key
api_key = "0000000000"

# Example request body (customize parameters as needed)
# body = {
#     "payload":{
#                 "prompt": "A photorealistic portrait of a cat wearing a crown"
#                 # "params": {
                #     "sampler_name": "k_dpmpp_sde",
                #     "cfg_scale": 7.5,
                #     "denoising_strength": 0.75,
                #     "seed": "The little seed that could",
                #     "height": 512,
                #     "width": 512,
                #     "seed_variation": 1,
                #     "post_processing": [
                #     "GFPGAN"
                #     ],
                #     "clip_skip": 1,
                #     "control_type": "canny",
                #     "facefixer_strength": 0.75,
                #     "loras": [
                #     {
                #         "name": "Magnagothica",
                #         "model": 1,
                #         "clip": 1,
                #         "inject_trigger": "string",
                #     }
                #     ],
                #     "steps": 30,
                #     "n": 1, 
                # },
                # "models": [
                #     "Deliberate"
                # ],
body = {
        "prompt": "A photorealistic portrait of a cat wearing a crown",
        "params": {
                    "sampler_name": "k_dpmpp_sde",
                    "cfg_scale": 7.5,
                    "denoising_strength": 0.75,
                    "seed": "tews",
                    "height": 576,
                    "width": 960,
                    "seed_variation": 1,
                    "post_processing": [
                    "GFPGAN" #"RealESRGAN_x4plus", "NMKD_Siax","CodeFormers"
                    ],
                    "facefixer_strength": 1,
                    "steps": 10,
                    "n": 1, 
                },
        "models": [
            "Deliberate",""
        ],
    }                

# Optional headers
headers = {
    "apikey": f"{api_key}",
    "Client-Agent": "unknown:0:unknown",  # Replace with your client info
    # "X-Fields": "..."  # Optional field mask (refer to API documentation)
}

# Send the POST request
# url = "https://<your-api-endpoint>/v2/generate/async"  # Replace with actual endpoint
response = requests.post(API_POST_URL, headers=headers, json=body)
request_id = ""
# Handle the response
if response.status_code == 202:  # Accepted request
    data = response.json()
    print(data)
    request_id = data.get("id")
    print(f"Request submitted. Request ID: {request_id}")
else:
    print(f"Error sending request: {response.status_code} - {response.text}")

headers1 = {
    "Client-Agent": "unknown:0:unknown",  # Replace with your client info
    # "X-Fields": "..."  # Optional field mask (refer to API documentation)
}
check_url = STATUS_URL.format(job_id=request_id)

print("check_url",check_url)

aq ="F"
while aq == "F":
    response1 = requests.get(check_url)
    data = response1.json()
    print(data)
    sta = data.get("done")
    print("sta",sta)
    if  sta == True:
        aq ="T"
    
    print(data.get("done"))
    time.sleep(10)

check_url1 = RESULT_URL.format(job_id=request_id)
response2 = requests.get(check_url1)
data = response2.json()
print(data)

for generation in data['generations']:
    image_url = generation['img']
    image_id = generation['id']
    print(f"Image URL: {image_url}")
    print(f"Image ID: {image_id}")