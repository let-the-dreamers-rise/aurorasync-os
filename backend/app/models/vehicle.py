"""
Vehicle model for storing vehicle information.
"""

from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base


class Vehicle(Base):
    """
    Vehicle table stores information about each vehicle in the fleet.
    
    Attributes:
        id: Primary key (auto-increment)
        vehicle_id: Unique vehicle identifier (e.g., VEH001)
        make: Vehicle manufacturer (e.g., Toyota, Honda)
        model: Vehicle model (e.g., Camry, Accord)
        year: Manufacturing year
        mileage: Current odometer reading
        owner_name: Name of the vehicle owner
        owner_phone: Contact phone number
        status: Current health status (healthy, warning, critical)
        created_at: Timestamp when record was created
        updated_at: Timestamp when record was last updated
    """
    
    __tablename__ = "vehicles"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Vehicle identification
    vehicle_id = Column(String(20), unique=True, nullable=False, index=True)
    make = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)
    mileage = Column(Integer, default=0)
    
    # Owner information
    owner_name = Column(String(100), nullable=False)
    owner_phone = Column(String(20), nullable=True)
    
    # Vehicle status
    status = Column(
        String(20),
        default="healthy",
        nullable=False,
        comment="Vehicle health status: healthy, warning, critical"
    )
    
    # Additional information
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    def __repr__(self):
        return f"<Vehicle(vehicle_id='{self.vehicle_id}', model='{self.make} {self.model}', status='{self.status}')>"
