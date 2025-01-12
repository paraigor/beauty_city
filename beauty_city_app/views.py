import random

import phonenumbers as ph
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from beauty_city_app.models import (
    Master,
    MasterDaySchedule,
    Salon,
    Service,
    ServiceType,
)


def index(request):
    context = {}
    return render(request, "index.html", context)


def generate_otp():
    return str(random.randint(1000, 9999))


def normalise_phone_number(pn):
    pn_parsed = ph.parse(pn, "RU")
    if ph.is_valid_number(pn_parsed):
        pn_normalized = ph.format_number(pn_parsed, ph.PhoneNumberFormat.E164)
    else:
        raise

    return pn_normalized


class UserRegistrationView(View):
    def get(self, request):
        if not request.session.get("next_url"):
            request.session["next_url"] = request.META.get("HTTP_REFERER", "/")
        return render(request, "registration.html", {"otp_verify": False})

    def post(self, request):
        if "otp" in request.POST:
            submitted_otp = request.POST.get("otp")
            saved_otp = request.session.get("otp")

            if submitted_otp == saved_otp:
                phone_number = request.session.get("phone_number")
                full_name = request.session.get("full_name")
                User = get_user_model()
                user = User.objects.create(
                    phone_number=phone_number, full_name=full_name
                )
                user.save()
                next_url = request.session["next_url"]
                login(request, user)
                return redirect(next_url)
            else:
                messages.error(
                    request, "Неверный код подтверждения. Попробуйте еще раз"
                )
                return render(
                    request, "registration.html", {"otp_verify": False}
                )
        else:
            form_data = request.POST
            full_name = form_data["full_name"]

            try:
                phone_number = normalise_phone_number(
                    form_data["phone_number"]
                )
            except ph.phonenumberutil.NumberParseException:
                messages.error(request, "Введен неверный телефонный номер")
                return render(
                    request, "registration.html", {"otp_verify": False}
                )

            otp = generate_otp()
            # send_sms_otp(phone_number, otp)

            request.session["otp"] = otp
            request.session["phone_number"] = phone_number
            request.session["full_name"] = full_name

            return render(
                request,
                "registration.html",
                {"otp_verify": True, "otp": otp, "phone_number": phone_number},
            )


class UserLoginView(View):
    def get(self, request):
        if not request.session.get("next_url"):
            request.session["next_url"] = request.META.get("HTTP_REFERER", "/")
        return render(request, "login.html", {"otp_verify": False})

    def post(self, request):
        if "otp" in request.POST:
            submitted_otp = request.POST.get("otp")
            saved_otp = request.session.get("otp")

            if submitted_otp == saved_otp:
                phone_number = request.session["phone_number"]
                User = get_user_model()
                user = User.objects.get(phone_number=phone_number)
                next_url = request.session["next_url"]
                login(request, user)
                return redirect(next_url)
            else:
                messages.error(
                    request, "Неверный код подтверждения. Попробуйте еще раз"
                )
                return render(request, "login.html", {"otp_verify": False})
        else:
            try:
                phone_number = normalise_phone_number(
                    request.POST["phone_number"]
                )
            except ph.phonenumberutil.NumberParseException:
                messages.error(request, "Введен неверный телефонный номер")
                return render(request, "login.html", {"otp_verify": False})
            User = get_user_model()
            try:
                user = User.objects.get(phone_number=phone_number)
            except ObjectDoesNotExist:
                messages.error(request, "Пользователь не найден")
                return render(request, "login.html", {"otp_verify": False})
            otp = generate_otp()
            # send_sms_otp(phone_number, otp)

            request.session["otp"] = otp
            request.session["phone_number"] = phone_number

            return render(
                request,
                "login.html",
                {"otp_verify": True, "otp": otp, "phone_number": phone_number},
            )


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("index")


@method_decorator(csrf_exempt, name="dispatch")
class TestDivView(View):
    def get(self, request):
        pass

    def post(self, request):
        new_data = int(request.POST["div_data"]) + 2
        return JsonResponse({"new_data": new_data})
