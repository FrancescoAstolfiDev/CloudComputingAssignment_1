from typing import Optional, Dict, Any, List
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure, OperationFailure, PyMongoError
from .config import settings


class MongoDBManager:
    """Class for handle the operations with MongoDB"""

    _instance: Optional['MongoDBManager'] = None
    _client: Optional[MongoClient] = None
    _db: Optional[Database] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.connection_string = self._build_connection_string()

    def _build_connection_string(self) -> str:
        """build the connection string for MongoDB"""
        return (
            f"mongodb+srv://{settings.mongodb_username}:"
            f"{settings.mongodb_password.get_secret_value()}@"
            f"{settings.mongodb_cluster}/"
            f"{settings.mongodb_db}?"
            f"retryWrites=true&w=majority"
        )

    def connect(self) -> Database:
        """Create a connection to the Mongodb database"""
        try:
            if self._client is None:
                self._client = MongoClient(
                    self.connection_string,
                    maxPoolSize=50,
                    connectTimeoutMS=30000,
                    socketTimeoutMS=30000
                )

                # Test of connection
                self._client.admin.command('ping')
                print("✅ Connected with mongoDB!")

                # Seleziona il database
                self._db = self._client[settings.mongodb_db]

            return self._db

        except ConnectionFailure as e:
            print(f"❌ Error of connection: {e}")
            raise
        except OperationFailure as e:
            print(f"❌ Error of operation: {e}")
            raise
        except Exception as e:
            print(f"❌ Unprevist error: {e}")
            raise

    def get_database(self) -> Database:
        """Return the db Instance"""
        if self._db is None:
            return self.connect()
        return self._db

    def get_collection(self, collection_name: str) -> Collection:
        """Return a specific collection"""
        db = self.get_database()
        return db[collection_name]

    def insert_document(self, collection_name: str, document: Dict[str, Any]) -> str:
        """Insert a document into the collection"""
        try:
            collection = self.get_collection(collection_name)
            result = collection.insert_one(document)
            return str(result.inserted_id)
        except PyMongoError as e:
            print(f"❌ Error during the input: {e}")
            raise

    def find_documents(self, collection_name: str, query: Dict[str, Any] = None,
                       projection: Dict[str, Any] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Find the document in the collection"""
        try:
            collection = self.get_collection(collection_name)
            query = query or {}
            projection = projection or {}

            cursor = collection.find(query, projection).limit(limit)
            documents = list(cursor)

            # Convert ObjectId to string for JSON serialization
            for doc in documents:
                if '_id' in doc:
                    doc['_id'] = str(doc['_id'])

            return documents
        except PyMongoError as e:
            print(f"❌ Error during the research: {e}")
            raise

    def find_one(self, collection_name: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find one document in the collection"""
        try:
            collection = self.get_collection(collection_name)
            document = collection.find_one(query)

            if document and '_id' in document:
                document['_id'] = str(document['_id'])

            return document
        except PyMongoError as e:
            print(f"❌ Error on the research-phase: {e}")
            raise

    def update_document(self, collection_name: str, query: Dict[str, Any],
                        update_data: Dict[str, Any]) -> int:
        """Update a document"""
        try:
            collection = self.get_collection(collection_name)
            result = collection.update_one(query, {'$set': update_data})
            return result.modified_count
        except PyMongoError as e:
            print(f"❌ Error on the update : {e}")
            raise

    def delete_document(self, collection_name: str, query: Dict[str, Any]) -> int:
        """Delete a document"""
        try:
            collection = self.get_collection(collection_name)
            result = collection.delete_one(query)
            return result.deleted_count
        except PyMongoError as e:
            print(f"❌  Error during the elimination: {e}")
            raise

    def count_documents(self, collection_name: str, query: Dict[str, Any] = None) -> int:
        """Count the num of documents in the collection"""
        try:
            collection = self.get_collection(collection_name)
            query = query or {}
            return collection.count_documents(query)
        except PyMongoError as e:
            print(f"❌ Error during the count phase : {e}")
            raise

    def close_connection(self):
        """Close the connection with MongoDB"""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
            print("✅ Connection closed with MongoDB!")

    def is_connected(self) -> bool:
        """Verify if the connection is open"""
        try:
            if self._client:
                self._client.admin.command('ping')
                return True
            return False
        except:
            return False

    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close_connection()


# Istanza globale del database manager
db_manager = MongoDBManager()


# Funzioni di utilità per FastAPI dependencies
def get_db_manager() -> MongoDBManager:
    """Return the db manager (for FastAPI Depends)"""
    return db_manager


def get_database() -> Database:
    """Return the db Instance (for FastAPI Depends)"""
    return db_manager.get_database()

if __name__ == "__main__":
    get_database()