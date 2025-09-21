from django.contrib import admin
from .models import Lottery, Prize, WinningTicket, ConsolationPrize, ContactNumber
from .admin_views import lottery_upload_view
from django.urls import path


class WinningTicketInline(admin.TabularInline):
    model = WinningTicket
    extra = 0
    fields = ['ticket_number', 'place']
    can_delete = True


class ConsolationPrizeInline(admin.StackedInline):
    model = ConsolationPrize
    can_delete = True
    fields = ['amount', 'winning_tickets']


@admin.register(Prize)
class PrizeAdmin(admin.ModelAdmin):
    list_display = ['prize_rank', 'prize_amount', 'lottery']
    list_filter = ['prize_rank', 'lottery']
    search_fields = ['prize_rank', 'prize_amount']
    inlines = [WinningTicketInline, ConsolationPrizeInline]
    readonly_fields = ['winning_ticket_endings']

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields


@admin.register(Lottery)
class LotteryAdmin(admin.ModelAdmin):
    list_display = ["lottery_name", "draw_number", "draw_date"]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "upload-json/",
                self.admin_site.admin_view(lottery_upload_view),
                name="lottery-upload-json",
            ),
        ]
        return custom_urls + urls


@admin.register(WinningTicket)
class WinningTicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_number', 'place', 'prize']
    list_filter = ['prize__prize_rank']
    search_fields = ['ticket_number', 'place']


@admin.register(ConsolationPrize)
class ConsolationPrizeAdmin(admin.ModelAdmin):
    list_display = ['amount', 'prize']
    search_fields = ['amount']


@admin.register(ContactNumber)
class ContactNumberAdmin(admin.ModelAdmin):
    list_display = ['phone', 'director', 'office', 'lottery']
