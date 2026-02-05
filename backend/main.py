import hashlib
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
from database import engine, get_db

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow the website to talk to the brain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- SECURITY TOOLS ---
def get_password_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password, hashed_password):
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password

# --- DATA SHAPES ---
class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str

class LoginRequest(BaseModel):
    email: str
    password: str

class ShipCreate(BaseModel):
    name: str
    imo: str
    type: str
    owner_email: str

class IntelReport(BaseModel):
    raw_text: str

# --- 1. USER REGISTRATION & LOGIN ---
@app.post("/register/")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = get_password_hash(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_pw, full_name=user.full_name)
    db.add(new_user)
    db.commit()
    return {"status": "User Created", "email": user.email}

@app.post("/login/")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    
    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    return {"status": "Login Successful", "user": user.full_name}

# --- 2. FLEET MANAGEMENT ---
@app.post("/add-ship/")
def add_ship(ship: ShipCreate, db: Session = Depends(get_db)):
    new_ship = models.Ship(name=ship.name, imo_number=ship.imo, ship_type=ship.type, owner_email=ship.owner_email)
    db.add(new_ship)
    db.commit()
    return {"status": "Ship Added", "ship": ship.name}

@app.get("/my-fleet/{email}")
def get_my_fleet(email: str, db: Session = Depends(get_db)):
    my_ships = db.query(models.Ship).filter(models.Ship.owner_email == email).all()
    return my_ships

# --- 3. CORE FEATURES (Search & Risk) ---
@app.get("/")
def read_root():
    return {"message": "NBNexus Systems Online"}

@app.post("/create-morocco-test/")
def create_test_data(db: Session = Depends(get_db)):
    subscriber = models.ServiceFacility(name="Casablanca Marine Safety (Subscriber)", facility_type="LSA Service", country="Morocco", city="Casablanca", tier="platinum", is_verified=True, approvals="ABS,LR")
    db.add(subscriber)
    db.commit()
    return {"status": "Marketplace Data Loaded"}

@app.get("/find-service/{country}")
def find_service(country: str, db: Session = Depends(get_db)):
    results = db.query(models.ServiceFacility).filter(models.ServiceFacility.country == country).order_by(models.ServiceFacility.tier.desc()).all()
    return results

@app.get("/check-risk/{region}")
def check_risk(region: str, db: Session = Depends(get_db)):
    alerts = db.query(models.GeopoliticalAlert).filter(models.GeopoliticalAlert.region == region).all()
    if not alerts:
        return {"status": "SAFE", "message": "No active threats detected."}
    return {"status": "WARNING", "alerts": alerts}

# --- 4. INTELLIGENCE ENGINE (Updated for Consistency) ---
@app.post("/analyze-intel/")
def analyze_intel(report: IntelReport, db: Session = Depends(get_db)):
    text = report.raw_text.lower()
    
    # DEFAULT STATE
    headline = "Routine Traffic"
    risk = "LOW"
    advice = "Maintain standard watch."
    region = "Global"

    # RULE 1: PIRACY
    if "pirate" in text or "skiff" in text or "weapon" in text:
        headline = "PIRACY ATTACK IMMINENT"
        risk = "CRITICAL"
        advice = "LOCKDOWN: Muster crew to citadel. Activate SSAS immediately. Increase speed."
        region = "Gulf of Aden"

    # RULE 2: DRONE/AIR
    elif "drone" in text or "uav" in text or "missile" in text:
        headline = "AERIAL THREAT DETECTED"
        risk = "HIGH"
        advice = "EVASIVE MANEUVERS: Alter course. Monitor air radar. Report to UKMTO."
        region = "Red Sea"

    # RULE 3: WEATHER
    elif "storm" in text or "hurricane" in text or "wind" in text:
        headline = "SEVERE WEATHER WARNING"
        risk = "MEDIUM"
        advice = "NAVIGATION HAZARD: Secure loose deck cargo. Check weather routing."
        region = "Pacific Ocean"

    # Save to database
    new_alert = models.GeopoliticalAlert(
        headline=headline, 
        risk_level=risk, 
        region=region, 
        affected_country=region, 
        ai_advice=advice, 
        source_url="AI Analysis"
    )
    db.add(new_alert)
    db.commit()

    # FORCE CLEAN DICTIONARY RETURN
    return {
        "status": "Intel Processed",
        "analysis": {
            "headline": headline,
            "risk_level": risk,
            "ai_advice": advice,
            "region": region
        }
    }