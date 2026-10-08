#!/usr/bin/env python3
"""
Smart Agriculture Platform (SAP) — FastAPI Backend Server
Real Crop Disease AI Pipeline + Agricultural Intelligence APIs
"""

import os
import sys
import json
import base64
import traceback
import asyncio
from typing import Optional

# Enable UTF-8 encoding on console output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from fastapi import FastAPI, UploadFile, File, Form, Request, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Add current workspace to sys.path first, then nested project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
NESTED_DIR = os.path.join(BASE_DIR, 'final sap project', 'final sap project')
if NESTED_DIR not in sys.path and os.path.isdir(NESTED_DIR):
    sys.path.append(NESTED_DIR)

# Import real AI crop disease analyzer
try:
    from disease_analyzer import analyze_plant_disease
except Exception as e:
    def analyze_plant_disease(*args, **kwargs):
        return {"success": False, "error": str(e), "message": "Disease analyzer unavailable."}

# Import existing platform helpers from original server module
try:
    import legacy_helpers as platform_helpers
except ImportError:
    import server as platform_helpers

app = FastAPI(
    title="Smart Agriculture Platform (SAP) API",
    description="Real Crop-Specific Plant Disease AI Pipeline & Farm Intelligence API",
    version="2.0.0"
)

# Enable CORS for all local origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Disease Analysis Endpoints ───────────────────────────────────────────────

@app.post("/api/disease/analyze")
async def analyze_disease_api(
    request: Request,
    image_file: Optional[UploadFile] = File(None),
    crop_form: Optional[str] = Form(None)
):
    """
    Main endpoint for real crop-specific disease diagnosis.
    Accepts:
    1. JSON body: { "image": "<base64_data_url>", "crop": "Wheat" }
    2. Multipart form: image_file=<binary>, crop_form="Wheat"
    """
    try:
        image_bytes = None
        crop_name = "general"

        # Check multipart upload
        if image_file is not None:
            image_bytes = await image_file.read()
            if crop_form:
                crop_name = crop_form

        # Otherwise parse JSON body
        if not image_bytes:
            try:
                body = await request.json()
            except Exception:
                body = {}

            crop_name = body.get("crop", crop_form or "Wheat")
            raw_img = body.get("image", "")

            if raw_img:
                if "," in raw_img:
                    _, raw_img = raw_img.split(",", 1)
                image_bytes = base64.b64decode(raw_img)

        if not image_bytes:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "NO_IMAGE_PROVIDED",
                    "message": "Please provide an image via JSON base64 or multipart upload."
                }
            )

        # Run Real AI Pipeline (Not_A_Leaf check + Crop-specific model + Grad-CAM)
        result = analyze_plant_disease(image_bytes, crop_name=crop_name)
        return JSONResponse(status_code=200, content=result)

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "message": f"Server error during disease analysis: {str(e)}"
            }
        )


@app.post("/api/disease-scan")
@app.post("/api/predict")
async def legacy_disease_scan_api(request: Request):
    """
    Legacy-compatible disease scan endpoint for existing frontend calls.
    Routes directly to real crop-specific AI models.
    """
    try:
        body = await request.json()
        raw_img = body.get("image", "")
        crop_name = body.get("crop", "Wheat")

        if not raw_img:
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "No image data provided."}
            )

        if "," in raw_img:
            _, raw_img = raw_img.split(",", 1)
        image_bytes = base64.b64decode(raw_img)

        result = analyze_plant_disease(image_bytes, crop_name=crop_name)
        return JSONResponse(status_code=200, content=result)

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Diagnosis failed: {str(e)}"}
        )


# ─── Weather & Location Endpoints ─────────────────────────────────────────────

@app.get("/api/weather")
async def get_weather(lat: float, lon: float, crop: str = "Wheat"):
    try:
        data = platform_helpers.get_weather_data(lat, lon, crop)
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})


@app.get("/api/geocode")
async def geocode(pincode: Optional[str] = None, q: Optional[str] = None):
    try:
        if pincode:
            data = platform_helpers.geocode_pincode(pincode)
            return JSONResponse(content=data)
        elif q:
            data = platform_helpers.geocode_city(q)
            return JSONResponse(content=data)
        else:
            return JSONResponse(status_code=400, content={"status": "error", "message": "Provide pincode or q."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})


@app.get("/api/health")
@app.get("/health")
async def health_check():
    key_configured = bool(os.environ.get("GEMINI_API_KEY", "").strip())
    if not key_configured and kisan_ai:
        key_configured = bool(kisan_ai.get_gemini_api_key())
    return JSONResponse(content={
        "status": "healthy",
        "service": "Smart Agriculture Platform (SAP) API",
        "gemini_configured": key_configured,
        "model": os.environ.get("GEMINI_MODEL", "gemini-3.8-flash"),
        "version": "2.0.0"
    })


# Import real AI Kisan Bot Assistant
try:
    import kisan_ai
except ImportError:
    kisan_ai = None


# ─── Kisan Bot Chat Endpoint ──────────────────────────────────────────────────

@app.post("/api/chat")
async def chat_api(request: Request):
    try:
        body = await request.json()
        message = body.get('message', '').strip()
        context = body.get('context') or {}
        if not isinstance(context, dict):
            context = {}

        # Safely merge top-level fields into context
        if 'crop' in body and 'crop' not in context:
            context['crop'] = body['crop']
        if 'location' in body and 'location' not in context:
            context['location'] = body['location']
        if 'locationData' in body and 'locationData' not in context:
            context['locationData'] = body['locationData']
        if 'weather' in body and 'weather' not in context:
            context['weather'] = body['weather']
        if 'soil' in body and 'soil' not in context:
            context['soil'] = body['soil']

        history = body.get('history', [])
        img_data = body.get('image')
        language = body.get('language') or body.get('lang') or context.get('language') or 'en'

        img_bytes = None
        mime_type = 'image/jpeg'
        if img_data:
            if ',' in img_data:
                header, img_data = img_data.split(',', 1)
                if 'png' in header:
                    mime_type = 'image/png'
                elif 'webp' in header:
                    mime_type = 'image/webp'
            img_bytes = base64.b64decode(img_data)

        if not message and not img_bytes:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "error": "EMPTY_MESSAGE",
                    "message": "Please provide a question or attach an image."
                }
            )

        if kisan_ai is not None:
            result = await asyncio.to_thread(
                kisan_ai.generate_kisan_chat_response,
                message=message,
                context=context,
                history=history,
                image_bytes=img_bytes,
                mime_type=mime_type,
                language=language
            )
        else:
            result = await asyncio.to_thread(
                platform_helpers.generate_kisan_chat_response,
                message=message,
                context=context,
                history=history,
                image_bytes=img_bytes,
                mime_type=mime_type,
                language=language
            )

        # Return HTTP 200 on success, appropriate error code on failure (NEVER HTTP 200 on error)
        if result.get('status') == 'success':
            return JSONResponse(status_code=200, content=result)
        else:
            err_code = result.get('error', '')
            status_code = 503 if err_code in ('API_KEY_NOT_CONFIGURED', 'GEMINI_CALL_FAILED') else 500
            return JSONResponse(status_code=status_code, content=result)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"status": "error", "error": str(e), "message": "Internal server error"})


# ─── Fertilizer, Mandi & Schemes Endpoints ─────────────────────────────────────

@app.post("/api/fertilizer")
@app.post("/api/fertilizer/recommend")
async def fertilizer_api(request: Request):
    try:
        body = await request.json()
        img_data = body.get('image')
        img_bytes = None
        mime_type = 'image/jpeg'
        if img_data:
            if ',' in img_data:
                header, img_data = img_data.split(',', 1)
                if 'png' in header:
                    mime_type = 'image/png'
                elif 'webp' in header:
                    mime_type = 'image/webp'
            img_bytes = base64.b64decode(img_data)
        body['image_bytes'] = img_bytes
        body['mime_type'] = mime_type

        result = platform_helpers.generate_fertilizer_advice(body)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})


@app.post("/api/mandi")
@app.post("/api/mandi/prices")
async def mandi_api(request: Request):
    try:
        body = await request.json()
        result = platform_helpers.get_mandi_prices(body)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})


@app.post("/api/schemes")
@app.post("/api/schemes/search")
async def schemes_api(request: Request):
    try:
        body = await request.json()
        result = platform_helpers.search_government_schemes(body)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})


# ─── Static Files & Frontend Mount ───────────────────────────────────────────

FRONTEND_DIRS = [
    os.path.join(BASE_DIR, 'www'),
    BASE_DIR
]

for fdir in FRONTEND_DIRS:
    if os.path.exists(os.path.join(fdir, 'index.html')):
        app.mount("/static", StaticFiles(directory=fdir), name="static")

        @app.get("/")
        async def serve_index():
            return FileResponse(os.path.join(fdir, 'index.html'))

        @app.get("/{file_path:path}")
        async def serve_static_file(file_path: str):
            p = os.path.join(fdir, file_path)
            if os.path.isfile(p):
                return FileResponse(p)
            index_path = os.path.join(fdir, 'index.html')
            return FileResponse(index_path)
        break


# ─── Server Launcher ──────────────────────────────────────────────────────────

def run(port: int = 8080):
    print("=" * 65)
    print("  [SAP] Smart Agriculture Platform — FastAPI Backend")
    print(f"  Web Portal:    http://localhost:{port}")
    print(f"  AI Disease:    POST http://localhost:{port}/api/disease/analyze")
    print(f"  AI Kisan Chat: POST http://localhost:{port}/api/chat")
    print(f"  Weather API:   GET  http://localhost:{port}/api/weather")
    print(f"  Geocode API:   GET  http://localhost:{port}/api/geocode")
    print("=" * 65)
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 8080
    run(port)
