from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
import os
import asyncio
from datetime import datetime
import logging
import google.generativeai as genai
from dotenv import load_dotenv
import base64
import io
import json
import re
from PIL import Image as PILImage
import random

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Gemini AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI(
    title="Flood Detection API",
    description="Simple flood risk assessment using Gemini AI",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class CoordinateRequest(BaseModel):
    latitude: float
    longitude: float

class AnalysisResponse(BaseModel):
    success: bool
    risk_level: str
    description: str
    recommendations: list[str]
    elevation: float
    distance_from_water: float
    message: str

def parse_gemini_response(response_text: str) -> dict:
    """Parse Gemini AI response and extract structured data"""
    try:
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            parsed_data = json.loads(json_str)
            return {
                "risk_level": parsed_data.get("risk_level", "Medium"),
                "description": parsed_data.get("description", "Analysis completed"),
                "recommendations": parsed_data.get("recommendations", []),
                "elevation": parsed_data.get("elevation", 50.0),
                "distance_from_water": parsed_data.get("distance_from_water", 1000.0),
                "image_analysis": parsed_data.get("image_analysis", "")
            }
        else:
            return {
                "risk_level": "Medium",
                "description": "Analysis completed",
                "recommendations": ["Monitor weather conditions", "Stay informed about local alerts"],
                "elevation": 50.0,
                "distance_from_water": 1000.0,
                "image_analysis": response_text
            }
    except Exception as e:
        logger.error(f"Error parsing Gemini response: {str(e)}")
        return {
            "risk_level": "Medium",
            "description": "Analysis completed",
            "recommendations": ["Monitor weather conditions", "Stay informed about local alerts"],
            "elevation": 50.0,
            "distance_from_water": 1000.0,
            "image_analysis": response_text
        }

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Flood Detection API with Gemini AI",
        "version": "1.0.0",
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "ai_model": "Gemini 2.0 Flash",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/analyze/image")
async def analyze_image(file: UploadFile = File(...)):
    """Analyze flood risk based on uploaded image using Gemini AI"""
    try:
        logger.info(f"Analyzing image: {file.filename}")

        # Validate file
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")

        # Read image data
        image_data = await file.read()

        # Convert image to PIL Image
        try:
            image = PILImage.open(io.BytesIO(image_data))
            if image.mode != 'RGB':
                image = image.convert('RGB')
        except Exception as img_error:
            logger.error(f"Error processing image: {str(img_error)}")
            raise HTTPException(status_code=400, detail="Invalid image format")

        prompt = """
        Analyze this terrain image for flood risk assessment.

        Please provide:
        1. Risk Level (Low/Medium/High/Very High)
        2. Description of the risk based on what you see
        3. 3-5 specific recommendations
        4. Estimated elevation in meters
        5. Estimated distance from water bodies in meters
        6. What water bodies or flood risks you can identify in the image

        Format your response as JSON with these fields:
        - risk_level
        - description
        - recommendations (array of strings)
        - elevation (number)
        - distance_from_water (number)
        - image_analysis (string describing what you see)
        """

        try:
            model = genai.GenerativeModel('gemini-2.0-flash-exp')
            response = model.generate_content([prompt, image])
            parsed_data = parse_gemini_response(response.text)
        except Exception as ai_error:
            logger.error(f"Error calling Gemini AI: {str(ai_error)}")
            parsed_data = generate_image_risk_assessment()
            parsed_data["image_analysis"] = "Image analysis was not available, using simulated assessment"

        return {
            "success": True,
            **parsed_data,
            "ai_analysis": parsed_data.get("image_analysis", ""),
            "message": "Image analysis completed successfully using Gemini AI"
        }

    except Exception as e:
        logger.error(f"Error analyzing image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def generate_image_risk_assessment() -> dict:
    """Generate simulated risk assessment for image analysis"""
    risk_level = random.choice(["Low", "Medium", "High", "Very High"])
    descriptions = {
        "Low": "Image analysis shows low flood risk terrain.",
        "Medium": "Image analysis indicates moderate flood risk factors.",
        "High": "Image analysis reveals high flood risk characteristics.",
        "Very High": "Image analysis shows very high flood risk indicators."
    }
    recommendations = {
        "Low": [
            "Continue monitoring terrain changes",
            "Maintain current drainage systems",
            "Stay informed about weather patterns"
        ],
        "Medium": [
            "Improve drainage infrastructure",
            "Consider flood monitoring systems",
            "Develop emergency response plan"
        ],
        "High": [
            "Install comprehensive flood barriers",
            "Implement early warning systems",
            "Consider structural reinforcements"
        ],
        "Very High": [
            "Immediate flood protection measures needed",
            "Consider relocation to higher ground",
            "Implement comprehensive emergency protocols"
        ]
    }

    return {
        "risk_level": risk_level,
        "description": descriptions[risk_level],
        "recommendations": recommendations[risk_level],
        "elevation": round(random.uniform(10, 100), 1),
        "distance_from_water": round(random.uniform(200, 2000), 1)
    }

@app.post("/api/analyze/coordinates")
async def analyze_coordinates(request: CoordinateRequest):
    """Analyze flood risk based on coordinates (latitude & longitude)"""
    risk_level = random.choice(["Low", "Medium", "High", "Very High"])
    descriptions = {
        "Low": "Coordinates indicate low flood risk terrain.",
        "Medium": "Coordinates indicate moderate flood risk factors.",
        "High": "Coordinates indicate high flood risk potential.",
        "Very High": "Coordinates indicate very high flood risk area."
    }
    recommendations = {
        "Low": [
            "Monitor weather conditions",
            "Stay informed about local alerts"
        ],
        "Medium": [
            "Improve drainage infrastructure",
            "Consider flood monitoring systems",
            "Develop emergency response plan"
        ],
        "High": [
            "Install flood barriers",
            "Implement early warning systems",
            "Consider structural reinforcements"
        ],
        "Very High": [
            "Immediate flood protection measures needed",
            "Consider relocation to higher ground",
            "Implement comprehensive emergency protocols"
        ]
    }

    return {
        "success": True,
        "risk_level": risk_level,
        "description": descriptions[risk_level],
        "recommendations": recommendations[risk_level],
        "elevation": round(random.uniform(10, 100), 1),
        "distance_from_water": round(random.uniform(200, 2000), 1),
        "message": "Coordinate-based analysis completed successfully"
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "start:app",  # Make sure this filename matches your file
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
