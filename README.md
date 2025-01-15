# Serverless Application for Transcription, Translation, and Audio Processing

This project implements a serverless application using AWS services to handle audio transcription, translation, and audio playback generation. The application utilizes AWS Step Functions to orchestrate multiple AWS Lambda functions, along with AWS S3, Polly, Translate, and API Gateway to build an end-to-end automated pipeline.

## Features

- **Audio Transcription**: Processes audio files to generate text transcription.
- **Language Translation**: Translates transcriptions from Hindi to English.
- **Audio Playback Generation**: Converts translated text back into audio.
- **User-Friendly UI**: Allows file uploads, triggers the processing pipeline, displays real-time transcription and translation results, and includes an audio player for playback.
- **Secure and Seamless Integration**: Ensures smooth interaction between AWS resources using IAM roles and permissions.

---

## Architecture Overview

The architecture consists of:

1. **AWS S3**: Used for storing input audio files, intermediary text files, and final audio outputs.
2. **AWS Lambda**: Handles the core logic for transcription, translation, and audio generation.
3. **AWS Step Functions**: Coordinates the execution of Lambda functions.
4. **AWS Translate**: Translates the transcription text into the desired language.
5. **AWS Polly**: Converts translated text into speech.
6. **AWS API Gateway**: Provides a RESTful API interface for interacting with the application.

---

## Step-by-Step Setup

### 1. **Prerequisites**
- AWS account with necessary permissions.
- Python environment with the AWS CLI and Boto3 installed.

### 2. **AWS Services Setup**

#### **IAM Roles**
Create an IAM role with the following policies:

- **Lambda Execution Role**: Grants Lambda functions permission to interact with S3, Translate, Polly, and Step Functions.
- **Step Functions Execution Role**: Grants Step Functions permission to invoke Lambda functions.

#### **S3 Buckets**
- `input-voice-bucket`: For uploading input audio files.
- `output-voice-data`: For storing generated audio files.

---

### 3. **Lambda Functions**

#### **Lambda 1: Process Input Audio**
Extracts audio files from S3 and generates transcription text.
```python
import boto3
...
```

#### **Lambda 2: Translate Text**
Translates transcription text from Hindi to English.
```python
import boto3
...
```

#### **Lambda 3: Generate Audio**
Converts translated text into an audio file using Polly.
```python
import boto3
...
```

---

### 4. **AWS Step Functions**

#### **State Machine Definition**
A JSON definition for the Step Functions workflow:

```json
{
  "Comment": "Serverless application pipeline",
  ...
}
```

---

### 5. **User Interface (UI)**
The UI allows users to:

- Upload audio files.
- Trigger Step Functions execution.
- View transcription and translation results.
- Play generated audio.

#### **Frontend Stack**
- **HTML/CSS/JavaScript**: Build the UI.
- **AWS API Gateway**: Connects the UI to backend services.

---

### Deployment Instructions

1. Deploy Lambda functions.
2. Set up S3 buckets.
3. Configure Step Functions with state machine JSON.
4. Deploy API Gateway endpoints.
5. Integrate UI with API Gateway.

---

## Example Workflow

1. Upload an audio file via the UI.
2. The file is stored in `input-voice-bucket`.
3. Step Functions triggers the first Lambda for transcription.
4. The second Lambda translates the transcription text.
5. The third Lambda generates an audio file from the translation.
6. The audio file is saved in `output-voice-data` and is accessible via the UI.

---

## Key AWS Policies

### Lambda Execution Policy
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:*",
        "translate:TranslateText",
        "polly:SynthesizeSpeech",
        "states:StartExecution"
      ],
      "Resource": "*"
    }
  ]
}
```

### Step Functions Policy
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "lambda:InvokeFunction",
      "Resource": "arn:aws:lambda:<region>:<account-id>:function:*"
    }
  ]
}
```

---

## Testing

1. **Lambda Function Unit Testing**:
   - Use mock events for each Lambda function.
2. **Step Functions Workflow**:
   - Test with a complete input JSON to ensure smooth transitions.
3. **End-to-End Testing**:
   - Upload audio via the UI and validate outputs at each stage.

---

## Conclusion

This project showcases an efficient, scalable serverless architecture for audio processing tasks. By leveraging AWS services, it provides a seamless pipeline for transcription, translation, and audio generation with minimal infrastructure management.

