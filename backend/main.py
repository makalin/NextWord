
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import random
import json
import speech_recognition as sr
import io
import wave
import pyaudio
import threading
import base64
import tempfile
import os
from pydub import AudioSegment
from pydub.utils import which
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware
import os
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173,http://localhost:5174").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>NextWord Backend</title>
    </head>
    <body>
        <h1>NextWord Backend</h1>
        <p>WebSocket endpoint at /ws</p>
        <p>Status: Running with simulated transcript generation</p>
    </body>
</html>
"""

# AI-powered idea prediction and cognitive assistance
import random
import time
import re

# Speech Recognition Settings
SPEECH_SETTINGS = {
    "language": "en-US",
    "confidence_threshold": 0.7,
    "use_google_cloud": False,  # Set to True if you have Google Cloud credentials
    "google_cloud_credentials_path": None,  # Path to Google Cloud credentials JSON
    "fallback_to_offline": True,
    "audio_format": "webm",  # Default format from MediaRecorder
    "sample_rate": 44100,
    "channels": 1
}

# Initialize speech recognition
recognizer = sr.Recognizer()
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8
recognizer.phrase_threshold = 0.3
recognizer.non_speaking_duration = 0.8

def convert_audio_format(audio_data):
    """Convert audio data from MediaRecorder format to WAV for speech recognition"""
    try:
        # Try different approaches for audio conversion
        
        # Method 1: Try to detect if it's already WAV data
        if audio_data.startswith(b'RIFF'):
            logger.info("Audio data appears to be WAV format")
            return audio_data
        
        # Method 2: Try WebM conversion with error handling
        try:
            with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_file_path = temp_file.name
            
            # Try to load as WebM
            audio = AudioSegment.from_file(temp_file_path, format="webm")
            
            # Convert to WAV
            wav_data = io.BytesIO()
            audio.export(wav_data, format="wav")
            wav_data.seek(0)
            
            # Clean up
            os.unlink(temp_file_path)
            
            return wav_data.getvalue()
            
        except Exception as webm_error:
            logger.warning(f"WebM conversion failed: {webm_error}")
            
            # Method 3: Try to create a simple WAV from raw data
            try:
                # Assume it's raw PCM data and create a simple WAV
                sample_rate = 44100
                channels = 1
                sample_width = 2  # 16-bit
                
                # Create WAV header
                wav_header = wave.struct.pack('<HHIIHH', 
                    1,  # Format (PCM)
                    channels,  # Channels
                    sample_rate,  # Sample rate
                    sample_rate * channels * sample_width,  # Byte rate
                    channels * sample_width,  # Block align
                    sample_width * 8  # Bits per sample
                )
                
                # Create WAV file
                wav_data = io.BytesIO()
                wav_data.write(b'RIFF')
                wav_data.write(wave.struct.pack('<I', len(audio_data) + 36))
                wav_data.write(b'WAVE')
                wav_data.write(b'fmt ')
                wav_data.write(wave.struct.pack('<I', 16))
                wav_data.write(wav_header)
                wav_data.write(b'data')
                wav_data.write(wave.struct.pack('<I', len(audio_data)))
                wav_data.write(audio_data)
                
                return wav_data.getvalue()
                
            except Exception as raw_error:
                logger.error(f"Raw audio conversion failed: {raw_error}")
                return None
        
    except Exception as e:
        logger.error(f"Audio format conversion error: {e}")
        return None

def transcribe_audio(audio_data):
    """Convert audio data to text using speech recognition"""
    try:
        logger.info(f"Received audio data: {len(audio_data)} bytes")
        
        if len(audio_data) < 1000:  # Too small for meaningful audio
            logger.info("Audio data too small, skipping")
            return ""
        
        # Try to convert audio format for real speech recognition
        wav_data = convert_audio_format(audio_data)
        if wav_data:
            try:
                # Use real speech recognition
                audio_file = io.BytesIO(wav_data)
                with sr.AudioFile(audio_file) as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = recognizer.record(source)
                    text = recognizer.recognize_google(audio, language=SPEECH_SETTINGS["language"])
                    logger.info(f"Real speech recognized: {text}")
                    return text
            except sr.UnknownValueError:
                logger.info("Could not understand audio")
                return ""
            except sr.RequestError as e:
                logger.error(f"Speech recognition service error: {e}")
                return ""
            except Exception as e:
                logger.error(f"Speech recognition error: {e}")
                return ""
        else:
            logger.info("Audio conversion failed, no transcript generated")
            return ""
        
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        return ""

def analyze_real_speech(text):
    """Analyze real speech content for ideas and tags using AI"""
    if not text or len(text.strip()) < 3:
        return {"ideas": [], "tags": [], "confidence": 0}
    
    logger.info(f"Analyzing speech: '{text}'")
    
    # Extract key concepts and generate AI-powered analysis
    words = text.lower().split()
    
    # AI-powered topic extraction based on content analysis
    ideas = []
    tags = []
    
    # Analyze the actual content for intelligent suggestions
    if any(word in text.lower() for word in ["focus", "important", "priorities", "key", "main"]):
        ideas = [
            f"Deep dive into the core aspects of: {text[:50]}...",
            "Prioritization matrix development",
            "Critical path analysis for this topic",
            "Stakeholder impact assessment"
        ]
        tags = ["Priority", "Focus", "Strategy", "Analysis"]
        
    elif any(word in text.lower() for word in ["think", "believe", "consider", "should", "need"]):
        ideas = [
            f"Explore different perspectives on: {text[:50]}...",
            "Alternative approaches and solutions",
            "Risk-benefit analysis",
            "Implementation roadmap"
        ]
        tags = ["Thinking", "Analysis", "Solutions", "Planning"]
        
    elif any(word in text.lower() for word in ["problem", "issue", "challenge", "difficult"]):
        ideas = [
            f"Root cause analysis for: {text[:50]}...",
            "Solution brainstorming session",
            "Resource allocation for problem-solving",
            "Success metrics definition"
        ]
        tags = ["Problem-Solving", "Solutions", "Strategy", "Analysis"]
        
    elif any(word in text.lower() for word in ["business", "company", "market", "customer", "revenue"]):
        ideas = [
            f"Business strategy development for: {text[:50]}...",
            "Market opportunity analysis",
            "Competitive advantage identification",
            "Revenue optimization strategies"
        ]
        tags = ["Business", "Strategy", "Market", "Growth"]
        
    elif any(word in text.lower() for word in ["technology", "software", "system", "development", "code"]):
        ideas = [
            f"Technical architecture for: {text[:50]}...",
            "Performance optimization strategies",
            "Security and scalability considerations",
            "User experience enhancement"
        ]
        tags = ["Technology", "Development", "Innovation", "Architecture"]
        
    elif any(word in text.lower() for word in ["creative", "design", "art", "visual", "aesthetic"]):
        ideas = [
            f"Creative exploration of: {text[:50]}...",
            "Design thinking methodology",
            "Visual concept development",
            "Brand identity enhancement"
        ]
        tags = ["Creative", "Design", "Innovation", "Visual"]
        
    else:
        # General AI analysis for any other content
        ideas = [
            f"Comprehensive analysis of: {text[:50]}...",
            "Multi-perspective exploration",
            "Implementation strategies",
            "Success measurement framework"
        ]
        tags = ["Analysis", "Strategy", "Implementation", "Planning"]
    
    # Calculate confidence based on content quality and length
    confidence = min(95, 70 + len(text.split()) * 3)
    
    logger.info(f"AI Analysis result: ideas={len(ideas)}, tags={len(tags)}, confidence={confidence}")
    
    return {
        "ideas": ideas[:3],  # Top 3 ideas
        "tags": tags[:4],    # Top 4 tags
        "confidence": confidence
    }

# Idea prediction based on sentence context
idea_predictions = {
    "tree": {
        "contexts": ["planting", "growing", "forest", "nature", "environment", "garden", "park"],
        "next_ideas": [
            "Tree species selection", "Soil preparation", "Watering schedule", "Pruning techniques",
            "Seasonal care", "Pest management", "Growth monitoring", "Environmental benefits",
            "Carbon sequestration", "Wildlife habitat", "Shade benefits", "Root system development"
        ],
        "related_tags": ["Botany", "Gardening", "Ecology", "Sustainability", "Landscaping", "Conservation"]
    },
    "business": {
        "contexts": ["strategy", "growth", "market", "revenue", "customer", "product", "service"],
        "next_ideas": [
            "Market analysis", "Customer segmentation", "Revenue optimization", "Competitive positioning",
            "Product development", "Marketing strategy", "Sales funnel", "Customer retention",
            "Business model", "Partnership opportunities", "Scaling strategy", "Risk management"
        ],
        "related_tags": ["Strategy", "Marketing", "Sales", "Finance", "Operations", "Leadership"]
    },
    "technology": {
        "contexts": ["software", "development", "coding", "programming", "system", "application", "platform"],
        "next_ideas": [
            "Architecture design", "Database optimization", "API development", "Security implementation",
            "Performance tuning", "User interface", "Testing strategy", "Deployment pipeline",
            "Monitoring setup", "Scalability planning", "Integration approach", "Maintenance strategy"
        ],
        "related_tags": ["Development", "Architecture", "Security", "DevOps", "UI/UX", "Testing"]
    },
    "creative": {
        "contexts": ["design", "art", "creative", "visual", "aesthetic", "brand", "style"],
        "next_ideas": [
            "Color palette", "Typography selection", "Layout design", "Visual hierarchy",
            "Brand identity", "User experience", "Creative process", "Inspiration sources",
            "Design principles", "Prototype development", "Feedback integration", "Final refinement"
        ],
        "related_tags": ["Design", "Art", "Branding", "UI/UX", "Visual", "Creative"]
    },
    "research": {
        "contexts": ["study", "analysis", "data", "experiment", "hypothesis", "findings", "conclusion"],
        "next_ideas": [
            "Research methodology", "Data collection", "Statistical analysis", "Literature review",
            "Hypothesis testing", "Results interpretation", "Peer review", "Publication strategy",
            "Further research", "Limitations analysis", "Recommendations", "Future studies"
        ],
        "related_tags": ["Research", "Analysis", "Data", "Statistics", "Methodology", "Academic"]
    }
}

def analyze_sentence_context(sentence):
    """Analyze sentence to predict next ideas and related tags"""
    sentence_lower = sentence.lower()
    
    # Find the most relevant context
    best_match = None
    max_score = 0
    
    for topic, data in idea_predictions.items():
        score = 0
        for context in data["contexts"]:
            if context in sentence_lower:
                score += 1
        if score > max_score:
            max_score = score
            best_match = topic
    
    if best_match:
        return idea_predictions[best_match]
    else:
        # Default to general ideas
        return {
            "next_ideas": ["Continue your thought", "Explore further", "Consider alternatives", "Develop the concept"],
            "related_tags": ["General", "Ideas", "Development", "Exploration"]
        }

def get_idea_suggestions(sentence):
    """Get next idea suggestions based on sentence context"""
    context_data = analyze_sentence_context(sentence)
    return random.sample(context_data["next_ideas"], min(3, len(context_data["next_ideas"])))

def get_related_tags(sentence):
    """Get related tags based on sentence context"""
    context_data = analyze_sentence_context(sentence)
    return random.sample(context_data["related_tags"], min(4, len(context_data["related_tags"])))

def calculate_idea_confidence(sentence):
    """Calculate confidence percentage for idea suggestions"""
    # Simple confidence calculation based on sentence length and context matches
    words = len(sentence.split())
    context_matches = 0
    
    for topic, data in idea_predictions.items():
        for context in data["contexts"]:
            if context in sentence.lower():
                context_matches += 1
    
    base_confidence = min(95, 60 + (words * 2) + (context_matches * 10))
    return base_confidence

def analyze_document_content(document_text):
    """Analyze uploaded document content for better context"""
    document_lower = document_text.lower()
    
    # Enhanced context detection based on document content
    enhanced_contexts = {
        "business": ["strategy", "market", "revenue", "customer", "product", "service", "growth", "profit", "sales", "marketing"],
        "technology": ["software", "development", "coding", "programming", "system", "application", "platform", "api", "database", "security"],
        "creative": ["design", "art", "creative", "visual", "aesthetic", "brand", "style", "color", "typography", "layout"],
        "research": ["study", "analysis", "data", "experiment", "hypothesis", "findings", "conclusion", "methodology", "statistics", "results"],
        "tree": ["planting", "growing", "forest", "nature", "environment", "garden", "park", "soil", "water", "growth", "species"]
    }
    
    # Find the most relevant context from document
    best_match = None
    max_score = 0
    
    for topic, keywords in enhanced_contexts.items():
        score = sum(1 for keyword in keywords if keyword in document_lower)
        if score > max_score:
            max_score = score
            best_match = topic
    
    if best_match and best_match in idea_predictions:
        return idea_predictions[best_match]
    else:
        # Return general enhanced suggestions based on document content
        return {
            "next_ideas": [
                "Document analysis", "Content review", "Key insights", "Main points", 
                "Summary creation", "Further research", "Implementation plan", "Next steps"
            ],
            "related_tags": ["Document", "Analysis", "Content", "Review", "Insights"]
        }

def get_document_enhanced_suggestions(document_text, current_speech):
    """Generate suggestions based on both document content and current speech"""
    doc_context = analyze_document_content(document_text)
    speech_context = analyze_sentence_context(current_speech)
    
    # Combine both contexts for richer suggestions
    combined_ideas = list(set(doc_context["next_ideas"] + speech_context["next_ideas"]))
    combined_tags = list(set(doc_context["related_tags"] + speech_context["related_tags"]))
    
    return {
        "ideas": combined_ideas[:5],  # Top 5 combined ideas
        "tags": combined_tags[:4]    # Top 4 combined tags
    }

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.get("/settings")
async def get_settings():
    """Get current speech recognition settings"""
    return SPEECH_SETTINGS

@app.post("/settings")
async def update_settings(settings: dict):
    """Update speech recognition settings"""
    global SPEECH_SETTINGS
    SPEECH_SETTINGS.update(settings)
    
    # Update recognizer settings
    if "confidence_threshold" in settings:
        recognizer.energy_threshold = int(settings.get("confidence_threshold", 0.7) * 1000)
    
    logger.info(f"Settings updated: {settings}")
    return {"status": "success", "settings": SPEECH_SETTINGS}

@app.post("/analyze-speech")
async def analyze_speech(request: dict):
    """Analyze speech text and return AI suggestions"""
    text = request.get("text", "")
    
    if not text or len(text.strip()) < 3:
        return {"ideas": [], "tags": [], "confidence": 0}
    
    logger.info(f"Analyzing speech text: '{text}'")
    
    # Use the same AI analysis function
    result = analyze_real_speech(text)
    
    logger.info(f"AI Analysis result: {result}")
    return result

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    session_transcript = ""
    current_context = None
    last_suggestion_time = 0
    suggestion_cooldown = 3.0  # Wait 3 seconds between suggestions
    document_context = ""  # Store uploaded document context
    
    try:
        while True:
            # Try to receive text first (for document analysis)
            try:
                data = await websocket.receive_text()
                if data.startswith('{'):
                    # JSON message for document analysis
                    import json
                    message = json.loads(data)
                    if message.get('type') == 'document_analysis':
                        document_context = message.get('content', '')
                        await websocket.send_text("Document analysis started...")
                        continue
                else:
                    # Regular text message, treat as audio data
                    data = data.encode()
            except:
                # If text receive fails, try bytes (audio data)
                try:
                    data = await websocket.receive_bytes()
                except:
                    # If both fail, break the loop
                    break
            
            current_time = time.time()
            
            # Simulate processing delay
            await asyncio.sleep(0.5)
            
            # Process real audio data
            logger.info(f"Processing audio data: {len(data)} bytes")
            if len(data) > 100:  # Minimum audio data threshold
                # Use real speech recognition
                real_transcript = transcribe_audio(data)
                if real_transcript:
                    simulated_transcript = real_transcript
                    session_transcript += real_transcript + " "
                    logger.info(f"Real speech detected: {real_transcript}")
                else:
                    simulated_transcript = ""
                    logger.info("No transcript generated from audio")
            else:
                # No meaningful audio detected, don't generate transcript
                simulated_transcript = ""
                logger.info("Audio data too small, skipping")
            
            logger.info(f"Final transcript: '{simulated_transcript}'")
            
            # Send transcript to frontend
            await websocket.send_text(f"transcript:{simulated_transcript}")
            
            # Only suggest ideas if there's actual speech content and enough time has passed
            logger.info(f"Checking if should generate ideas: transcript='{simulated_transcript}', words={len(simulated_transcript.split()) if simulated_transcript else 0}")
            if simulated_transcript.strip() and len(simulated_transcript.split()) > 2:
                logger.info("Generating ideas and tags...")
                # Use real speech analysis instead of simulated context
                speech_analysis = analyze_real_speech(simulated_transcript)
                logger.info(f"Speech analysis result: {speech_analysis}")
                
                if (current_time - last_suggestion_time > suggestion_cooldown or 
                    current_context != speech_analysis):
                    
                    # Use document-enhanced suggestions if document context is available
                    if document_context:
                        enhanced_suggestions = get_document_enhanced_suggestions(document_context, simulated_transcript)
                        logger.info(f"Sending enhanced suggestions: {enhanced_suggestions}")
                        for suggestion in enhanced_suggestions["ideas"]:
                            await websocket.send_text(f"idea:{suggestion}")
                        for tag in enhanced_suggestions["tags"]:
                            await websocket.send_text(f"tag:{tag}")
                    else:
                        # Use real speech analysis for ideas and tags
                        logger.info(f"Sending speech analysis: {speech_analysis}")
                        for suggestion in speech_analysis["ideas"]:
                            await websocket.send_text(f"idea:{suggestion}")
                        
                        for tag in speech_analysis["tags"]:
                            await websocket.send_text(f"tag:{tag}")
                    
                    # Send real confidence based on speech analysis
                    confidence = speech_analysis["confidence"]
                    if document_context:
                        confidence = min(95, confidence + 15)  # Boost confidence with document context
                    await websocket.send_text(f"confidence:{confidence}")
                    
                    current_context = speech_analysis
                    last_suggestion_time = current_time
                    logger.info("Ideas and tags sent successfully")
                else:
                    logger.info("Skipping suggestions due to cooldown or same context")
            else:
                logger.info("Not generating ideas - transcript too short or empty")
            
            # Send audio confirmation
            await websocket.send_text(f"Audio processed: {len(data)} bytes")
            
    except Exception as e:
        print(f"WebSocket error: {e}")
        try:
            await websocket.close()
        except:
            pass
