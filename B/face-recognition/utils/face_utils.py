from datetime import datetime
from utils.aws_utils import get_aws_clients, get_config

clients = get_aws_clients()
config = get_config()

def upload_image_to_s3(file_path, s3_key):
    print(f"Debug - Bucket: {config.get('bucket')}")
    print(f"Debug - Config: {config}")
    clients['s3'].upload_file(file_path, config['bucket'], s3_key)
    print(f"✅ Uploaded {file_path} to S3 as {s3_key}")

def detect_faces(image_bytes):
    response = clients['rekognition'].detect_faces(
        Image={'Bytes': image_bytes},
        Attributes=['ALL']
    )
    return response['FaceDetails']

def search_face_in_collection(image_bytes, threshold=80):
    try:
        response = clients['rekognition'].search_faces_by_image(
            CollectionId=config['collection_id'],
            Image={'Bytes': image_bytes},
            MaxFaces=1,
            FaceMatchThreshold=threshold
        )
        return response
    except Exception as e:
        print(f"❌ Error searching faces: {str(e)}")
        return None

def index_new_face(image_bytes):
    try:
        response = clients['rekognition'].index_faces(
            CollectionId=config['collection_id'],
            Image={'Bytes': image_bytes},
            DetectionAttributes=['DEFAULT'],
            QualityFilter='AUTO'
        )
        return response
    except Exception as e:
        print(f"❌ Error indexing face: {str(e)}")
        return None

def get_customer(face_id):
    try:
        table = clients['dynamodb'].Table(config['table_name'])
        response = table.get_item(Key={'CustomerID': face_id})
        return response.get('Item')
    except Exception as e:
        print(f"❌ Error getting customer: {str(e)}")
        return None

def repair_missing_customer(face_id):
    """Attempt to recover when face exists in Rekognition but not in DB"""
    try:
        # Get face details from Rekognition
        response = clients['rekognition'].get_face(
            CollectionId=config['collection_id'],
            FaceId=face_id
        )
        
        if response.get('Face'):
            print("\n⚠️ Found orphaned face in Rekognition collection")
            name = input("Enter customer name to recreate record: ").strip()
            member_id = input("Enter member ID (or leave blank): ").strip() or None
            
            # Create a dummy S3 key since we don't have the original
            s3_key = f"recovered_faces/{face_id}.jpg"
            
            if add_customer(face_id, name, s3_key, member_id):
                print(f"✅ Successfully recreated customer record for {name}")
                return True
    except Exception as e:
        print(f"❌ Error repairing customer: {str(e)}")
    return False

def cleanup_orphaned_faces():
    """Remove faces from Rekognition that have no DB record"""
    try:
        # List all faces in collection
        response = clients['rekognition'].list_faces(
            CollectionId=config['collection_id']
        )
        
        orphan_count = 0
        for face in response.get('Faces', []):
            face_id = face['FaceId']
            if not get_customer(face_id):
                clients['rekognition'].delete_faces(
                    CollectionId=config['collection_id'],
                    FaceIds=[face_id]
                )
                print(f"Removed orphaned face: {face_id}")
                orphan_count += 1
                
        print(f"✅ Cleanup complete. Removed {orphan_count} orphaned faces.")
        return orphan_count
    except Exception as e:
        print(f"❌ Error during cleanup: {str(e)}")
        return 0
    
def add_customer(face_id, name, s3_key, member_id=None):
    try:
        table = clients['dynamodb'].Table(config['table_name'])
        item = {
            'CustomerID': face_id,
            'name': name,
            's3_key': s3_key,
            'member_id': member_id,
            'registration_date': datetime.now().isoformat()
        }
        table.put_item(Item=item)
        print(f"✅ Customer {name} added with Face ID {face_id}")
        if member_id:
            print(f"Member ID: {member_id}")
        return True
    except Exception as e:
        print(f"❌ Error adding customer: {str(e)}")
        return False