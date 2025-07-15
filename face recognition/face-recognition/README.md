# Face Recognition & Purchase Summary System

## Project Overview

This project is a comprehensive Python-based application that integrates computer vision, cloud computing, and API calling technologies to achieve face recognition and member purchase information query functions. The system uses OpenCV to capture face images from the camera, employs AWS Rekognition for face recognition to match corresponding customer information. Once the face is recognized successfully, the program logs in to the Stickie API to retrieve detailed member information and purchase records, and then summarizes and displays the purchase records.

## Features

1. **Automatic Face Capture**: Using the OpenCV library, the program can automatically detect faces in the camera and capture a clear face image automatically after a 2-second delay once a face is detected.
2. **High-precision Face Recognition**: Leveraging the powerful capabilities of AWS Rekognition, it can quickly and accurately search for matching faces in the specified face collection. The matching threshold can be adjusted according to requirements.
3. **Member Information Query**: Through the Stickie API, the system can obtain the member's basic information (such as name, email, phone number, etc.) and detailed purchase records.
4. **Purchase Record Summarization**: Intelligently summarizes the member's purchase records, counting the total purchase quantity and the last purchase date of each product for easy viewing.
5. **Data Cleaning and Repair**: Provides the function to clean up orphaned faces in Rekognition (i.e., faces that exist in the Rekognition collection but have no corresponding records in the database). It also supports repairing missing customer records.

## Installation Steps

### 1.Clone the Repository
First, you need to clone the project repository to your local machine. Open the terminal or command prompt and execute the following command:
```
git clone <repository-url>
cd face-recognition
```
### 2. Create and Activate a Virtual Environment (Optional but Recommended)
To avoid conflicts between project dependencies and the system environment, it is recommended to create a virtual environment. Execute the following command:
``` python -m venv venv ```
Activate the virtual environment:
- **Linux/MacOS**:
``` source venv/bin/activate ```
- **Windows**:
``` venv\Scripts\activate ```
### 3. Install Dependencies
After activating the virtual environment, use the following command to install the project's required dependencies:
``` pip install -r requirements.txt ```
### 4. Configure Environment Variables
Create a ``` .env ```file in the project root directory and add the following environment variables:
```
S3_BUCKET=<your-S3-bucket-name>
DYNAMODB_TABLE=<your-DynamoDB-table-name>
REKOGNITION_COLLECTION=<your-Rekognition-collection-name>
```
Please ensure that you replace **<your-S3-bucket-name>**, **<your-DynamoDB-table-name>**, and **<your-Rekognition-collection-name>** with your own AWS resource names.

## Usage

### Run the Main Program
After completing the above installation and configuration steps, you can run the main program:
``` python app5.py ```

### Detailed Process
1. **Face Capture**: After the program starts, the camera will open and start detecting faces. When a face is detected, a countdown will be displayed on the screen, and the face image will be automatically captured after 2 seconds.
2. **Face Recognition**: The captured face image will be sent to AWS Rekognition for matching. If a match is found, the matched face ID and matching confidence will be displayed.
3. **Member Information Query**: Based on the matched face ID, the program will retrieve the corresponding customer information from DynamoDB. If the customer information exists, the program will log in to the Stickie API to obtain the member's detailed information and purchase records.
4. **Result Display**: Finally, the program will display the member's basic information (such as name, email, phone number, etc.) and a summary of the purchase records, including the total purchase quantity and the last purchase date of each product.

## Code Structure
```
face-recognition/
├── app5.py              # The main program entry, containing the main logic of face capture, face recognition, member information query, and result display.
├── utils/
│   ├── aws_utils.py     # AWS client and configuration acquisition tools, responsible for creating clients for AWS services and obtaining relevant configuration information.
│   └── face_utils.py    # Face processing-related tools, including image upload, face detection, face recognition, customer information retrieval, etc.
├── .env                 # Environment variable configuration file, storing the names of AWS resources.
└── requirements.txt     # List of dependencies, listing the Python libraries required by the project.
```

## Notes
1. **AWS Credential Configuration**: Please ensure that your AWS credentials are correctly configured. You can configure them through the ~/.aws/credentials file. This file should contain your AWS access key and secret access key.
2. **Stickie API Login Information**: Currently, the Stickie API login information (email and password) is hard-coded in the **app5.py** file. In a production environment, it is recommended to store this information in a secure location, such as an environment variable, and retrieve it by reading the environment variable.
3. **Temporary File Handling**: The captured face image will be temporarily saved as a local file and automatically deleted after the program ends. If an exception occurs during the program execution, the temporary file may not be deleted. You can manually clean up these files.

## License
This project is licensed under the MIT License. You are free to use, modify, and distribute this project, but you need to retain the license file and copyright notice.

## Frequently Asked Questions (FAQ)

### 1. Why can't the program open the camera?
Possible reasons include camera device failure, permission issues, or another program is already using the camera. Please check if the camera device is working properly, ensure that your program has permission to access the camera, and close other programs that are using the camera.
### 2. What should I do if face recognition fails?
Face recognition failure may be due to poor face image quality, no matching face in the face collection, or issues with the Rekognition service. You can try to recapture the face image, ensuring that the image is clear, frontal, and well-lit. If the problem persists, please check the configuration and status of the AWS Rekognition service.
### 3. How can I modify the Stickie API login information?
You can find the login_to_stickie function in the **app5.py** file and modify the payload dictionary inside it. Replace the email and password fields with your own login information. In a production environment, it is recommended to store this information in an environment variable and retrieve it using the os.getenv function.
### 4. How can I clean up orphaned faces in Rekognition?
You can call the cleanup_orphaned_faces function in the **face_utils.py** file. This function will automatically check the faces in the Rekognition collection and delete the orphaned faces that have no corresponding records in DynamoDB.
### 5. How can I repair missing customer records?
If a face exists in the Rekognition collection but has no corresponding record in DynamoDB, you can call the repair_missing_customer function in the **face_utils.py** file. This function will prompt you to enter the customer's name and member ID and attempt to recreate the customer record.

