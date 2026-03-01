from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from config import Config
from models import db, Item, Claim, Transaction
from datetime import datetime
import os

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# create the database tables if they dont exist
with app.app_context():
    db.create_all()

# checks if the file type is good
def allowedFile(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

# routes

@app.route("/")
def home():
    # get the recent items and stats for the home page
    recentItems = Item.query.filter_by(status="approved").order_by(Item.submittedAt.desc()).limit(6).all()
    totalFound = Item.query.filter(Item.status.in_(["approved", "claimed"])).count()
    totalClaimed = Item.query.filter_by(status="claimed").count()
    return render_template("home.html", recentItems=recentItems, totalFound=totalFound, totalClaimed=totalClaimed)

@app.route("/submit", methods=["GET", "POST"])
def submitItem():
    if request.method == "POST":
        # handles the photo upload
        photoName = None
        if "photo" in request.files:
            photo = request.files["photo"]
            if photo.filename != "" and allowedFile(photo.filename):
                safeName = secure_filename(photo.filename)
                # add a timestamp so the file names dont overlap or anything happens like that
                photoName = datetime.now().strftime('%Y%m%d%H%M%S') + "_" + safeName
                photo.save(os.path.join(app.config["UPLOAD_FOLDER"], photoName))

        newItem = Item(
            title=request.form["title"],
            category=request.form["category"],
            description=request.form["description"],
            location=request.form["location"],
            dateFound=request.form["dateFound"],
            finderName=request.form["finderName"],
            finderEmail=request.form["finderEmail"],
            photoFilename=photoName
        )
        db.session.add(newItem)
        db.session.commit()
        flash("Item submitted! It'll show up once an admin approves it.", "success")
        return redirect(url_for("home"))

    return render_template("submit.html")

@app.route("/search")
def search():
    query = request.args.get("q", "").strip()
    category = request.args.get("category", "all")
    sortBy = request.args.get("sort", "newest")

    # only show approved items
    results = Item.query.filter_by(status="approved")

    if query:
        searchTerm = "%" + query + "%"
        results = results.filter(
            db.or_(
                Item.title.ilike(searchTerm),
                Item.description.ilike(searchTerm),
                Item.location.ilike(searchTerm)
            )
        )
    if category != "all":
        results = results.filter_by(category=category)
    if sortBy == "oldest":
        results = results.order_by(Item.submittedAt.asc())
    else:
        results = results.order_by(Item.submittedAt.desc())

    items = results.all()
    return render_template("search.html", items=items, query=query, category=category, sortBy=sortBy)

@app.route("/item/<int:itemId>")
def itemDetail(itemId):
    item = Item.query.get_or_404(itemId)
    return render_template("item.html", item=item)

@app.route("/claim/<int:itemId>", methods=["GET", "POST"])
def claimItem(itemId):
    item = Item.query.get_or_404(itemId)
    if request.method == "POST":
        newClaim = Claim(
            itemId=item.id,
            claimantName=request.form["claimantName"],
            claimantEmail=request.form["claimantEmail"],
            message=request.form["message"]
        )
        db.session.add(newClaim)
        db.session.commit()
        flash("Claim submitted! The admin will review it and get back to you.", "success")
        return redirect(url_for("itemDetail", itemId=item.id))
    return render_template("claim.html", item=item)

# e-commerce which boosts a listing to the top of search results
# simulated payment and no real charges

@app.route("/boost/<int:itemId>", methods=["GET", "POST"])
def boostItem(itemId):
    item = Item.query.get_or_404(itemId)
    if request.method == "POST":
        # just store the last 4 digits of the credit card number
        cardNum = request.form.get("cardNumber", "")
        last4 = cardNum[-4:] if len(cardNum) >= 4 else "0000"
        txn = Transaction(
            itemId=item.id,
            buyerName=request.form["buyerName"],
            buyerEmail=request.form["buyerEmail"],
            cardLast4=last4,
            amount=2.99
        )
        db.session.add(txn)
        db.session.commit()
        flash("Payment processed! Your listing has been boosted.", "success")
        return redirect(url_for("itemDetail", itemId=item.id))
    return render_template("boost.html", item=item)

# admin

ADMIN_PASSWORD = os.environ.get("ADMIN_PASS", "commack2026")

@app.route("/admin", methods=["GET", "POST"])
def adminLogin():
    if session.get("isAdmin"):
        return redirect(url_for("adminDashboard"))
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            session["isAdmin"] = True
            flash("Logged in as admin.", "success")
            return redirect(url_for("adminDashboard"))
        else:
            flash("Wrong password, try again.", "error")
    return render_template("admin_login.html")

@app.route("/admin/dashboard")
def adminDashboard():
    if not session.get("isAdmin"):
        return redirect(url_for("adminLogin"))
    # pull everything the admin needs to see
    pendingItems = Item.query.filter_by(status="pending").order_by(Item.submittedAt.desc()).all()
    approvedItems = Item.query.filter_by(status="approved").order_by(Item.submittedAt.desc()).all()
    claimedItems = Item.query.filter_by(status="claimed").order_by(Item.submittedAt.desc()).all()
    openClaims = Claim.query.filter_by(status="open").order_by(Claim.filedAt.desc()).all()
    recentTxns = Transaction.query.order_by(Transaction.purchasedAt.desc()).limit(10).all()
    return render_template("admin.html", pendingItems=pendingItems, approvedItems=approvedItems,
        claimedItems=claimedItems, openClaims=openClaims, recentTxns=recentTxns)

# admin actions

@app.route("/admin/approve/<int:itemId>")
def approveItem(itemId):
    if not session.get("isAdmin"):
        return redirect(url_for("adminLogin"))
    item = Item.query.get_or_404(itemId)
    item.status = "approved"
    db.session.commit()
    flash("Approved: " + item.title, "success")
    return redirect(url_for("adminDashboard"))

@app.route("/admin/reject/<int:itemId>")
def rejectItem(itemId):
    if not session.get("isAdmin"):
        return redirect(url_for("adminLogin"))
    item = Item.query.get_or_404(itemId)
    item.status = "rejected"
    db.session.commit()
    flash("Rejected: " + item.title, "success")
    return redirect(url_for("adminDashboard"))

@app.route("/admin/markClaimed/<int:itemId>")
def markClaimed(itemId):
    if not session.get("isAdmin"):
        return redirect(url_for("adminLogin"))
    item = Item.query.get_or_404(itemId)
    item.status = "claimed"
    db.session.commit()
    flash("Marked as claimed: " + item.title, "success")
    return redirect(url_for("adminDashboard"))

@app.route("/admin/claim/<int:claimId>/<action>")
def handleClaim(claimId, action):
    if not session.get("isAdmin"):
        return redirect(url_for("adminLogin"))
    claim = Claim.query.get_or_404(claimId)
    if action == "approve":
        claim.status = "approved"
        claim.item.status = "claimed"
        flash("Claim approved for: " + claim.item.title, "success")
    elif action == "deny":
        claim.status = "denied"
        flash("Claim denied for: " + claim.item.title, "info")
    db.session.commit()
    return redirect(url_for("adminDashboard"))

@app.route("/logout")
def logout():
    session.pop("isAdmin", None)
    flash("Logged out.", "info")
    return redirect(url_for("home"))

@app.route("/accessibility")
def accessibility():
    return render_template("accessibility.html")

@app.route("/sources")
def sources():
    return render_template("sources.html")

if __name__ == "__main__":
    app.run(debug=True)
