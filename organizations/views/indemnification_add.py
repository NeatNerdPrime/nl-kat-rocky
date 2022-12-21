from django.contrib import messages
from django.shortcuts import HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView
from django_otp.decorators import otp_required
from two_factor.views.utils import class_view_decorator
from account.forms import IndemnificationAddForm
from organizations.models import OrganizationMember, Indemnification
from organizations.mixins import OrganizationsMixin


@class_view_decorator(otp_required)
class IndemnificationAddView(OrganizationsMixin, FormView):
    template_name = "indemnification_add.html"
    form_class = IndemnificationAddForm
    success_url = reverse_lazy("indemnification_add")
    indemnification_present = False

    def form_valid(self, form):
        Indemnification.objects.get_or_create(user=self.request.user, organization=self.organization)
        self.add_success_notification()
        return HttpResponseRedirect(self.get_success_url())

    def add_success_notification(self):
        success_message = _("Indemnification successfully set.")
        messages.add_message(self.request, messages.SUCCESS, success_message)

    def get(self, *args, **kwargs):
        if Indemnification.objects.filter(organization=self.organization):
            self.indemnification_present = True
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = [
            {"url": "", "text": "Indemnifications"},
        ]
        context["indemnification_present"] = self.indemnification_present

        return context