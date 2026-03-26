// Initialize AOS animations with better settings
AOS.init({
    duration: 800,
    once: true,
    offset: 100,
    easing: 'ease-out-quad'
});

// Smooth scroll for anchor links with offset
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;
        
        const target = document.querySelector(targetId);
        if (target) {
            const offset = 80;
            const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - offset;
            
            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        }
    });
});

// Form validation with real-time feedback
const forms = document.querySelectorAll('.needs-validation');
forms.forEach(form => {
    const inputs = form.querySelectorAll('input, textarea, select');
    
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateInput(this);
        });
        
        input.addEventListener('input', function() {
            if (this.classList.contains('is-invalid')) {
                validateInput(this);
            }
        });
    });
    
    form.addEventListener('submit', event => {
        let isValid = true;
        inputs.forEach(input => {
            if (!validateInput(input)) isValid = false;
        });
        
        if (!isValid) {
            event.preventDefault();
            event.stopPropagation();
        } else {
            // Show loading state
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Sending...';
                submitBtn.disabled = true;
                
                // Reset button after submission
                setTimeout(() => {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }, 3000);
            }
        }
        form.classList.add('was-validated');
    });
});

function validateInput(input) {
    const value = input.value.trim();
    let isValid = true;
    
    if (input.required && !value) {
        isValid = false;
        input.classList.add('is-invalid');
    } else if (input.type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            isValid = false;
            input.classList.add('is-invalid');
        } else {
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
        }
    } else if (input.type === 'tel' && value) {
        const phoneRegex = /^[\d\s\-+()]{10,}$/;
        if (!phoneRegex.test(value)) {
            isValid = false;
            input.classList.add('is-invalid');
        } else {
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
        }
    } else if (value) {
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
    } else if (!input.required) {
        input.classList.remove('is-invalid');
        input.classList.remove('is-valid');
    }
    
    return isValid;
}

// Phone number formatting
const phoneInputs = document.querySelectorAll('input[type="tel"]');
phoneInputs.forEach(phoneInput => {
    phoneInput.addEventListener('input', function(e) {
        let x = this.value.replace(/\D/g, '').match(/(\d{0,4})(\d{0,3})(\d{0,4})/);
        this.value = !x[2] ? x[1] : x[1] + ' ' + x[2] + (x[3] ? ' ' + x[3] : '');
    });
});

// Gallery lightbox
const galleryItems = document.querySelectorAll('.gallery-item');
if (galleryItems.length > 0) {
    // Create modal dynamically
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.id = 'galleryModal';
    modal.innerHTML = `
        <div class="modal-dialog modal-lg modal-dialog-centered">
            <div class="modal-content bg-dark">
                <div class="modal-header border-0">
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body text-center">
                    <img id="modalImage" src="" alt="" class="img-fluid rounded">
                </div>
            </div>
        </div>
    `;
    document.body.appendChild(modal);
    
    const modalImage = document.getElementById('modalImage');
    const bsModal = new bootstrap.Modal(modal);
    
    galleryItems.forEach(item => {
        item.addEventListener('click', () => {
            const img = item.querySelector('img');
            if (img) {
                modalImage.src = img.src;
                bsModal.show();
            }
        });
    });
}

// Back to top button
const backToTop = document.createElement('button');
backToTop.innerHTML = '<i class="fas fa-arrow-up"></i>';
backToTop.className = 'back-to-top';
document.body.appendChild(backToTop);

window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
        backToTop.style.display = 'flex';
    } else {
        backToTop.style.display = 'none';
    }
});

backToTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

// Lazy loading images
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                }
                observer.unobserve(img);
            }
        });
    });
    
    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// Add active class to current nav item
const currentPath = window.location.pathname;
const navLinks = document.querySelectorAll('.nav-link');
navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPath || (currentPath === '/' && href === '/')) {
        link.classList.add('active');
    }
});

// Counter animation for stats
function animateCounter(element, target) {
    let current = 0;
    const increment = target / 50;
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 20);
}

// Initialize counters if they exist
const counters = document.querySelectorAll('.stat-number[data-count]');
counters.forEach(counter => {
    const target = parseInt(counter.getAttribute('data-count'));
    if (!isNaN(target)) {
        animateCounter(counter, target);
    }
});

// Add hover effect to cards
const cards = document.querySelectorAll('.card, .service-card, .testimonial-card, .portfolio-card');
cards.forEach(card => {
    card.classList.add('hover-lift');
});

// Parallax effect for hero section
const heroSection = document.querySelector('.hero-section');
if (heroSection) {
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const heroBg = heroSection.querySelector('.hero-background');
        if (heroBg) {
            heroBg.style.transform = `translateY(${scrolled * 0.3}px)`;
        }
    });
}

// Wait for DOM to be fully loaded for all modal functionality
document.addEventListener('DOMContentLoaded', function() {
    
    // Portfolio Filter Functionality
    const filterButtons = document.querySelectorAll('.filter-btn');
    const portfolioItems = document.querySelectorAll('.portfolio-item');

    if (filterButtons.length > 0) {
        filterButtons.forEach(button => {
            button.addEventListener('click', () => {
                filterButtons.forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');
                
                const filterValue = button.getAttribute('data-filter');
                
                portfolioItems.forEach(item => {
                    if (filterValue === 'all' || item.getAttribute('data-category') === filterValue) {
                        item.style.display = 'block';
                        setTimeout(() => {
                            item.style.opacity = '1';
                            item.style.transform = 'scale(1)';
                        }, 10);
                    } else {
                        item.style.opacity = '0';
                        item.style.transform = 'scale(0.8)';
                        setTimeout(() => {
                            item.style.display = 'none';
                        }, 300);
                    }
                });
            });
        });
    }

    // Enhanced View Project Modal
    const viewProjectButtons = document.querySelectorAll('.view-project');
    const projectModalElement = document.getElementById('projectModal');
    
    if (viewProjectButtons.length > 0 && projectModalElement) {
        const projectModal = new bootstrap.Modal(projectModalElement);
        
        viewProjectButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                
                // Get all project details from data attributes
                const title = button.getAttribute('data-title') || 'Project';
                const description = button.getAttribute('data-description') || 'No description available.';
                const image = button.getAttribute('data-image') || 'https://via.placeholder.com/600x400?text=Project+Image';
                const category = button.getAttribute('data-category') || 'General';
                const location = button.getAttribute('data-location') || 'Location not specified';
                const client = button.getAttribute('data-client') || 'Client not specified';
                const date = button.getAttribute('data-full-date') || button.getAttribute('data-date') || 'Recent';
                const views = button.getAttribute('data-views') || '0';
                
                // Populate modal with all details
                const modalTitle = document.getElementById('modalProjectTitle');
                const modalDescription = document.getElementById('modalDescription');
                const modalImage = document.getElementById('modalImage');
                const modalDate = document.getElementById('modalDate');
                const modalClient = document.getElementById('modalClient');
                const modalViews = document.getElementById('modalViews');
                const modalCategoryBadge = document.getElementById('modalCategoryBadge');
                const modalLocationBadge = document.getElementById('modalLocationBadge');
                
                if (modalTitle) modalTitle.textContent = title;
                if (modalDescription) modalDescription.textContent = description;
                if (modalImage) modalImage.src = image;
                if (modalDate) modalDate.textContent = date;
                if (modalClient) modalClient.textContent = client;
                if (modalViews) modalViews.textContent = views;
                if (modalCategoryBadge) modalCategoryBadge.textContent = category;
                if (modalLocationBadge) modalLocationBadge.textContent = location;
                
                projectModal.show();
            });
        });
    }

    // Share functionality
    const shareBtn = document.getElementById('shareProjectBtn');
    if (shareBtn) {
        shareBtn.addEventListener('click', (e) => {
            e.preventDefault();
            const title = document.getElementById('modalProjectTitle')?.textContent || 'Project';
            if (navigator.share) {
                navigator.share({
                    title: title,
                    text: `Check out this project: ${title}`,
                    url: window.location.href,
                });
            } else {
                navigator.clipboard.writeText(window.location.href);
                alert('Link copied to clipboard!');
            }
        });
    }

    // Edit Project Modal
    const editProjectButtons = document.querySelectorAll('.edit-project');
    const editProjectModalElement = document.getElementById('editProjectModal');
    
    if (editProjectButtons.length > 0 && editProjectModalElement) {
        const editModal = new bootstrap.Modal(editProjectModalElement);
        const editForm = document.getElementById('editProjectForm');
        
        editProjectButtons.forEach(button => {
            button.addEventListener('click', function() {
                document.getElementById('edit_project_id').value = this.getAttribute('data-id') || '';
                document.getElementById('edit_title').value = this.getAttribute('data-title') || '';
                document.getElementById('edit_description').value = this.getAttribute('data-description') || '';
                document.getElementById('edit_category').value = this.getAttribute('data-category') || '';
                document.getElementById('edit_location').value = this.getAttribute('data-location') || '';
                document.getElementById('edit_client_name').value = this.getAttribute('data-client') || '';
                document.getElementById('edit_project_type').value = this.getAttribute('data-type') || '';
                document.getElementById('edit_date_completed').value = this.getAttribute('data-date') || '';
                document.getElementById('edit_featured').checked = this.getAttribute('data-featured') === 'True';
                document.getElementById('edit_image_url').value = this.getAttribute('data-image') || '';
                
                // Show current image preview
                const currentImage = this.getAttribute('data-image');
                const previewContainer = document.getElementById('currentImagePreview');
                if (previewContainer) {
                    if (currentImage && currentImage !== '') {
                        previewContainer.innerHTML = `<img src="${currentImage}" alt="Current image" class="rounded" style="max-width: 100px; max-height: 100px;">`;
                    } else {
                        previewContainer.innerHTML = '<span class="text-muted">No image</span>';
                    }
                }
                
                editModal.show();
            });
        });
        
        // Handle edit form submission
        if (editForm) {
            editForm.addEventListener('submit', function(e) {
                e.preventDefault();
                const submitBtn = this.querySelector('button[type="submit"]');
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Saving...';
                submitBtn.disabled = true;
                
                const formData = new FormData(this);
                const projectId = document.getElementById('edit_project_id').value;
                
                fetch(`/admin/projects/edit/${projectId}`, {
                    method: 'POST',
                    body: formData
                }).then(response => {
                    if (response.ok) {
                        location.reload();
                    } else {
                        alert('Error updating project');
                        submitBtn.innerHTML = originalText;
                        submitBtn.disabled = false;
                    }
                }).catch(error => {
                    console.error('Error:', error);
                    alert('Error updating project');
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                });
            });
        }
    }

    // View Testimonial Modal
    const viewTestimonialButtons = document.querySelectorAll('.view-testimonial');
    const testimonialModalElement = document.getElementById('viewTestimonialModal');
    
    if (viewTestimonialButtons.length > 0 && testimonialModalElement) {
        const testimonialModal = new bootstrap.Modal(testimonialModalElement);
        
        viewTestimonialButtons.forEach(button => {
            button.addEventListener('click', function() {
                document.getElementById('viewName').textContent = this.getAttribute('data-name') || 'Client';
                document.getElementById('viewEmail').textContent = this.getAttribute('data-email') || 'Not provided';
                document.getElementById('viewLocation').textContent = this.getAttribute('data-location') || 'Not specified';
                const rating = parseInt(this.getAttribute('data-rating')) || 5;
                document.getElementById('viewRating').innerHTML = `${'<i class="fas fa-star text-warning"></i>'.repeat(rating)}${'<i class="far fa-star text-muted"></i>'.repeat(5 - rating)} (${rating}/5)`;
                document.getElementById('viewContent').textContent = this.getAttribute('data-content') || '';
                document.getElementById('viewDate').textContent = this.getAttribute('data-date') || '';
                
                testimonialModal.show();
            });
        });
    }

    // Edit Testimonial Modal
    const editTestimonialButtons = document.querySelectorAll('.edit-testimonial');
    const editTestimonialModalElement = document.getElementById('editTestimonialModal');
    
    if (editTestimonialButtons.length > 0 && editTestimonialModalElement) {
        const editTestimonialModal = new bootstrap.Modal(editTestimonialModalElement);
        
        editTestimonialButtons.forEach(button => {
            button.addEventListener('click', function() {
                document.getElementById('edit_testimonial_id').value = this.getAttribute('data-id') || '';
                document.getElementById('edit_testimonial_name').value = this.getAttribute('data-name') || '';
                document.getElementById('edit_testimonial_email').value = this.getAttribute('data-email') || '';
                document.getElementById('edit_testimonial_location').value = this.getAttribute('data-location') || '';
                document.getElementById('edit_testimonial_rating').value = this.getAttribute('data-rating') || 5;
                document.getElementById('edit_testimonial_content').value = this.getAttribute('data-content') || '';
                document.getElementById('edit_testimonial_approved').checked = this.getAttribute('data-approved') === 'True';
                document.getElementById('edit_testimonial_featured').checked = this.getAttribute('data-featured') === 'True';
                
                // Show current image preview
                const currentImage = this.getAttribute('data-image');
                const previewContainer = document.getElementById('currentTestimonialImagePreview');
                if (previewContainer) {
                    if (currentImage && currentImage !== '') {
                        previewContainer.innerHTML = `<img src="${currentImage}" alt="Current image" class="rounded-circle" style="width: 60px; height: 60px; object-fit: cover;">`;
                    } else {
                        previewContainer.innerHTML = '<span class="text-muted">No image</span>';
                    }
                }
                
                editTestimonialModal.show();
            });
        });
    }

    // Message Modal Functionality
    const viewMessageButtons = document.querySelectorAll('.view-message');
    const messageModalElement = document.getElementById('messageModal');
    
    if (viewMessageButtons.length > 0 && messageModalElement) {
        const messageModal = new bootstrap.Modal(messageModalElement);
        
        viewMessageButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                
                document.getElementById('modalName').textContent = this.getAttribute('data-name') || '';
                document.getElementById('modalEmail').textContent = this.getAttribute('data-email') || '';
                document.getElementById('modalEmail').href = `mailto:${this.getAttribute('data-email')}`;
                document.getElementById('modalPhone').textContent = this.getAttribute('data-phone') || 'Not provided';
                document.getElementById('modalService').textContent = this.getAttribute('data-service') || 'Not specified';
                document.getElementById('modalMessage').textContent = this.getAttribute('data-message') || '';
                document.getElementById('modalDate').textContent = this.getAttribute('data-date') || '';
                
                document.getElementById('replyBtn').href = `mailto:${this.getAttribute('data-email')}?subject=Re: Your inquiry about ${this.getAttribute('data-service')}&body=Hello ${this.getAttribute('data-name')},%0D%0A%0D%0AThank you for contacting KJC. We've received your message and will get back to you shortly.%0D%0A%0D%0ABest regards,%0D%0AKJC Team`;
                
                // Mark as read if unread
                const messageCard = this.closest('.message-card');
                if (messageCard && messageCard.classList.contains('unread')) {
                    messageCard.classList.remove('unread');
                    const messageId = this.getAttribute('data-id');
                    fetch(`/admin/messages/mark-read/${messageId}`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' }
                    }).catch(err => console.log('Error marking as read:', err));
                }
                
                messageModal.show();
            });
        });
    }

    // WhatsApp Modal Functionality
    const whatsappNumber = "447700000000";
    const whatsappFloatBtn = document.getElementById('whatsappFloatBtn');
    const whatsappCtaBtn = document.getElementById('whatsappCtaBtn');
    const whatsappHeroBtn = document.getElementById('whatsappHeroBtn');
    const sendWhatsappBtn = document.getElementById('sendWhatsappBtn');
    const whatsappModalElement = document.getElementById('whatsappModal');
    
    function openWhatsAppModal(e) {
        e.preventDefault();
        if (whatsappModalElement) {
            const modal = new bootstrap.Modal(whatsappModalElement);
            modal.show();
        }
    }
    
    function sendWhatsAppMessage() {
        const message = document.getElementById('whatsappMessage')?.value || "Hello! I'm interested in your services.";
        const encodedMessage = encodeURIComponent(message);
        const whatsappUrl = `https://wa.me/${whatsappNumber}?text=${encodedMessage}`;
        window.open(whatsappUrl, '_blank');
    }
    
    if (whatsappFloatBtn) whatsappFloatBtn.addEventListener('click', openWhatsAppModal);
    if (whatsappCtaBtn) whatsappCtaBtn.addEventListener('click', openWhatsAppModal);
    if (whatsappHeroBtn) whatsappHeroBtn.addEventListener('click', openWhatsAppModal);
    if (sendWhatsappBtn) sendWhatsappBtn.addEventListener('click', sendWhatsAppMessage);
});

// Delete confirmation function
window.confirmDelete = function(itemName) {
    return confirm(`Are you sure you want to delete "${itemName}"? This action cannot be undone.`);
};

// Auto-expand textarea
const autoExpandTextareas = document.querySelectorAll('textarea');
autoExpandTextareas.forEach(textarea => {
    textarea.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 200) + 'px';
    });
});

// Image preview for file uploads
const fileInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
fileInputs.forEach(input => {
    input.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                // Look for preview container in various locations
                let previewContainer = this.closest('.mb-3')?.querySelector('.image-preview');
                if (!previewContainer) {
                    previewContainer = document.getElementById('currentImagePreview');
                }
                if (previewContainer) {
                    previewContainer.innerHTML = `<img src="${e.target.result}" class="img-fluid rounded" style="max-height: 150px;">`;
                    previewContainer.style.display = 'block';
                }
            }.bind(this);
            reader.readAsDataURL(file);
        }
    });
});

// Initialize all tooltips
const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
});

// Session keep-alive for admin
let sessionTimer;
function resetSessionTimer() {
    if (sessionTimer) clearTimeout(sessionTimer);
    sessionTimer = setTimeout(() => {
        fetch('/admin/ping', {
            method: 'POST',
            credentials: 'same-origin'
        }).catch(() => {});
    }, 300000);
}

// Only add session keep-alive if on admin pages
if (window.location.pathname.includes('/admin')) {
    ['click', 'mousemove', 'keypress'].forEach(event => {
        document.addEventListener(event, resetSessionTimer);
    });
    resetSessionTimer();
}