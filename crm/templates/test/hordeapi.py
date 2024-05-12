import asyncio
import time
import json
import aiohttp, os, requests

# Replace with your actual API details
API_POST_URL = "https://stablehorde.net/api/v2/generate/async"
STATUS_URL = "https://stablehorde.net/api/v2/generate/check/{job_id}"
RESULT_URL = "https://stablehorde.net/api/v2/generate/status/{job_id}"


async def main():
    # Replace with your actual API key
    api_key = "7LGsqLjIsFMXtsnwbgobTA"

    # Example request body (customize parameters as needed)
    body = {
        "prompt": "A photorealistic portrait of a cat wearing a crown",
        # "params": {...}  # Add additional parameters if needed (refer to API documentation)
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
                    status = data.get("done")
                    if status:
                        break  # Job is finished
                    print(f"Job status: {status}")
            except (aiohttp.ClientError, json.JSONDecodeError) as e:
                print(f"Error checking job status: {e}")
            await asyncio.sleep(10)  # Sleep for 10 seconds between checks

        # Get results
        result_url = RESULT_URL.format(job_id=request_id)
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
        except (aiohttp.ClientError, json.JSONDecodeError) as e:
            print(f"Error fetching results: {e}")

        # output_dir = os.path.dirname(output_filename)
        # if not os.path.exists(output_dir):
        #     os.makedirs(output_dir)

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as response:
                    response.raise_for_status()  # Raise exception for non-200 status codes

                output_filename = f"{image_id}_{'img_'}.webp"
                # Construct the final output filename with extension (if not provided)

                with open(output_filename, "wb") as f:
                    async for chunk in response.content:
                        f.write(chunk)

                

            print(f"Image downloaded successfully: {output_filename}")
            return True

        except (aiohttp.ClientError, OSError) as e:
            print(f"Error downloading image: {e}")
            return False

if __name__ == "__main__":
    asyncio.run(main())
