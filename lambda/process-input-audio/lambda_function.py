import boto3
import uuid
import time
import os

def lambda_handler(event, context):
    try:
        # Retrieve the S3 bucket and object information from the event
        s3_bucket = event['Records'][0]['s3']['bucket']['name']
        s3_key = event['Records'][0]['s3']['object']['key']
        print(f"Received file: {s3_key} from bucket: {s3_bucket}")

        # Extract the file name from the s3_key (removing the file extension to use as the output file name)
        input_file_name = os.path.splitext(os.path.basename(s3_key))[0]
        output_file_name = f"{input_file_name}.txt"  # Use the input file name with .txt extension for output

        # Generate a unique job name
        job_name = str(uuid.uuid4())

        # Create an Amazon Transcribe client
        transcribe_client = boto3.client('transcribe')
        
        # Set the S3 URI for the input audio file
        s3_uri = f"s3://{s3_bucket}/{s3_key}"

        # Start the transcription job
        print("Starting transcription job...")
        transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            LanguageCode='hi-IN',  # Specify the input language (Hindi in this case)
            Media={'MediaFileUri': s3_uri},
            OutputBucketName='output-voice-bucket',  # Specify the output bucket name
            OutputKey=output_file_name  # Use the input file name as the output file name
        )
        print(f"Transcription job started with name: {job_name}")

        # Wait for the transcription job to complete
        job_status = 'IN_PROGRESS'
        max_wait_time = 180  # Maximum wait time in seconds (3 minutes)
        wait_interval = 10  # Polling interval in seconds
        elapsed_time = 0

        while job_status == 'IN_PROGRESS' and elapsed_time < max_wait_time:
            print(f"Checking job status... (elapsed time: {elapsed_time}s)")
            time.sleep(wait_interval)
            elapsed_time += wait_interval

            status_response = transcribe_client.get_transcription_job(
                TranscriptionJobName=job_name
            )
            job_status = status_response['TranscriptionJob']['TranscriptionJobStatus']
            print(f"Job status: {job_status}")

            if job_status == 'COMPLETED':
                print("Transcription job completed successfully.")
                # Retrieve the transcript text from the results URL
                transcript_uri = status_response['TranscriptionJob']['Transcript']['TranscriptFileUri']
                print(f"Transcript available at: {transcript_uri}")
                
                # Download the transcript from the provided URL
                transcript = boto3.client('s3').get_object(Bucket='output-voice-bucket', Key=output_file_name)['Body'].read().decode('utf-8')

                # Save the final transcription result
                print("Transcript retrieved successfully.")
                # Simple return for next Lambda
                return {
                    'transcriptionText': transcript
                }
        if elapsed_time >= max_wait_time:
            print("Job timed out.")
            return {'statusCode': 500, 'body': "Transcription job timed out"}

        if job_status == 'FAILED':
            print("Transcription job failed.")
            return {'statusCode': 500, 'body': "Transcription job failed"}

    except Exception as e:
        print(f"Error: {e}")
        return {'statusCode': 500, 'body': f"An error occurred: {e}"}
