from rest_framework import serializers
from .models import PhoneNumber, Career, Contact, BookDemo, Submission

JOB_TYPES = ['Full-Time', 'Part-Time', 'Internship', 'Contract']
SERVICES = ['Web Development', 'SEO', 'App Development', 'Marketing']
INDUSTRIES = ['SaaS', 'EdTech', 'Finance', 'Healthcare']
MEMBERS = ['1-10', '11-50', '51-200', '201-500', '500+']

class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ['countryCode', 'number']

    def validate_number(self, value):
        if not value.isdigit() or not (7 <= len(value) <= 15):
            raise serializers.ValidationError("Phone number must be digits only and 7–15 characters long.")
        return value


class CareerSerializer(serializers.ModelSerializer):
    phone = PhoneNumberSerializer()

    class Meta:
        model = Career
        fields = '__all__'

    def validate_email(self, value):
        if '@' not in value:
            raise serializers.ValidationError("Invalid email format.")
        return value

    def validate_linkedIn(self, value):
        if not value.startswith("https://"):
            raise serializers.ValidationError("LinkedIn URL must start with 'https://'")
        return value

    def validate_jobType(self, value):
        if value not in JOB_TYPES:
            raise serializers.ValidationError(f"Job type must be one of: {', '.join(JOB_TYPES)}")
        return value


class ContactSerializer(serializers.ModelSerializer):
    phone = PhoneNumberSerializer()

    class Meta:
        model = Contact
        fields = '__all__'

    def validate_email(self, value):
        if '@' not in value:
            raise serializers.ValidationError("Invalid email format.")
        return value

    def validate_services(self, value):
        if value not in SERVICES:
            raise serializers.ValidationError(f"Service must be one of: {', '.join(SERVICES)}")
        return value


class BookDemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookDemo
        fields = '__all__'

    def validate_email(self, value):
        if '@' not in value:
            raise serializers.ValidationError("Invalid email format.")
        return value

    def validate_phone(self, value):
        if not value.isdigit() or not (7 <= len(value) <= 15):
            raise serializers.ValidationError("Phone must be digits only and 7–15 characters long.")
        return value

    def validate_industry(self, value):
        if value not in INDUSTRIES:
            raise serializers.ValidationError(f"Industry must be one of: {', '.join(INDUSTRIES)}")
        return value

    def validate_members(self, value):
        if value not in MEMBERS:
            raise serializers.ValidationError(f"Members must be one of: {', '.join(MEMBERS)}")
        return value


class SubmissionSerializer(serializers.ModelSerializer):
    career = CareerSerializer()
    contact = ContactSerializer()
    bookDemo = BookDemoSerializer()

    class Meta:
        model = Submission
        fields = ['career', 'contact', 'bookDemo', 'timestamp']

    def create(self, validated_data):
        career_data = validated_data.pop('career')
        contact_data = validated_data.pop('contact')
        book_demo_data = validated_data.pop('bookDemo')

        # Handle nested phone data
        career_phone_data = career_data.pop('phone')
        contact_phone_data = contact_data.pop('phone')

        career_phone = PhoneNumber.objects.create(**career_phone_data)
        contact_phone = PhoneNumber.objects.create(**contact_phone_data)

        career = Career.objects.create(phone=career_phone, **career_data)
        contact = Contact.objects.create(phone=contact_phone, **contact_data)
        book_demo = BookDemo.objects.create(**book_demo_data)

        submission = Submission.objects.create(
            career=career,
            contact=contact,
            bookDemo=book_demo
        )
        return submission
