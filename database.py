from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """Admin user model"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(120))
    avatar = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'avatar': self.avatar,
            'is_active': self.is_active,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Service(db.Model):
    """Service model for construction and bricklaying services"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(50), default='fa-brick')
    order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    image_url = db.Column(db.String(200))
    price_range = db.Column(db.String(50))
    duration = db.Column(db.String(50))
    features = db.Column(db.Text)  # JSON string of features
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Service {self.title}>'
    
    def get_features(self):
        """Return features as list"""
        if self.features:
            try:
                return json.loads(self.features)
            except (json.JSONDecodeError, TypeError):
                return []
        return []
    
    def set_features(self, features_list):
        """Set features from list"""
        self.features = json.dumps(features_list)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'icon': self.icon,
            'order': self.order,
            'is_active': self.is_active,
            'image_url': self.image_url,
            'price_range': self.price_range,
            'duration': self.duration,
            'features': self.get_features()
        }


class Project(db.Model):
    """Project model for portfolio items"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(200))
    category = db.Column(db.String(50))
    date_completed = db.Column(db.DateTime)
    featured = db.Column(db.Boolean, default=False)
    location = db.Column(db.String(100))
    client_name = db.Column(db.String(100))
    project_type = db.Column(db.String(50))
    before_image_url = db.Column(db.String(200))
    after_image_url = db.Column(db.String(200))
    gallery_images = db.Column(db.Text)  # JSON string of image URLs
    views = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    slug = db.Column(db.String(200), unique=True)  # SEO-friendly URL
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Project {self.title}>'
    
    def get_gallery_images(self):
        """Return gallery images as list"""
        if self.gallery_images:
            try:
                return json.loads(self.gallery_images)
            except (json.JSONDecodeError, TypeError):
                return []
        return []
    
    def set_gallery_images(self, images_list):
        """Set gallery images from list"""
        self.gallery_images = json.dumps(images_list)
    
    def increment_views(self):
        """Increment project view count"""
        self.views += 1
        db.session.commit()
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'image_url': self.image_url,
            'category': self.category,
            'date_completed': self.date_completed.isoformat() if self.date_completed else None,
            'featured': self.featured,
            'location': self.location,
            'client_name': self.client_name,
            'project_type': self.project_type,
            'before_image_url': self.before_image_url,
            'after_image_url': self.after_image_url,
            'gallery_images': self.get_gallery_images(),
            'views': self.views,
            'is_active': self.is_active,
            'slug': self.slug
        }


class Testimonial(db.Model):
    """Testimonial model for client reviews"""
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    client_email = db.Column(db.String(120), nullable=False)
    client_location = db.Column(db.String(100))
    client_image = db.Column(db.String(200))
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, default=5)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    approved = db.Column(db.Boolean, default=False)  # Default to False for pending approval
    featured = db.Column(db.Boolean, default=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete='SET NULL'))
    project = db.relationship('Project', backref='testimonials', foreign_keys=[project_id])
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Testimonial {self.client_name}>'
    
    def approve(self):
        """Approve testimonial"""
        self.approved = True
        db.session.commit()
    
    def reject(self):
        """Reject testimonial (soft delete)"""
        db.session.delete(self)
        db.session.commit()
    
    def to_dict(self):
        return {
            'id': self.id,
            'client_name': self.client_name,
            'client_email': self.client_email,
            'client_location': self.client_location,
            'client_image': self.client_image,
            'content': self.content,
            'rating': self.rating,
            'date': self.date.isoformat() if self.date else None,
            'approved': self.approved,
            'featured': self.featured,
            'project': self.project.title if self.project else None,
            'project_id': self.project_id
        }


class ContactMessage(db.Model):
    """Contact message model for inquiries"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    service_type = db.Column(db.String(100))
    message = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    read = db.Column(db.Boolean, default=False)
    responded = db.Column(db.Boolean, default=False)
    responded_at = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(200))
    
    def __repr__(self):
        return f'<ContactMessage from {self.name}>'
    
    def mark_as_read(self):
        """Mark message as read"""
        self.read = True
        db.session.commit()
    
    def mark_as_responded(self):
        """Mark message as responded"""
        self.responded = True
        self.responded_at = datetime.utcnow()
        db.session.commit()
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'service_type': self.service_type,
            'message': self.message,
            'date': self.date.isoformat() if self.date else None,
            'read': self.read,
            'responded': self.responded,
            'responded_at': self.responded_at.isoformat() if self.responded_at else None
        }


class FAQ(db.Model):
    """FAQ model for frequently asked questions"""
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), default='General')
    order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<FAQ {self.question[:50]}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'order': self.order,
            'is_active': self.is_active
        }


class BlogPost(db.Model):
    """Blog post model for content marketing"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.String(300))
    featured_image = db.Column(db.String(200))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'))
    author = db.relationship('User', backref='blog_posts', foreign_keys=[author_id])
    category = db.Column(db.String(50))
    tags = db.Column(db.String(200))  # Comma-separated tags
    views = db.Column(db.Integer, default=0)
    published = db.Column(db.Boolean, default=False)
    published_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<BlogPost {self.title}>'
    
    def get_tags(self):
        """Return tags as list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        return []
    
    def set_tags(self, tags_list):
        """Set tags from list"""
        if tags_list:
            self.tags = ', '.join([tag.strip() for tag in tags_list if tag.strip()])
        else:
            self.tags = None
    
    def increment_views(self):
        """Increment view count"""
        self.views += 1
        db.session.commit()
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'excerpt': self.excerpt,
            'featured_image': self.featured_image,
            'author': self.author.username if self.author else None,
            'category': self.category,
            'tags': self.get_tags(),
            'views': self.views,
            'published': self.published,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Newsletter(db.Model):
    """Newsletter subscription model"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100))
    subscribed_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Newsletter {self.email}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'subscribed_at': self.subscribed_at.isoformat() if self.subscribed_at else None,
            'is_active': self.is_active
        }


class SiteSettings(db.Model):
    """Site settings model for configuration"""
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text)
    description = db.Column(db.String(200))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<SiteSettings {self.key}>'
    
    @staticmethod
    def get(key, default=None):
        """Get setting value by key"""
        setting = SiteSettings.query.filter_by(key=key).first()
        return setting.value if setting else default
    
    @staticmethod
    def set(key, value):
        """Set setting value"""
        setting = SiteSettings.query.filter_by(key=key).first()
        if setting:
            setting.value = value
        else:
            setting = SiteSettings(key=key, value=value)
            db.session.add(setting)
        db.session.commit()
    
    @staticmethod
    def get_all():
        """Get all settings as dictionary"""
        settings = SiteSettings.query.all()
        return {setting.key: setting.value for setting in settings}
    
    def to_dict(self):
        return {
            'key': self.key,
            'value': self.value,
            'description': self.description,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


# Default site settings to be created
DEFAULT_SETTINGS = {
    'site_title': 'KJC Construction & Bricklaying',
    'site_description': 'Family-run construction and bricklaying business in Coventry. Quality workmanship, free quotes, 10+ years experience. Call today!',
    'phone': '07700 000000',
    'email': 'kjcbricklaying@gmail.com',
    'address': 'Coventry, West Midlands',
    'whatsapp': '447700000000',
    'facebook': '',
    'twitter': '',
    'instagram': '',
    'linkedin': '',
    'hours_weekday': '7:00 AM - 5:00 PM',
    'hours_saturday': '8:00 AM - 1:00 PM',
    'meta_keywords': 'bricklayer coventry, construction services, landscaping, fencing, groundworks, local builder coventry, garden walls, extensions',
    'google_analytics': ''
}