import boto3

def lambda_handler(event, context):
    try:
        # Retrieve the transcription text directly from the event
        transcript_text = event.get('transcriptionText', '')
        if not transcript_text:
            print("No transcription text found in the event.")
            return {
                'statusCode': 400,
                'body': "Invalid input, expected 'transcriptionText' in the event"
            }

        print(f"Received transcription text: {transcript_text}")

        # Translate the transcription text from Hindi to English
        translate_client = boto3.client('translate')
        translation_response = translate_client.translate_text(
            Text=transcript_text,
            SourceLanguageCode='hi',
            TargetLanguageCode='en'
        )

        # Get the translated text
        translated_text = translation_response['TranslatedText']
        print("Translated text: ", translated_text)

        # Simple return for next Lambda
        return {
            'translatedText': translated_text
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': f"An error occurred: {e}"
        }
