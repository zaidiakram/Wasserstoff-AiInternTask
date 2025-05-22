class AppConfig:
    BACKEND_URL = "http://localhost:8080"
    MAX_FILE_SIZE_MB = 50
    SUPPORTED_FILE_TYPES = ["pdf", "docx", "txt"]
    DEFAULT_TOP_K = 5  # Number of documents to retrieve per query