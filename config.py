import os

baseDir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "commack-lf-dev-key-2026")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///" + os.path.join(baseDir, "lostandfound.db"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(baseDir, "static", "uploads")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024 # 5mb
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
