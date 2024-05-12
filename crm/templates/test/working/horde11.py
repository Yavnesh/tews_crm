import asyncio
from pathlib import Path
import json
import aiohttp

# Replace with your actual API details
API_POST_URL = "https://stablehorde.net/api/v2/generate/async"
STATUS_URL = "https://stablehorde.net/api/v2/generate/check/{job_id}"
RESULT_URL = "https://stablehorde.net/api/v2/generate/status/{job_id}"

prompt = """**Top Ranked Image Prompt:**

**A family packed into a car, heading off on a road trip.**

**Refined Prompt for Professional Cover Photo:**

**A high-resolution, realistic image of a family packed into a car, heading off on a road trip. The family is laughing and smiling, and they are all wearing seatbelts. The car is packed with luggage and snacks, and it is driving down a scenic highway. The sun is shining, and the sky is clear and blue.**

**Description:**

This image prompt is designed to generate a visually appealing and heartwarming image of a family embarking on a road trip. The cartoonish style will make the image more engaging and fun, while the high-resolution will ensure that the image is clear and sharp. The prompt includes specific details about the family, the car, and the setting, which will help the AI to generate a more accurate and realistic image.

**Additional Notes:**

* The target audience for this image is US readers who love to read articles and blog posts.
* The image should be visually appealing and engaging, and it should evoke feelings of nostalgia, adventure, and family bonding.
* The image should be in a cartoonish style, with bright colors and exaggerated features.
* The image should be high-resolution and clear, with no blurry or distorted elements."""
async def main():
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

                    filepath_to_write_to = example_path / f"{image_id}_man_async_example.webp"

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
    asyncio.run(main())
