// ProSell - Professional Selling System JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize all popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert-dismissible');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Cart functionality
    initCartFunctions();

    // Quantity input validation
    initQuantityValidation();

    // Product image zoom
    initProductImageZoom();

    // Smooth scroll for anchor links
    initSmoothScroll();

    // Form validation
    initFormValidation();

    // AJAX cart updates
    initAjaxCart();
});

// Cart Functions
function initCartFunctions() {
    // Update cart quantity
    var quantityInputs = document.querySelectorAll('.cart-quantity-input');
    quantityInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            var form = this.closest('form');
            if (form) {
                form.submit();
            }
        });
    });

    // Remove item confirmation
    var removeButtons = document.querySelectorAll('.cart-remove-btn');
    removeButtons.forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to remove this item?')) {
                e.preventDefault();
            }
        });
    });

    // Clear cart confirmation
    var clearCartBtn = document.querySelector('.cart-clear-btn');
    if (clearCartBtn) {
        clearCartBtn.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to clear your cart?')) {
                e.preventDefault();
            }
        });
    }
}

// Quantity Input Validation
function initQuantityValidation() {
    var quantityInputs = document.querySelectorAll('input[type="number"]');
    quantityInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            var min = parseInt(this.getAttribute('min')) || 1;
            var max = parseInt(this.getAttribute('max'));
            var value = parseInt(this.value);

            if (value < min) {
                this.value = min;
            }
            if (max && value > max) {
                this.value = max;
            }
        });
    });
}

// Product Image Zoom
function initProductImageZoom() {
    var productImages = document.querySelectorAll('.product-image-zoom');
    productImages.forEach(function(img) {
        img.addEventListener('mousemove', function(e) {
            var rect = this.getBoundingClientRect();
            var x = e.clientX - rect.left;
            var y = e.clientY - rect.top;
            
            var xPercent = (x / rect.width) * 100;
            var yPercent = (y / rect.height) * 100;
            
            this.style.transformOrigin = xPercent + '% ' + yPercent + '%';
            this.style.transform = 'scale(1.5)';
        });

        img.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
}

// Smooth Scroll
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            var target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Form Validation
function initFormValidation() {
    var forms = document.querySelectorAll('.needs-validation');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

// AJAX Cart Functions
function initAjaxCart() {
    // Add to cart with AJAX
    var addToCartForms = document.querySelectorAll('.ajax-add-to-cart');
    addToCartForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            var formData = new FormData(this);
            var url = this.getAttribute('action');
            
            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    updateCartBadge(data.cart_count);
                    showToast(data.message, 'success');
                } else {
                    showToast(data.message, 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showToast('An error occurred. Please try again.', 'error');
            });
        });
    });
}

// Update Cart Badge
function updateCartBadge(count) {
    var badges = document.querySelectorAll('.cart-count-badge');
    badges.forEach(function(badge) {
        badge.textContent = count;
        if (count > 0) {
            badge.style.display = 'flex';
        } else {
            badge.style.display = 'none';
        }
    });
}

// Show Toast Notification
function showToast(message, type) {
    var toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container';
        document.body.appendChild(toastContainer);
    }

    var toastId = 'toast-' + Date.now();
    var bgClass = type === 'success' ? 'bg-success' : 'bg-danger';
    var iconClass = type === 'success' ? 'bi-check-circle' : 'bi-x-circle';

    var toastHtml = `
        <div id="${toastId}" class="toast align-items-center ${bgClass} text-white" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="bi ${iconClass} me-2"></i>${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;

    toastContainer.insertAdjacentHTML('beforeend', toastHtml);

    var toastElement = document.getElementById(toastId);
    var toast = new bootstrap.Toast(toastElement, { delay: 3000 });
    toast.show();

    toastElement.addEventListener('hidden.bs.toast', function() {
        this.remove();
    });
}

// Search suggestions
function initSearchSuggestions() {
    var searchInput = document.querySelector('.search-input');
    if (searchInput) {
        var timeout = null;
        searchInput.addEventListener('input', function() {
            clearTimeout(timeout);
            timeout = setTimeout(function() {
                // Implement search suggestions AJAX call here
            }, 300);
        });
    }
}

// Product filter
function filterProducts(category) {
    var url = new URL(window.location.href);
    if (category) {
        url.searchParams.set('category', category);
    } else {
        url.searchParams.delete('category');
    }
    window.location.href = url.toString();
}

// Sort products
function sortProducts(sortValue) {
    var url = new URL(window.location.href);
    if (sortValue) {
        url.searchParams.set('sort', sortValue);
    } else {
        url.searchParams.delete('sort');
    }
    window.location.href = url.toString();
}

// Wishlist toggle
function toggleWishlist(productId) {
    fetch('/wishlist/toggle/' + productId + '/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showToast(data.message, 'success');
            updateWishlistIcon(productId, data.in_wishlist);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Update wishlist icon
function updateWishlistIcon(productId, inWishlist) {
    var icon = document.querySelector('.wishlist-icon-' + productId);
    if (icon) {
        if (inWishlist) {
            icon.classList.remove('bi-heart');
            icon.classList.add('bi-heart-fill', 'text-danger');
        } else {
            icon.classList.remove('bi-heart-fill', 'text-danger');
            icon.classList.add('bi-heart');
        }
    }
}

// Get CSRF Token from cookie
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Lazy loading images
function initLazyLoading() {
    var lazyImages = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
        var imageObserver = new IntersectionObserver(function(entries, observer) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    var img = entry.target;
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            });
        });

        lazyImages.forEach(function(img) {
            imageObserver.observe(img);
        });
    } else {
        // Fallback for browsers without IntersectionObserver
        lazyImages.forEach(function(img) {
            img.src = img.dataset.src;
            img.removeAttribute('data-src');
        });
    }
}

// Sticky header
function initStickyHeader() {
    var header = document.querySelector('.navbar');
    if (header) {
        var sticky = header.offsetTop;
        
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > sticky) {
                header.classList.add('sticky-top');
            } else {
                header.classList.remove('sticky-top');
            }
        });
    }
}

// Back to top button
function initBackToTop() {
    var backToTopBtn = document.querySelector('.back-to-top');
    if (backToTopBtn) {
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTopBtn.classList.add('show');
            } else {
                backToTopBtn.classList.remove('show');
            }
        });

        backToTopBtn.addEventListener('click', function(e) {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
}

// Initialize on document ready
document.addEventListener('DOMContentLoaded', function() {
    initLazyLoading();
    initStickyHeader();
    initBackToTop();
});

// Handle window resize
var resizeTimer;
window.addEventListener('resize', function() {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function() {
        // Reinitialize components that need resize handling
    }, 250);
});
