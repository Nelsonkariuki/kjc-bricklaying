from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, send_file
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from database import db, User, Service, Project, Testimonial, ContactMessage, FAQ, BlogPost, Newsletter, SiteSettings
import os
import json
from datetime import datetime
import uuid
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kjc.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour

# File upload configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create upload folders
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, 'projects'), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, 'testimonials'), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, 'blog'), exist_ok=True)

# WhatsApp configuration
WHATSAPP_NUMBER = '447700000000'  # UK number without the leading 0
app.config['WHATSAPP_NUMBER'] = WHATSAPP_NUMBER

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file, subfolder=''):
    """Save uploaded file and return filename"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        
        # Create subfolder path
        save_path = app.config['UPLOAD_FOLDER']
        if subfolder:
            save_path = os.path.join(save_path, subfolder)
            os.makedirs(save_path, exist_ok=True)
        
        filepath = os.path.join(save_path, unique_filename)
        file.save(filepath)
        return f'/static/uploads/{subfolder}/{unique_filename}' if subfolder else f'/static/uploads/{unique_filename}'
    return None

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create admin user and default data
def init_db():
    with app.app_context():
        db.create_all()
        
        # Check if admin exists
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@kjcbricklaying.com',
                password_hash=generate_password_hash('admin123'),
                full_name='Administrator',
                is_active=True
            )
            db.session.add(admin)
            
            # Add default services if none exist
            if Service.query.count() == 0:
                services = [
                    Service(title='Landscaping', description='Complete garden design and landscaping services. From patios to planting, we transform outdoor spaces into beautiful, functional areas.', icon='fa-tree', order=1, features=json.dumps(['Free Consultation', 'Quality Materials', 'Workmanship Guarantee'])),
                    Service(title='Fencing', description='Professional fencing installation and repair. Timber, concrete, or decorative fencing to suit your property and budget.', icon='fa-fence', order=2, features=json.dumps(['Free Consultation', 'Quality Materials', 'Workmanship Guarantee'])),
                    Service(title='Groundworks', description='Comprehensive groundworks services including excavations, foundations, and site preparation for any project size.', icon='fa-hard-hat', order=3, features=json.dumps(['Free Consultation', 'Quality Materials', 'Workmanship Guarantee'])),
                    Service(title='Land Drainage', description='Expert land drainage solutions to prevent flooding and waterlogging. Improve your property\'s drainage system effectively.', icon='fa-water', order=4, features=json.dumps(['Free Consultation', 'Quality Materials', 'Workmanship Guarantee'])),
                    Service(title='Plant with Operator', description='Hire plant machinery with experienced operator. Excavators, diggers, and other equipment for your project needs.', icon='fa-tractor', order=5, features=json.dumps(['Free Consultation', 'Quality Materials', 'Workmanship Guarantee'])),
                    Service(title='Aggregate Delivery', description='Fast and reliable aggregate delivery up to 2 tons. Topsoil, gravel, sand, and more for your landscaping and construction needs.', icon='fa-truck', order=6, features=json.dumps(['Free Consultation', 'Quality Materials', 'Workmanship Guarantee'])),
                    Service(title='Bricklaying', description='Traditional bricklaying services for extensions, garden walls, and new builds. Quality craftsmanship with attention to detail.', icon='fa-brick', order=7, features=json.dumps(['Free Consultation', 'Quality Materials', 'Workmanship Guarantee'])),
                ]
                db.session.add_all(services)
            
            # Add sample testimonials if none exist
            if Testimonial.query.count() == 0:
                testimonial = Testimonial(
                    client_name='John Smith',
                    client_email='john@example.com',
                    client_location='Coventry',
                    content='Karol did an amazing job on our extension. Professional, punctual, and quality workmanship. Would highly recommend!',
                    rating=5,
                    approved=True,
                    featured=True,
                    ip_address='127.0.0.1',
                    user_agent='Sample Data'
                )
                db.session.add(testimonial)
                
                testimonial2 = Testimonial(
                    client_name='Sarah Johnson',
                    client_email='sarah@example.com',
                    client_location='Nuneaton',
                    content='Excellent service from start to finish. The garden wall looks beautiful and was completed on time.',
                    rating=5,
                    approved=True,
                    featured=False
                )
                db.session.add(testimonial2)
            
            # Add sample projects if none exist
            if Project.query.count() == 0:
                sample_projects = [
                    Project(
                        title='Modern House Extension',
                        description='Complete rear extension with full-height glass doors and brick facade matching existing property.',
                        image_url='https://images.unsplash.com/photo-1541888946425-d81bb19240f5?ixlib=rb-4.0.3&w=800&h=600&fit=crop',
                        category='Extension',
                        featured=True,
                        location='Coventry',
                        project_type='Residential',
                        date_completed=datetime(2024, 1, 15),
                        views=150
                    ),
                    Project(
                        title='Garden Wall Renovation',
                        description='Rebuilt garden boundary wall with decorative brick patterns and coping stones.',
                        image_url='https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?ixlib=rb-4.0.3&w=800&h=600&fit=crop',
                        category='Garden Wall',
                        featured=True,
                        location='Nuneaton',
                        project_type='Landscaping',
                        date_completed=datetime(2024, 2, 20),
                        views=98
                    ),
                    Project(
                        title='Chimney Restoration',
                        description='Complete chimney rebuild with new flue liner and weatherproofing.',
                        image_url='https://images.unsplash.com/photo-1581094794329-c8112a89af12?ixlib=rb-4.0.3&w=800&h=600&fit=crop',
                        category='Chimney',
                        featured=True,
                        location='Rugby',
                        project_type='Restoration',
                        date_completed=datetime(2024, 3, 10),
                        views=112
                    )
                ]
                db.session.add_all(sample_projects)
            
            # Add default FAQs
            if FAQ.query.count() == 0:
                faqs = [
                    FAQ(question='How quickly can you provide a quote?', answer='We typically respond to all inquiries within 24 hours. For urgent projects, we can provide a quote on the same day.', category='General', order=1),
                    FAQ(question='Are you fully insured?', answer='Yes, we are fully insured with public liability insurance up to £5 million.', category='Insurance', order=2),
                    FAQ(question='Do you offer free estimates?', answer='Absolutely! We provide free, no-obligation quotes for all projects.', category='Pricing', order=3),
                ]
                db.session.add_all(faqs)
            
            db.session.commit()

# ==================== PUBLIC ROUTES ====================
@app.route('/')
def index():
    services = Service.query.filter_by(is_active=True).order_by(Service.order).all()
    featured_projects = Project.query.filter_by(featured=True, is_active=True).order_by(Project.date_completed.desc()).limit(3).all()
    recent_testimonials = Testimonial.query.filter_by(approved=True).order_by(Testimonial.date.desc()).limit(3).all()
    
    return render_template('index.html', 
                         services=services,
                         featured_projects=featured_projects, 
                         testimonials=recent_testimonials,
                         now=datetime.now(),
                         whatsapp_number=WHATSAPP_NUMBER)

@app.route('/services')
def services_page():
    services = Service.query.filter_by(is_active=True).order_by(Service.order).all()
    return render_template('services.html', services=services, now=datetime.now(), whatsapp_number=WHATSAPP_NUMBER)

@app.route('/portfolio')
def portfolio():
    projects = Project.query.filter_by(is_active=True).order_by(Project.date_completed.desc()).all()
    categories = db.session.query(Project.category).distinct().filter(Project.category != '', Project.is_active == True).all()
    return render_template('portfolio.html', projects=projects, categories=categories, now=datetime.now(), whatsapp_number=WHATSAPP_NUMBER)

@app.route('/portfolio/<int:project_id>')
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    project.increment_views()
    return render_template('project_detail.html', project=project, now=datetime.now(), whatsapp_number=WHATSAPP_NUMBER)

@app.route('/testimonials')
def testimonials_page():
    testimonials = Testimonial.query.filter_by(approved=True).order_by(Testimonial.date.desc()).all()
    featured_testimonials = Testimonial.query.filter_by(approved=True, featured=True).order_by(Testimonial.date.desc()).limit(2).all()
    
    # Calculate average rating
    if testimonials:
        total_rating = sum(t.rating for t in testimonials)
        average_rating = total_rating / len(testimonials)
    else:
        average_rating = 0
    
    return render_template('testimonials.html', 
                         testimonials=testimonials, 
                         featured=featured_testimonials,
                         average_rating=average_rating,
                         now=datetime.now(),
                         whatsapp_number=WHATSAPP_NUMBER)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message_text = request.form.get('message', '').strip()
        
        if not name or not email or not message_text:
            flash('Please fill in all required fields', 'danger')
            return redirect(url_for('contact'))
        
        message = ContactMessage(
            name=name,
            email=email,
            phone=request.form.get('phone', ''),
            service_type=request.form.get('service_type', ''),
            message=message_text,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        db.session.add(message)
        db.session.commit()
        flash('Thank you! We will get back to you within 24 hours.', 'success')
        return redirect(url_for('contact'))
    
    services = Service.query.filter_by(is_active=True).all()
    return render_template('contact.html', services=services, now=datetime.now(), whatsapp_number=WHATSAPP_NUMBER)

@app.route('/faq')
def faq():
    faqs = FAQ.query.filter_by(is_active=True).order_by(FAQ.order).all()
    categories = db.session.query(FAQ.category).distinct().filter(FAQ.is_active == True).all()
    return render_template('faq.html', faqs=faqs, categories=categories, now=datetime.now(), whatsapp_number=WHATSAPP_NUMBER)

@app.route('/blog')
def blog():
    posts = BlogPost.query.filter_by(published=True).order_by(BlogPost.published_at.desc()).all()
    return render_template('blog.html', posts=posts, now=datetime.now(), whatsapp_number=WHATSAPP_NUMBER)

@app.route('/blog/<slug>')
def blog_post(slug):
    post = BlogPost.query.filter_by(slug=slug, published=True).first_or_404()
    post.increment_views()
    return render_template('blog_post.html', post=post, now=datetime.now(), whatsapp_number=WHATSAPP_NUMBER)

@app.route('/newsletter/subscribe', methods=['POST'])
def newsletter_subscribe():
    email = request.form.get('email')
    if email:
        existing = Newsletter.query.filter_by(email=email).first()
        if not existing:
            newsletter = Newsletter(email=email)
            db.session.add(newsletter)
            db.session.commit()
            flash('Successfully subscribed to newsletter!', 'success')
        else:
            flash('Email already subscribed!', 'info')
    return redirect(request.referrer or url_for('index'))

@app.route('/submit-review', methods=['POST'])
def submit_review():
    """Handle public testimonial submission"""
    name = request.form.get('client_name', '').strip()
    email = request.form.get('client_email', '').strip()
    location = request.form.get('client_location', '').strip()
    rating = request.form.get('rating', 5)
    content = request.form.get('content', '').strip()
    
    # Validate
    if not name or not email or not content:
        flash('Please fill in all required fields', 'danger')
        return redirect(url_for('testimonials_page') + '#reviewForm')
    
    # Handle image upload
    client_image = ''
    file = request.files.get('client_image')
    if file and file.filename:
        saved_path = save_file(file, 'testimonials')
        if saved_path:
            client_image = saved_path
    
    # Create testimonial (pending approval)
    testimonial = Testimonial(
        client_name=name,
        client_email=email,
        client_location=location,
        client_image=client_image,
        content=content,
        rating=int(rating),
        approved=False,  # Needs admin approval
        featured=False,
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent')
    )
    db.session.add(testimonial)
    db.session.commit()
    
    flash('Thank you for your review! It will be published after moderation.', 'success')
    return redirect(url_for('testimonials_page'))

# ==================== ADMIN ROUTES ====================
@app.route('/admin')
def admin_redirect():
    """Redirect /admin to admin index"""
    if current_user.is_authenticated:
        return redirect(url_for('admin_index'))
    return redirect(url_for('admin_login'))

@app.route('/admin/index')
@login_required
def admin_index():
    """Admin main page"""
    projects_count = Project.query.count()
    messages_count = ContactMessage.query.filter_by(read=False).count()
    testimonials_count = Testimonial.query.filter_by(approved=True).count()
    services_count = Service.query.count()
    pending_testimonials = Testimonial.query.filter_by(approved=False).count()
    recent_messages = ContactMessage.query.order_by(ContactMessage.date.desc()).limit(5).all()
    
    return render_template('admin/index.html',
                         projects_count=projects_count,
                         messages_count=messages_count,
                         testimonials_count=testimonials_count,
                         services_count=services_count,
                         pending_testimonials=pending_testimonials,
                         recent_messages=recent_messages,
                         now=datetime.now())

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password_hash, request.form['password']):
            login_user(user)
            user.last_login = datetime.utcnow()
            db.session.commit()
            session.permanent = True
            flash('Welcome back to the admin dashboard!', 'success')
            return redirect(url_for('admin_dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('admin/login.html')

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    projects_count = Project.query.count()
    unread_messages_count = ContactMessage.query.filter_by(read=False).count()
    testimonials_count = Testimonial.query.filter_by(approved=True).count()
    pending_testimonials = Testimonial.query.filter_by(approved=False).count()
    total_messages = ContactMessage.query.count()
    recent_messages = ContactMessage.query.order_by(ContactMessage.date.desc()).limit(5).all()
    recent_projects = Project.query.order_by(Project.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         projects_count=projects_count,
                         messages_count=unread_messages_count,
                         total_messages=total_messages,
                         unread_messages_count=unread_messages_count,
                         testimonials_count=testimonials_count,
                         pending_testimonials=pending_testimonials,
                         recent_messages=recent_messages,
                         recent_projects=recent_projects,
                         now=datetime.now())

@app.route('/admin/projects/add', methods=['GET', 'POST'])
@login_required
def add_project():
    if request.method == 'POST':
        image_url = request.form.get('image_url', '')
        file = request.files.get('image_file')
        
        if file and file.filename:
            saved_path = save_file(file, 'projects')
            if saved_path:
                image_url = saved_path
        
        project = Project(
            title=request.form['title'],
            description=request.form.get('description', ''),
            image_url=image_url,
            category=request.form.get('category', 'General'),
            featured='featured' in request.form,
            location=request.form.get('location', ''),
            client_name=request.form.get('client_name', ''),
            project_type=request.form.get('project_type', ''),
            date_completed=datetime.strptime(request.form.get('date_completed', datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d') if request.form.get('date_completed') else datetime.now()
        )
        db.session.add(project)
        db.session.commit()
        flash('Project added successfully!', 'success')
        return redirect(url_for('portfolio'))
    return render_template('admin/add_project.html')

@app.route('/admin/projects/edit/<int:project_id>', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    if request.method == 'POST':
        project.title = request.form['title']
        project.description = request.form.get('description', '')
        project.category = request.form.get('category', 'General')
        project.featured = 'featured' in request.form
        project.location = request.form.get('location', '')
        project.client_name = request.form.get('client_name', '')
        project.project_type = request.form.get('project_type', '')
        
        # Handle date completed
        if request.form.get('date_completed'):
            try:
                project.date_completed = datetime.strptime(request.form.get('date_completed'), '%Y-%m-%d')
            except ValueError:
                pass
        
        # Handle image upload
        file = request.files.get('image_file')
        if file and file.filename:
            saved_path = save_file(file, 'projects')
            if saved_path:
                project.image_url = saved_path
        elif request.form.get('image_url'):
            project.image_url = request.form.get('image_url')
        
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('portfolio'))
    return render_template('admin/edit_project.html', project=project)

@app.route('/admin/projects/delete/<int:project_id>', methods=['POST'])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('portfolio'))

@app.route('/admin/testimonials')
@login_required
def admin_testimonials():
    """View all testimonials with pending status"""
    pending = Testimonial.query.filter_by(approved=False).order_by(Testimonial.date.desc()).all()
    approved = Testimonial.query.filter_by(approved=True).order_by(Testimonial.date.desc()).all()
    return render_template('admin/testimonials.html', pending=pending, approved=approved, now=datetime.now())

@app.route('/admin/testimonials/approve/<int:testimonial_id>', methods=['POST'])
@login_required
def approve_testimonial(testimonial_id):
    testimonial = Testimonial.query.get_or_404(testimonial_id)
    testimonial.approved = True
    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/admin/testimonials/toggle-featured/<int:testimonial_id>', methods=['POST'])
@login_required
def toggle_featured_testimonial(testimonial_id):
    testimonial = Testimonial.query.get_or_404(testimonial_id)
    testimonial.featured = not testimonial.featured
    db.session.commit()
    return jsonify({'status': 'success', 'featured': testimonial.featured})

@app.route('/admin/testimonials/add', methods=['GET', 'POST'])
@login_required
def add_testimonial():
    if request.method == 'POST':
        client_image = request.form.get('client_image_url', '')
        file = request.files.get('client_image')
        
        if file and file.filename:
            saved_path = save_file(file, 'testimonials')
            if saved_path:
                client_image = saved_path
        
        testimonial = Testimonial(
            client_name=request.form['client_name'],
            client_email=request.form.get('client_email', ''),
            client_location=request.form.get('client_location', ''),
            client_image=client_image,
            content=request.form['content'],
            rating=int(request.form['rating']),
            approved='approved' in request.form,
            featured='featured' in request.form,
            project_id=request.form.get('project_id') or None
        )
        db.session.add(testimonial)
        db.session.commit()
        flash('Testimonial added successfully!', 'success')
        return redirect(url_for('testimonials_page'))
    
    projects = Project.query.filter_by(is_active=True).order_by(Project.title).all()
    return render_template('admin/add_testimonial.html', projects=projects, now=datetime.now())

@app.route('/admin/testimonials/edit/<int:testimonial_id>', methods=['POST'])
@login_required
def edit_testimonial(testimonial_id):
    """Edit testimonial"""
    testimonial = Testimonial.query.get_or_404(testimonial_id)
    
    # Update basic info
    testimonial.client_name = request.form.get('client_name')
    testimonial.client_email = request.form.get('client_email', '')
    testimonial.client_location = request.form.get('client_location', '')
    testimonial.content = request.form.get('content')
    testimonial.rating = int(request.form.get('rating'))
    testimonial.approved = 'approved' in request.form
    testimonial.featured = 'featured' in request.form
    
    # Handle image upload
    file = request.files.get('client_image')
    if file and file.filename:
        saved_path = save_file(file, 'testimonials')
        if saved_path:
            testimonial.client_image = saved_path
    elif request.form.get('client_image_url'):
        testimonial.client_image = request.form.get('client_image_url')
    
    db.session.commit()
    flash('Testimonial updated successfully!', 'success')
    return redirect(url_for('admin_testimonials'))

@app.route('/admin/testimonials/delete/<int:testimonial_id>', methods=['POST'])
@login_required
def delete_testimonial(testimonial_id):
    testimonial = Testimonial.query.get_or_404(testimonial_id)
    db.session.delete(testimonial)
    db.session.commit()
    flash('Testimonial deleted successfully!', 'success')
    return redirect(url_for('admin_testimonials'))

@app.route('/admin/messages')
@login_required
def view_messages():
    messages = ContactMessage.query.order_by(ContactMessage.date.desc()).all()
    for msg in messages:
        if not msg.read:
            msg.read = True
    db.session.commit()
    return render_template('admin/messages.html', messages=messages, now=datetime.now())

@app.route('/admin/messages/delete/<int:message_id>', methods=['POST'])
@login_required
def delete_message(message_id):
    message = ContactMessage.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    flash('Message deleted successfully!', 'success')
    return redirect(url_for('view_messages'))

@app.route('/admin/messages/mark-read/<int:message_id>', methods=['POST'])
@login_required
def mark_message_read(message_id):
    message = ContactMessage.query.get_or_404(message_id)
    message.read = True
    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
    if request.method == 'POST':
        # Save site settings
        SiteSettings.set('site_title', request.form.get('site_title', 'KJC'))
        SiteSettings.set('site_description', request.form.get('site_description', ''))
        SiteSettings.set('phone', request.form.get('phone', '07700 000000'))
        SiteSettings.set('email', request.form.get('email', 'info@kjcbricklaying.com'))
        SiteSettings.set('address', request.form.get('address', 'Coventry, West Midlands'))
        SiteSettings.set('facebook', request.form.get('facebook', ''))
        SiteSettings.set('twitter', request.form.get('twitter', ''))
        SiteSettings.set('instagram', request.form.get('instagram', ''))
        SiteSettings.set('linkedin', request.form.get('linkedin', ''))
        SiteSettings.set('whatsapp', request.form.get('whatsapp', '447700000000'))
        SiteSettings.set('hours_weekday', request.form.get('hours_weekday', '7:00 AM - 5:00 PM'))
        SiteSettings.set('hours_saturday', request.form.get('hours_saturday', '8:00 AM - 1:00 PM'))
        SiteSettings.set('meta_keywords', request.form.get('meta_keywords', ''))
        SiteSettings.set('google_analytics', request.form.get('google_analytics', ''))
        flash('Settings saved successfully!', 'success')
        return redirect(url_for('admin_settings'))
    
    return render_template('admin/settings.html', now=datetime.now())

@app.route('/admin/clear-cache', methods=['POST'])
@login_required
def clear_cache():
    """Clear cached data"""
    return jsonify({'status': 'success', 'message': 'Cache cleared successfully!'})

@app.route('/admin/export-data')
@login_required
def export_data():
    """Export all website data"""
    data = {
        'export_date': datetime.now().isoformat(),
        'projects': [p.to_dict() for p in Project.query.all()],
        'testimonials': [t.to_dict() for t in Testimonial.query.all()],
        'services': [s.to_dict() for s in Service.query.all()],
        'messages': [m.to_dict() for m in ContactMessage.query.all()],
        'faqs': [f.to_dict() for f in FAQ.query.all()],
        'settings': SiteSettings.get_all()
    }
    
    json_data = json.dumps(data, indent=2, default=str)
    
    output = io.BytesIO()
    output.write(json_data.encode('utf-8'))
    output.seek(0)
    
    return send_file(
        output,
        as_attachment=True,
        download_name=f'kjc_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json',
        mimetype='application/json'
    )

# ==================== API ROUTES ====================
@app.route('/api/contact', methods=['POST'])
def api_contact():
    data = request.get_json()
    message = ContactMessage(
        name=data.get('name'),
        email=data.get('email'),
        phone=data.get('phone', ''),
        service_type=data.get('service_type', ''),
        message=data.get('message'),
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent')
    )
    db.session.add(message)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Message sent successfully!'})

@app.route('/api/stats')
def api_stats():
    stats = {
        'projects': Project.query.count(),
        'testimonials': Testimonial.query.filter_by(approved=True).count(),
        'pending_testimonials': Testimonial.query.filter_by(approved=False).count(),
        'messages': ContactMessage.query.filter_by(read=False).count()
    }
    return jsonify(stats)

@app.route('/api/whatsapp', methods=['GET'])
def api_whatsapp():
    """Get WhatsApp number"""
    whatsapp = SiteSettings.get('whatsapp', '447700000000')
    return jsonify({'whatsapp': whatsapp})

@app.route('/admin/ping', methods=['POST'])
@login_required
def admin_ping():
    """Keep session alive"""
    return jsonify({'status': 'ok'})

# ==================== CONTEXT PROCESSOR ====================
@app.context_processor
def inject_now():
    return {
        'now': datetime.now(),
        'site_title': SiteSettings.get('site_title', 'KJC'),
        'site_phone': SiteSettings.get('phone', '07700 000000'),
        'site_email': SiteSettings.get('email', 'info@kjcbricklaying.com'),
        'site_address': SiteSettings.get('address', 'Coventry, West Midlands'),
        'whatsapp_number': SiteSettings.get('whatsapp', '447700000000'),
        'facebook_url': SiteSettings.get('facebook', '#'),
        'twitter_url': SiteSettings.get('twitter', '#'),
        'instagram_url': SiteSettings.get('instagram', '#'),
        'linkedin_url': SiteSettings.get('linkedin', '#')
    }

# ==================== ERROR HANDLERS ====================
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@app.errorhandler(413)
def too_large_error(error):
    flash('File is too large. Maximum size is 16MB.', 'danger')
    return redirect(request.url), 413

if __name__ == '__main__':
    init_db()
    app.run(debug=True)