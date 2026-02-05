from sqlalchemy import Boolean, Column, Integer, String
from database import Base

# 1. MARKETPLACE TABLE
class ServiceFacility(Base):
    __tablename__ = "facilities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    facility_type = Column(String)
    country = Column(String, index=True)
    city = Column(String)
    tier = Column(String) # 'platinum' or 'free'
    is_verified = Column(Boolean, default=False)
    approvals = Column(String)

# 2. INTELLIGENCE TABLE
class GeopoliticalAlert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    headline = Column(String)
    risk_level = Column(String)
    region = Column(String)
    affected_country = Column(String)
    ai_advice = Column(String)
    source_url = Column(String)

# 3. USERS TABLE
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)

# 4. SHIPS TABLE (This is the one we need!)
class Ship(Base):
    __tablename__ = "ships"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    imo_number = Column(String)
    ship_type = Column(String)
    owner_email = Column(String, index=True)