import json
import time
import httpx


async def run_windmill_job(token, body, base_url):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    
    async with httpx.AsyncClient() as client:
        # Start the job
        url = f'{base_url}/jobs/run/f/u/siam19/seavoice_transcript_to_summary'
        response = await client.post(url, headers=headers, json=body)
        uuid = response.text.strip('"')
        print("sent transcript..")
        # Poll for job completion
        url = f'{base_url}/jobs_u/completed/get_result_maybe/{uuid}'
        while True:
            response = await client.get(url, headers=headers)
            data = response.json()
            
            if data.get('completed'):
                print("summary done..")
                return data.get('result')
            
            time.sleep(1)

async def send_transcript(transcript_url:str):
    token = 'bWluNCSHd0KipMlktemoo5TdzsSJhaFF'
    body = {
    "seavoice_transcript_url": transcript_url
    }
    base_url = 'https://app.windmill.dev/api/w/automations_bastok'
    print("sending transcript..")
    result = await run_windmill_job(token, body, base_url)
    return result
