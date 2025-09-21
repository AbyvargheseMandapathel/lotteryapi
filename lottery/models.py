from django.db import models

class Lottery(models.Model):
    lottery_name = models.CharField(max_length=200)
    draw_number = models.CharField(max_length=50)
    draw_date = models.DateField()
    draw_time = models.CharField(max_length=50, blank=True, null=True)
    draw_location = models.TextField(blank=True, null=True)
    official_website = models.CharField(max_length=200, blank=True, null=True)
    official_email = models.EmailField(blank=True, null=True)
    government_website = models.CharField(max_length=200, blank=True, null=True)
    important_notice = models.TextField(blank=True, null=True)
    signature = models.TextField(blank=True, null=True)
    document_generated = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.lottery_name} ({self.draw_number})"

class ContactNumber(models.Model):
    lottery = models.OneToOneField(Lottery, related_name="contact_numbers", on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    director = models.CharField(max_length=20, blank=True, null=True)
    office = models.CharField(max_length=20, blank=True, null=True)

class Prize(models.Model):
    lottery = models.ForeignKey(Lottery, related_name="prizes", on_delete=models.CASCADE)
    prize_rank = models.CharField(max_length=50)
    prize_amount = models.CharField(max_length=100)
    winning_ticket_endings = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.prize_rank} - {self.lottery.lottery_name}"

class WinningTicket(models.Model):
    prize = models.ForeignKey(Prize, related_name="winning_tickets", on_delete=models.CASCADE)
    ticket_number = models.CharField(max_length=50)
    place = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.ticket_number

class ConsolationPrize(models.Model):
    prize = models.OneToOneField(Prize, related_name="consolation_prize", on_delete=models.CASCADE)
    amount = models.CharField(max_length=100)
    winning_tickets = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"Consolation for {self.prize.prize_rank}"