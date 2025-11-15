# from django.contrib import admin
# from .models import Banner, ProductCategory, Product, Price

# # # Custom Admin Site Configuration
# # admin.site.site_header = "Siva Jewellery Administration"
# # admin.site.site_title = "Siva Jewellery Admin Portal"
# # admin.site.index_title = "Welcome to Siva Jewellery Management System"
# @admin.register(Banner)
# class BannerAdmin(admin.ModelAdmin):
#     list_display = ['name', 'active', 'created_at', 'updated_at']
#     list_filter = ['active', 'created_at']
#     search_fields = ['name']
#     readonly_fields = ['created_at', 'updated_at']


# @admin.register(ProductCategory)
# class ProductCategoryAdmin(admin.ModelAdmin):
#     list_display = ['category', 'slug', 'created_at']
#     search_fields = ['category', 'slug']
#     readonly_fields = ['created_at', 'updated_at']
#     prepopulated_fields = {'slug': ('category',)}


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['product_id', 'product_name', 'category', 'size', 'created_at']
#     list_filter = ['category', 'created_at']
#     search_fields = ['product_id', 'product_name']
#     readonly_fields = ['created_at', 'updated_at']
#     autocomplete_fields = ['category']


# @admin.register(Price)
# class PriceAdmin(admin.ModelAdmin):
#     list_display = ['gold_price', 'silver_price', 'effective_date', 'updated_at']
#     list_filter = ['effective_date']
#     readonly_fields = ['effective_date', 'updated_at']

from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.decorators import display
from .models import Banner, ProductCategory, Product, Price
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

admin.site.unregister(User)
admin.site.unregister(Group)

# Re-register with Unfold styling
@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    """Styled User admin with Unfold"""
    
    # Use Unfold forms for proper styling
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff_badge', 'is_active']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering = ['username']
    
    # Fieldsets for better form layout
    fieldsets = (
        ('User Information', {
            'fields': ('username', 'password')
        }),
        ('Personal Details', {
            'fields': ('first_name', 'last_name', 'email')
        }),
                ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            ),
            'classes': ('collapse',),  # Make collapsible
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',),
        }),
    )
    add_fieldsets = (
        ('Create New User', {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        ('Additional Information', {
            'fields': ('email', 'first_name', 'last_name'),
        }),
    )
    
    @display(description="Staff", label={"yes": "success", "no": "danger"}, boolean=True)
    def is_staff_badge(self, obj):
        """Show staff status with badge"""
        return "yes" if obj.is_staff else "no"

@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    """Styled Group admin with Unfold"""
    
    list_display = ['name', 'user_count']
    search_fields = ['name']
    ordering = ['name']
    
    # Better form layout
    fieldsets = (
        ('Group Information', {
            'fields': ('name',)
        }),
        ('Permissions', {
            'fields': ('permissions',),
            'description': 'Select permissions for this group'
        }),
    )
    @display(description="Users")
    def user_count(self, obj):
        """Show number of users in group"""
        count = obj.user_set.count()
        return format_html(
            '<span style="background: #f3f4f6; padding: 4px 12px; border-radius: 12px; font-weight: 500;">{} users</span>',
            count
        )
    
@admin.register(Banner)
class BannerAdmin(ModelAdmin):
    """Beautiful admin for Banner with image preview"""
    
    # List view configuration
    list_display = ['name', 'image_preview', 'active_badge', 'created_at', 'updated_at']
    list_filter = ['active', 'created_at']
    search_fields = ['name']
    list_editable = []
    readonly_fields = ['created_at', 'updated_at', 'image_preview_large']
    
    # Form layout - group fields nicely
    fieldsets = (
        ('Banner Information', {
            'fields': ('name', 'active'),
            'description': 'Internal name for identification (not shown on website)'
        }),
        ('Banner Image', {
            'fields': ('image', 'image_preview_large'),
            'description': 'Upload banner image (recommended size: 1920x1080px)'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),  # Collapsible section
        }),
    )
    
    # Custom display methods
    @display(description="Preview", label=True)
    def image_preview(self, obj):
        """Show small image thumbnail in list view"""
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 60px; height: 40px; object-fit: cover; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);" />',
                obj.image.url
            )
        return format_html('<span style="color: #999;">No image</span>')
    
    @display(description="Large Preview")
    def image_preview_large(self, obj):
        """Show large image preview in form view"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 400px; max-height: 300px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" />',
                obj.image.url
            )
        return format_html('<span style="color: #999;">No image uploaded</span>')
    
    @display(description="Status", label={"active": "success", "inactive": "danger"})
    def active_badge(self, obj):
        """Show active status with colored badge"""
        return "active" if obj.active else "inactive"


@admin.register(ProductCategory)
class ProductCategoryAdmin(ModelAdmin):
    """Beautiful admin for Product Categories"""
    
    list_display = ['category', 'slug', 'product_count', 'created_at']
    search_fields = ['category', 'slug']
    readonly_fields = ['slug', 'created_at', 'updated_at']
    
    # Form layout
    fieldsets = (
        ('Category Information', {
            'fields': ('category', 'slug'),
            'description': 'Slug is auto-generated from category name'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    @display(description="Products")
    def product_count(self, obj):
        """Show count of products in this category"""
        count = obj.products.count()
        return format_html(
            '<span style="background: #f3f4f6; padding: 4px 12px; border-radius: 12px; font-weight: 500;">{} products</span>',
            count
        )


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    """Beautiful admin for Products with image previews"""
    
    list_display = ['product_id', 'product_name', 'category', 'size', 'images_preview', 'created_at']
    list_filter = ['category', 'created_at', 'size']
    search_fields = ['product_id', 'product_name']
    readonly_fields = ['created_at', 'updated_at', 'image1_preview', 'image2_preview']
    autocomplete_fields = ['category']
    
    # Form layout
    fieldsets = (
        ('Product Information', {
            'fields': (('product_id', 'product_name'), 'category', 'size'),
            'description': 'Basic product details'
        }),
        ('Product Images', {
            'fields': (
                ('image1', 'image1_preview'),
                ('image2', 'image2_preview'),
            ),
            'description': 'Upload product images (recommended size: 800x800px)'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    # Custom display methods
    @display(description="Images", label=True)
    def images_preview(self, obj):
        """Show image thumbnails in list view"""
        images = []
        if obj.image1:
            images.append(format_html(
                '<img src="{}" style="width: 40px; height: 40px; object-fit: cover; border-radius: 4px; margin-right: 4px; box-shadow: 0 1px 2px rgba(0,0,0,0.1);" />',
                obj.image1.url
            ))
        if obj.image2:
            images.append(format_html(
                '<img src="{}" style="width: 40px; height: 40px; object-fit: cover; border-radius: 4px; box-shadow: 0 1px 2px rgba(0,0,0,0.1);" />',
                obj.image2.url
            ))
        if images:
            return format_html(''.join(str(img) for img in images))
        return format_html('<span style="color: #999;">No images</span>')
    
    @display(description="Image 1 Preview")
    def image1_preview(self, obj):
        """Show large preview of image 1"""
        if obj.image1:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" />',
                obj.image1.url
            )
        return format_html('<span style="color: #999;">No image uploaded</span>')
    
    @display(description="Image 2 Preview")
    def image2_preview(self, obj):
        """Show large preview of image 2"""
        if obj.image2:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" />',
                obj.image2.url
            )
        return format_html('<span style="color: #999;">No image uploaded</span>')


@admin.register(Price)
class PriceAdmin(ModelAdmin):
    """Beautiful admin for Gold & Silver Prices"""
    
    list_display = ['price_display', 'effective_date', 'updated_at', 'is_current']
    list_filter = ['effective_date']
    readonly_fields = ['effective_date', 'updated_at']
    
    # Form layout
    fieldsets = (
        ('Current Rates', {
            'fields': (('gold_price', 'silver_price'),),
            'description': 'Enter current gold and silver prices per gram'
        }),
        ('Timestamps', {
            'fields': ('effective_date', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    # Custom display methods
    @display(description="Current Prices", label=True)
    def price_display(self, obj):
        """Show formatted prices with currency"""
        # Convert Decimal to float for formatting
        gold_price_formatted = float(obj.gold_price)
        silver_price_formatted = float(obj.silver_price)
    
        return format_html(
            '<div style="display: flex; gap: 16px;">'
            '<span style="background: #fef3c7; color: #92400e; padding: 6px 12px; border-radius: 6px; font-weight: 600;">Gold: ₹{}/g</span>'
            '<span style="background: #e5e7eb; color: #374151; padding: 6px 12px; border-radius: 6px; font-weight: 600;">Silver: ₹{}/g</span>'
            '</div>',
            f'{gold_price_formatted:,.2f}',
            f'{silver_price_formatted:,.2f}'
        )
    
    @display(description="Status", label={"current": "success", "old": "secondary"}, boolean=True)
    def is_current(self, obj):
        """Check if this is the latest price entry"""
        latest = Price.objects.order_by('-effective_date').first()
        return obj.id == latest.id if latest else False
    
    class Meta:
        verbose_name = "Price Entry"
        verbose_name_plural = "Gold & Silver Prices"


# Optional: Customize admin site header
admin.site.site_header = "Siva Jewellery Administration"
admin.site.site_title = "Siva Jewellery Admin"
admin.site.index_title = "Jewelry Management Dashboard"
