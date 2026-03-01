from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    dateFound = db.Column(db.String(20), nullable=False)
    photoFilename = db.Column(db.String(255), default=None)
    finderName = db.Column(db.String(100), nullable=False)
    finderEmail = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(20), default="pending")
    # pending / approved / claimed / rejected
    submittedAt = db.Column(db.DateTime, default=datetime.utcnow)
    claims = db.relationship("Claim", backref="item", lazy=True)

class Claim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    itemId = db.Column(db.Integer, db.ForeignKey("item.id"), nullable=False)
    claimantName = db.Column(db.String(100), nullable=False)
    claimantEmail = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="open")
    # open / approved / denied
    filedAt = db.Column(db.DateTime, default=datetime.utcnow)

class Transaction(db.Model):
    # simulated e-commerce which boosts a listing to the top of search
    id = db.Column(db.Integer, primary_key=True)
    itemId = db.Column(db.Integer, db.ForeignKey("item.id"), nullable=False)
    buyerName = db.Column(db.String(100), nullable=False)
    buyerEmail = db.Column(db.String(150), nullable=False)
    cardLast4 = db.Column(db.String(4), default="0000")
    amount = db.Column(db.Float, default=2.99)
    purchasedAt = db.Column(db.DateTime, default=datetime.utcnow)
    item = db.relationship("Item", backref="transactions")