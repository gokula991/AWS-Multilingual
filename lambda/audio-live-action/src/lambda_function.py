import boto3

def lambda_handler(event, context):
    try:
        # Retrieve the translated text directly from the event
        translated_text = event.get('translatedText', '')
        if not translated_text:
            print("No translated text found in the event.")
            return {
                'statusCode': 400,
                'body': "Invalid input, expected 'translatedText' in the event"
            }

        print(f"Received translated text: {translated_text}")


        #Transform
        data = str(translated_text) # If the text is JSON formatted
        data = data.split('transcript')[2].split('items')
        transcript = data[0]

        # Set up Polly client
        polly_client = boto3.client('polly')
        s3_client = boto3.client('s3')

        # Use Polly to synthesize speech from the translated text
        response = polly_client.synthesize_speech(
            Text=transcript,
            OutputFormat='mp3',  # You can change the format if necessary
            VoiceId='Joanna'  # Choose a different voice if needed
        )

        # Specify the bucket and output file name
        output_bucket = 'output-voice-bucket'  # Replace with your output bucket name
        audio_file_key = 'output_audio.mp3'  # You can adjust this as needed

        # Save the resulting audio to S3
        s3_client.put_object(
            Bucket=output_bucket,
            Key=audio_file_key,
            Body=response['AudioStream'].read()
        )

        print(f"Audio file saved as {audio_file_key} in S3 bucket {output_bucket}")

        # Return the S3 URL for the generated audio file
        return {
            'statusCode': 200,
            'body': f"Audio file created and saved as s3://{output_bucket}/{audio_file_key}"
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': f"An error occurred: {e}"
        }
