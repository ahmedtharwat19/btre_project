from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Contact


def contact(request):
    if request.method == 'POST':
        listing = request.POST['listing']
        listing_id = request.POST['listing_id']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        realtor_email = request.POST['realtor_email']

        # check if user had made inquiry already

        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'You have already made an inquory in this listing')
                return redirect('/listings/' + listing_id)
                

        user_id = request.POST['user_id']
        contact = Contact(listing=listing, listing_id=listing_id, name=name, email=email
                            , phone=phone, message=message, user_id=user_id)
        contact.save()

        # Send Email
        send_mail(
            'Subject here',
            'Here is the message.' + listing + 'Hello ... ',
            'ahmedtharwat19@yahoo.com',
            [realtor_email, 'ahmed.tharwat19@gmail.com'],
            fail_silently=False,
        )

        messages.success(request, 'Your request has been submitted, a realtor will get back to you soon')
        return redirect('/listings/' + listing_id)