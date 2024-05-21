import asyncio
from pathlib import Path
import json
import aiohttp
from PIL import Image
import base64
from io import BytesIO
# Replace with your actual API details
API_POST_URL = "https://stablehorde.net/api/v2/generate/async"
STATUS_URL = "https://stablehorde.net/api/v2/generate/check/{job_id}"
RESULT_URL = "https://stablehorde.net/api/v2/generate/status/{job_id}"

Frames = ["A cute ball with a happy face sitting on the ground, starting to compress slightly as it prepares to bounce, with a simple white background.",
          "A cute ball with a happy face compressed more, ready to bounce, with slight deformation indicating downward pressure, with a simple white background.",
          "A cute ball with a happy face beginning to lift off the ground, slightly stretched vertically, with a simple white background.",
          "A cute ball with a happy face rising into the air, more stretched vertically, with a small shadow below it on the ground, with a simple white background.",
          "A cute ball with a happy face at the peak of its bounce, fully stretched vertically, highest point above the ground, with a simple white background.",
          "A cute ball with a happy face starting to fall back down, slightly less stretched, with a shadow growing on the ground, with a simple white background.",
          "A cute ball with a happy face falling faster towards the ground, less stretched, shadow getting closer, with a simple white background.",
          "A cute ball with a happy face just above the ground, almost back to its normal shape, shadow directly underneath, with a simple white background.",
          "A cute ball with a happy face hitting the ground, compressing slightly again on impact, with a simple white background.",
          "A cute ball with a happy face compressed on the ground, ready to bounce back up again, completing the cycle, with a simple white background."
        ]




def webp_to_base64(image_path):
    # Open the WebP image file
    with Image.open(image_path) as img:
        # Load the image into a BytesIO buffer
        buffered = BytesIO()
        img.save(buffered, format="WEBP")
        webp_image = buffered.getvalue()
        
        # Encode the WebP image to Base64
        base64_encoded = base64.b64encode(webp_image).decode('utf-8')
        
        # Create the Base64 data URL
        base64_webp = f"data:image/webp;base64,{base64_encoded}"
        print(base64_webp)
        return base64_encoded

async def main(base64_webp,ii):
    # Replace with your actual API key
    api_key = "7LGsqLjIsFMXtsnwbgobTA"

    # Example request body (customize parameters as needed)
    body = {
        "prompt": prompt,
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
        "source_image": base64_webp,
        "source_processing": "img2img",
    }                



    # Optional headers
    headers = {
        "apikey": f"{api_key}",
        "Client-Agent": "your_client_name/version"  # Replace with your client info
    }

    async with aiohttp.ClientSession() as session:
        # Send the POST request asynchronously
        try:
            async with session.post(API_POST_URL, headers=headers, json=body) as response:
                response.raise_for_status()  # Raise exception for non-200 status codes
                data = await response.json()
                request_id = data.get("id")
                print(f"Request submitted. Request ID: {request_id}")
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            print(f"Error sending request: {e}")
            return

        # Check job status in a loop
        while True:
            check_url = STATUS_URL.format(job_id=request_id)
            try:
                async with session.get(check_url, headers=headers) as response:
                    response.raise_for_status()
                    data = await response.json()
                    print(data)
                    status = data.get("done")
                    if status:
                        print(f"Job status: {status}")
                        break  # Job is finished
                    
            except (aiohttp.ClientError, json.JSONDecodeError) as e:
                print(f"Error checking job status: {e}")
            await asyncio.sleep(10)  # Sleep for 10 seconds between checks

        # Get results
        result_url = RESULT_URL.format(job_id=request_id)
        while True:
            try:
                async with session.get(result_url, headers=headers) as response:
                    response.raise_for_status()
                    data = await response.json()
                    image_url = ""
                    image_id = ""
                    for generation in data["generations"]:
                        image_url = generation["img"]
                        image_id = generation["id"]
                        print(f"Image URL: {image_url}")
                        print(f"Image ID: {image_id}")

                    image_bytes = None
                    # image_gen.img is a url, download it using aiohttp.
                    async with aiohttp.ClientSession() as session, session.get(image_url) as resp:
                        image_bytes = await resp.read()
                        print(f"URL: {image_bytes}")

                    if image_bytes is None:
                        print("Error: Could not download image.")
                        return

                    example_path = Path("examples/requested_images")
                    example_path.mkdir(exist_ok=True, parents=True)

                    filepath_to_write_to = example_path / f"{ii}.webp"

                    with open(filepath_to_write_to, "wb") as image_file:
                        image_file.write(image_bytes)

                    print(f"Image downloaded to {filepath_to_write_to}!")
                    print(f"URL: {image_url}")
                    status = data.get("done")
                    if status:
                        break  # Job is finished

            except (aiohttp.ClientError, json.JSONDecodeError) as e:
                print(f"Error fetching results: {e}")

if __name__ == "__main__":
    ii = 0
    for i in Frames:
        ii = ii + 1
        prompt = """
        {}
        
        """.format(i)

        image_path = f"examples/requested_images/{ii-1}.webp" 
        print("check 1")
        base64_webp = webp_to_base64(image_path)
        print("check2")
        asyncio.run(main(base64_webp,ii))
