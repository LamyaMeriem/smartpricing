"""FastAPI application entry point"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.config import settings
from app.api.v1 import auth

# Configure logging
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="SmartPricing Engine",
    description="SaaS for e-commerce pricing and inventory automation",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)

# ============================================================================
# Health Check Endpoints
# ============================================================================


@app.get("/health", tags=["Health"])
async def health():
    """Health check endpoint - used by Docker"""
    return {"status": "ok"}


@app.get("/readiness", tags=["Health"])
async def readiness():
    """Readiness check endpoint - used for load balancing"""
    return {"status": "ready"}

# ============================================================================
# Root Endpoint
# ============================================================================


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "name": "SmartPricing Engine",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health"
    }

# ============================================================================
# API v1 - Products (placeholder)
# ============================================================================


@app.get("/api/v1/products", tags=["Products"])
async def list_products():
    """Static test data"""
    return {
        "products": [
            {
                "id": "product-1",
                "name": "iPhone 12",
                "model": "iPhone 12",
                "source": "prestashop",
                "source_id": "123",
                "variants": [
                    {
                        "id": "variant-1",
                        "sku": "IPHONE12-128-BLACK-A",
                        "storage": "128GB",
                        "color": "Black",
                        "grade": "A",
                        "current_price": 299.99,
                        "current_stock": 4,
                        "source": "prestashop",
                        "source_id": "456",
                    },
                    {
                        "id": "variant-2",
                        "sku": "IPHONE12-64-WHITE-B",
                        "storage": "64GB",
                        "color": "White",
                        "grade": "B",
                        "current_price": 239.99,
                        "current_stock": 2,
                        "source": "prestashop",
                        "source_id": "457",
                    },
                ],
            }
        ]
    }


@app.get("/api/v1/products/{product_id}", tags=["Products"])
async def get_product(product_id: str):
    """Get a specific product"""
    return {"product_id": product_id, "name": "Product", "sku": "SKU123"}

# ============================================================================
# Startup / Shutdown Events
# ============================================================================


@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info(f"🚀 SmartPricing Engine starting in {settings.environment} mode")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info("🛑 SmartPricing Engine shutting down")

# ============================================================================
# Run (for local development)
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level=settings.log_level.lower()
    )
