import io
from django.http import HttpResponse
from django.contrib import admin
from django.utils import timezone
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from .models import Category, Plant, Order, OrderItem, Article, Tag, Cart, CartItem

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

def export_to_pdf(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="orders_{timezone.now().strftime("%Y%m%d")}.pdf"'
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    y = 750
    p.drawString(100, y, "GreenLife Orders Invoice")
    y -= 30
    for order in queryset:
        p.drawString(100, y, f"Order #{order.id} - Customer: {order.customer_name}")
        y -= 20
        p.drawString(120, y, f"Total: ${order.get_total_cost()} - Status: В ожидании")
        y -= 30
        if y < 100:
            p.showPage()
            y = 750
    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

export_to_pdf.short_description = "Скачать чеки (PDF)"

def mark_as_delivered(modeladmin, request, queryset):
    queryset.update(status='D')

mark_as_delivered.short_description = "Отметить как доставленные"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'published_at', 'is_active']
    list_filter = ['is_active', 'published_at', 'author']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    list_editable = ['is_active']
    raw_id_fields = ['tags', 'plants']

@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'price', 'is_in_stock', 'published_at']
    list_filter = ['is_in_stock', 'category', 'published_at']
    list_editable = ['price', 'is_in_stock']
    list_display_links = ['name']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description', 'category__name']
    raw_id_fields = ['category', 'tags']
    date_hierarchy = 'published_at'
    readonly_fields = ['created_at', 'updated_at']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['plant']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'status', 'display_plants', 'get_total', 'created_at']
    list_filter = ['status', 'created_at', 'updated_at']
    list_display_links = ['id', 'customer_name']
    search_fields = ['customer_name', 'customer_email']
    date_hierarchy = 'created_at'
    inlines = [OrderItemInline]
    readonly_fields = ['created_at', 'updated_at']
    actions = [export_to_pdf, mark_as_delivered]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('items__plant')

    @admin.display(description='Состав заказа')
    def display_plants(self, obj):
        return ", ".join([f"{item.plant.name} (x{item.quantity})" for item in obj.items.all()])

    @admin.display(description='Итоговая сумма', ordering='items')
    def get_total(self, obj):
        return f"${obj.get_total_cost()}"

class CartItemInline(admin.TabularInline):
    model = CartItem
    raw_id_fields = ['plant']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at']
    raw_id_fields = ['user']
    inlines = [CartItemInline]
