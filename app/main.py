"""FastAPI application entry point and main configuration."""
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.api.v1.dependencies import get_db
from fastapi.middleware.cors import CORSMiddleware
from app.models.product import Product, ProductSource, ProductVariant
import logging
from pydantic import BaseModel
from app.config import settings
from app.api.v1 import auth
from app.db.base import Base
from app.db.session import engine

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

# Add CORS middleware to allow the frontend (or other services)
# to communicate with this API from different domains.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific allowed domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include modular routers for different API domains (e.g., authentication)
app.include_router(auth.router)

# ============================================================================
# Health Check Endpoints
# ============================================================================


@app.get("/health", tags=["Health"])
async def health():
    """Liveness check. Returns 200 if the app is running."""
    return {"status": "ok"}


@app.get("/readiness", tags=["Health"])
async def readiness():
    """
    Readiness check. Used by orchestrators like Kubernetes/Docker Swarm
    to check if the app is ready to receive traffic.
    """
    return {"status": "ready"}

# ============================================================================
# Root Endpoint
# ============================================================================


@app.get("/", tags=["Root"])
async def root():
    """Root landing page returning basic API info."""
    return {
        "name": "SmartPricing Engine",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health"
    }

# ============================================================================
# API v1 - Products (Placeholder logic for testing)
# ============================================================================


class ProductVariantCreate(BaseModel):
    sku: str
    storage: str | None = None
    color: str | None = None
    grade: str | None = None
    current_price: float | None = None
    current_stock: int = 0
    source: ProductSource = ProductSource.MANUAL
    source_id: str | None = None


class ProductCreate(BaseModel):
    name: str
    model: str | None = None
    description: str | None = None
    source: ProductSource = ProductSource.MANUAL
    source_id: str | None = None
    variants: list[ProductVariantCreate]


@app.get("/api/v1/products", tags=["Products"])
def list_products(db: Session = Depends(get_db)):
    """List products from the database."""
    products = db.query(Product).all()

    return {
        "products": [
            {
                "id": str(product.id),
                "name": product.name,
                "model": product.model,
                "source": product.source.value,
                "source_id": product.source_id,
                "variants": [
                    {
                        "id": str(variant.id),
                        "sku": variant.sku,
                        "storage": variant.storage,
                        "color": variant.color,
                        "grade": variant.grade,
                        "current_price": float(variant.current_price)
                        if variant.current_price is not None
                        else None,
                        "current_stock": variant.current_stock,
                        "source": variant.source.value,
                        "source_id": variant.source_id,
                    }
                    for variant in product.variants
                ],
            }
            for product in products
        ]
    }


@app.post("/api/v1/products", tags=["Products"], status_code=201)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    """Create a product with its variants."""
    product = Product(
        name=payload.name,
        model=payload.model,
        description=payload.description,
        source=payload.source,
        source_id=payload.source_id,
    )

    for variant_payload in payload.variants:
        variant = ProductVariant(
            sku=variant_payload.sku,
            storage=variant_payload.storage,
            color=variant_payload.color,
            grade=variant_payload.grade,
            current_price=variant_payload.current_price,
            current_stock=variant_payload.current_stock,
            source=variant_payload.source,
            source_id=variant_payload.source_id,
        )
        product.variants.append(variant)

    db.add(product)
    db.commit()
    db.refresh(product)

    return {
        "id": str(product.id),
        "name": product.name,
        "model": product.model,
        "variants": [
            {
                "id": str(variant.id),
                "sku": variant.sku,
                "storage": variant.storage,
                "color": variant.color,
                "grade": variant.grade,
                "current_price": float(variant.current_price)
                if variant.current_price is not None
                else None,
                "current_stock": variant.current_stock,
            }
            for variant in product.variants
        ],
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
    """Run on application startup."""
    Base.metadata.create_all(bind=engine)
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
