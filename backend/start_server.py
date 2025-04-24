import os
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get configuration from environment
port = int(os.getenv("PORT", 8000))
log_level = os.getenv("LOG_LEVEL", "info").lower()

if __name__ == "__main__":
    print(f"Starting Video Watermark Removal API on port {port}")
    print("Press CTRL+C to stop the server")
    
    # Run the server
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=port, 
        log_level=log_level,
        reload=True
    ) 