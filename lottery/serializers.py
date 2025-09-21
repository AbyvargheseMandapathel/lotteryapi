from rest_framework import serializers
from .models import Lottery, Prize, WinningTicket, ConsolationPrize, ContactNumber


class LotteryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lottery
        fields = ["lottery_name", "draw_number", "draw_date"]


class WinningTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = WinningTicket
        fields = ["ticket_number", "place"]


class ConsolationPrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsolationPrize
        fields = ["amount", "winning_tickets"]


class PrizeSerializer(serializers.ModelSerializer):
    winning_tickets = WinningTicketSerializer(many=True, required=False)
    consolation_prize = ConsolationPrizeSerializer(required=False)
    all_winning_numbers = serializers.SerializerMethodField()

    class Meta:
        model = Prize
        fields = [
            "prize_rank",
            "prize_amount",
            "winning_ticket_endings",
            "winning_tickets",
            "consolation_prize",
            "all_winning_numbers",
        ]

    def get_all_winning_numbers(self, obj):
        numbers = []

        # WinningTicket objects
        if hasattr(obj, "winning_tickets"):
            if hasattr(obj.winning_tickets, "all"):
                numbers += [wt.ticket_number for wt in obj.winning_tickets.all() if wt.ticket_number]
            elif isinstance(obj.winning_tickets, list):
                numbers += [wt.get("ticket_number") for wt in obj.winning_tickets if wt.get("ticket_number")]

        # Winning ticket endings (lower prizes)
        if getattr(obj, "winning_ticket_endings", None):
            numbers += obj.winning_ticket_endings

        # Consolation prize numbers
        if hasattr(obj, "consolation_prize") and obj.consolation_prize:
            cp_tickets = getattr(obj.consolation_prize, "winning_tickets", [])
            if cp_tickets:
                numbers += cp_tickets

        return numbers

    def create(self, validated_data):
        lottery = self.context.get("lottery")
        if not lottery:
            raise serializers.ValidationError("Lottery context not provided.")

        winning_tickets_data = validated_data.pop("winning_tickets", [])
        consolation_data = validated_data.pop("consolation_prize", None)

        prize = Prize.objects.create(lottery=lottery, **validated_data)

        for wt in winning_tickets_data:
            WinningTicket.objects.create(prize=prize, **wt)

        if consolation_data:
            ConsolationPrize.objects.create(prize=prize, **consolation_data)

        return prize

    def update(self, instance, validated_data):
        winning_tickets_data = validated_data.pop("winning_tickets", None)
        consolation_data = validated_data.pop("consolation_prize", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if winning_tickets_data is not None:
            instance.winning_tickets.all().delete()
            for wt in winning_tickets_data:
                WinningTicket.objects.create(prize=instance, **wt)

        if consolation_data is not None:
            if hasattr(instance, "consolation_prize"):
                instance.consolation_prize.delete()
            ConsolationPrize.objects.create(prize=instance, **consolation_data)

        return instance


class ContactNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactNumber
        fields = ["phone", "director", "office"]


class LotterySerializer(serializers.ModelSerializer):
    prizes = PrizeSerializer(many=True)
    contact_numbers = ContactNumberSerializer(required=False)
    draw_date = serializers.DateField(input_formats=["%d/%m/%Y", "%Y-%m-%d"])

    class Meta:
        model = Lottery
        fields = "__all__"

    def create(self, validated_data):
        prizes_data = validated_data.pop("prizes", [])
        contact_data = validated_data.pop("contact_numbers", None)

        lottery = Lottery.objects.create(**validated_data)

        if contact_data:
            ContactNumber.objects.create(lottery=lottery, **contact_data)

        prize_serializer = PrizeSerializer(data=prizes_data, many=True, context={"lottery": lottery})
        prize_serializer.is_valid(raise_exception=True)
        prize_serializer.save()

        return lottery

    def update(self, instance, validated_data):
        prizes_data = validated_data.pop("prizes", [])
        contact_data = validated_data.pop("contact_numbers", None)

        # Update Lottery fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update ContactNumber
        if contact_data:
            if hasattr(instance, "contact_numbers"):
                instance.contact_numbers.delete()
            ContactNumber.objects.create(lottery=instance, **contact_data)

        # Delete old prizes
        instance.prizes.all().delete()

        # Create new prizes
        prize_serializer = PrizeSerializer(data=prizes_data, many=True, context={"lottery": instance})
        prize_serializer.is_valid(raise_exception=True)
        prize_serializer.save()

        return instance
